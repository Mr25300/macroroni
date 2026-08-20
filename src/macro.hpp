#include "io.hpp"
#include "timer.hpp"

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
    IOController& io_control;
    std::vector<MacroAction> actions{};
    size_t loop_count{};

    uint32_t next_id{};
    bool running{};

public:
    Macro(IOController& io, size_t loops, std::vector<MacroAction> init_actions)
        : io_control{io}, actions{std::move(init_actions)}, loop_count{loops}
    {
        std::stable_sort(actions.begin(), actions.end(), [](const MacroAction& a, const MacroAction& b) {
            return a.time_ms < b.time_ms;
        });

        for (MacroAction& action : actions) {
            action.id = next_id++;
        }
    }

    uint32_t add_action(MacroAction action) {
        std::vector<MacroAction>::iterator it = std::upper_bound(
            actions.begin(), actions.end(), action,
            [](const MacroAction& a, const MacroAction& b) {
                return a.time_ms < b.time_ms;
            }
        );

        actions.insert(it, std::move(action));

        return action.id = next_id++;
    }

    void remove_action(uint32_t action_id) {
        std::vector<MacroAction>::iterator it = std::find_if(
            actions.begin(), actions.end(),
            [action_id](const MacroAction& a) {
                return a.id == action_id;
            }
        );

        if (it != actions.end()) actions.erase(it);
    }

    void run() {
        if (running) return;

        running = true;

        size_t action_index{};
        size_t loop_num{};

        size_t loop_time = actions.back().time_ms;

        run_timer(1000, [&](uint64_t time_ms) {
            if (!running) return false;

            while (action_index < actions.size()) {
                MacroAction& action = actions[action_index];

                if (time_ms % loop_time >= action.time_ms % loop_time) {
                    std::cout << action.out_info.code << ' ' << action.out_info.value << '\n';
                    // io_control.execute(action.out_info);

                    ++action_index;

                } else {
                    break;
                }
            }

            if (action_index >= actions.size()) {
                ++loop_num;

                if (loop_count == 0 || loop_num < loop_count) {
                    action_index = 0;

                } else {
                    return false;
                }
            }

            return true;
        });

        running = false;
    }

    void stop() {
        running = false;
    }
};
