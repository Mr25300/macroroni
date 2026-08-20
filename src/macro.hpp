#include "io.hpp"

#include <cstdint>
#include <vector>
#include <algorithm>
#include <chrono>
#include <thread>
#include <iostream>

struct MacroAction {
    IOInfo out_info;
    uint64_t time_ms;
    uint32_t id{};
};

class Macro {
    IOController& io;
    std::vector<MacroAction> actions{};

    uint64_t next_id{};
    bool running{};
    size_t action_index{};

public:
    Macro(IOController& io, std::vector<MacroAction> init_actions)
        : io(io), actions(std::move(init_actions))
    {
        std::sort(actions.begin(), actions.end(), [](const MacroAction& a, const MacroAction& b) {
            return a.time_ms < b.time_ms;
        });

        for (MacroAction& action : actions) {
            action.id = next_id++;
        }
    }

    void add_action(MacroAction& action) {
        action.id = next_id++;

        std::vector<MacroAction>::iterator it = std::upper_bound(
            actions.begin(), actions.end(), action,
            [](const MacroAction& a, const MacroAction& b) {
                return a.time_ms < b.time_ms;
            }
        );

        actions.insert(it, action);
    }

    void run() {
        if (running) return;

        using std::chrono::steady_clock;
        using std::chrono::time_point;
        using std::chrono::milliseconds;
        using std::chrono::microseconds;
        using std::chrono::duration_cast;

        running = true;

        time_point init_time = steady_clock::now();
        microseconds wait_time{1000};

        while (running) {
            time_point start_time = steady_clock::now();
            uint64_t diff_time = duration_cast<milliseconds>(start_time - init_time).count();

            update(diff_time);

            if (!running) break;

            std::this_thread::sleep_for(wait_time);
        }
    }

    void update(uint64_t time_ms) {
        while (true) {
            MacroAction& action = actions[action_index];

            if (time_ms >= action.time_ms) {
                std::cout << action.out_info.code << '\n';

                ++action_index;

                if (action_index >= actions.size()) {
                    action_index = 0;

                    break;
                }

            } else {
                break;
            }
        }
    }

    void stop() {
        running = false;
        action_index = 0;
    }
};
