#if defined(__linux__)

#pragma once

#include "io.hpp"

#include <fcntl.h>
#include <unistd.h>
#include <sys/ioctl.h>
#include <linux/uinput.h>
#include <cstring>
#include <filesystem>
#include <poll.h>
#include <thread>
#include <atomic>

class LinuxIOController : public IOController {
    int fd{-1};

    std::atomic<bool> listening;
    std::thread listen_thread;

public:
    LinuxIOController() {
        fd = open("/dev/uinput", O_WRONLY | O_NONBLOCK);
        if (fd < 0) return;

        ioctl(fd, UI_SET_EVBIT, EV_KEY);

        for (std::size_t i{}; i <= KEY_MAX; ++i) {
            ioctl(fd, UI_SET_KEYBIT, i);
        }

        struct uinput_setup usetup;
        std::memset(&usetup, 0, sizeof(usetup));
        usetup.id.bustype = BUS_USB;
        usetup.id.vendor = 0x1234;
        usetup.id.product = 0x5678;
        std::strcpy(usetup.name, "Macro Virtual Keyboard");

        ioctl(fd, UI_DEV_SETUP, &usetup);
        ioctl(fd, UI_DEV_CREATE);
    }

    ~LinuxIOController() {
        if (fd >= 0) {
            ioctl(fd, UI_DEV_DESTROY);
            close(fd);
        }
    }

    void execute(const IOInfo& info) {
        if (fd < 0) return;

        struct input_event ev{};
        ev.type = info.type;
        ev.code = info.code;
        ev.value = info.value;
        ev.time.tv_sec = 0;
        ev.time.tv_usec = 0;

        write(fd, &ev, sizeof(ev));

        struct input_event syn{};
        syn.type = EV_SYN;
        syn.code = SYN_REPORT;
        syn.value = 0;
        write(fd, &syn, sizeof(syn));
    }

    void listen(std::function<void(IOInfo input)> callback) {
        if (listening) stop_listening();

        listen_thread = std::thread([this, callback]() {
            std::vector<pollfd> pfds;

            std::filesystem::path input_dir = "/dev/input";
            if (!std::filesystem::exists(input_dir)) return;

            for (const auto& entry : std::filesystem::directory_iterator(input_dir)) {
                if (entry.is_regular_file() || entry.is_character_file()) {
                    std::string filename = entry.path().filename().string();
                    if (filename.rfind("event", 0) != 0) continue;

                    int fd = open(filename.c_str(), O_RDONLY);
                    if (fd < 0) continue;

                    pfds.push_back({fd, POLLIN, 0});

                    // pfds.push_back({
                    //     .fd = fd,
                    //     .events = POLLIN,
                    //     .revents = 0
                    // });
                }
            }

            while (listening) {
                int timeout_ms = 100;
                int ready = poll(pfds.data(), pfds.size(), timeout_ms);

                if (ready < 0) {
                    if (errno == EINTR) continue;
                    else break;
                }

                if (ready == 0) continue;

                for (size_t i{}; i < pfds.size(); ++i) {
                    if (pfds[i].revents & POLLIN) {
                        struct input_event ev{};
                        ssize_t bytes_read = read(pfds[i].fd, &ev, sizeof(ev));

                        if (bytes_read == sizeof(ev)) {
                            callback({ev.type, ev.code, ev.value});
                        }
                    }
                }
            }
        });
    }

    void stop_listening() {
        if (!listening) return;

        listening = false;
        if (listen_thread.joinable()) listen_thread.join();
    }
};

#endif
