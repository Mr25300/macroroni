#if defined(__linux__)

#pragma once

#include "io.hpp"

#include <fcntl.h>
#include <unistd.h>
#include <sys/ioctl.h>
#include <linux/uinput.h>
#include <cstring>

class LinuxIOController : public IOController {
    int fd{-1};

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
};

#endif
