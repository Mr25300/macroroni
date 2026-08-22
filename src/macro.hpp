#include "io.hpp"
#include "timer.hpp"

#include <cstdint>
#include <vector>
#include <algorithm>
#include <atomic>
#include <thread>

#include <iostream>

struct MacroAction {
    IOInfo output;
    uint64_t time_ms;
    uint32_t id{};
};

class Macro {
    IOController& io_control;
    std::vector<MacroAction> actions{};
    size_t loop_count{};
    uint64_t loop_delay{};

public:
    IOInfo start_trigger;
    IOInfo stop_trigger;

private:
    uint32_t next_id{};
    std::thread run_thread;
    std::atomic<bool> running{};

public:
    Macro(IOController& io, size_t loops, uint64_t delay_ms, std::vector<MacroAction> init_actions)
        : io_control{io}, actions{std::move(init_actions)}, loop_count{loops}, loop_delay{delay_ms}
    {
        std::stable_sort(actions.begin(), actions.end(), [](const MacroAction& a, const MacroAction& b) {
            return a.time_ms < b.time_ms;
        });

        for (MacroAction& action : actions) {
            action.id = next_id++;
        }
    }

    int32_t add_action(MacroAction action) {
        if (running) return -1;

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
        if (running) return;

        std::vector<MacroAction>::iterator it = std::find_if(
            actions.begin(), actions.end(),
            [action_id](const MacroAction& a) {
                return a.id == action_id;
            }
        );

        if (it != actions.end()) actions.erase(it);
    }

    void start() {
        if (running) return;
        if (run_thread.joinable()) run_thread.join();

        running = true;

        run_thread = std::thread{[this]() {
            const uint64_t last_time = actions.back().time_ms;
            const uint64_t loop_time = last_time + loop_delay;

            size_t action_index{};
            size_t loop_num{};

            run_timer(1000, [this, last_time, loop_time, &action_index, &loop_num](uint64_t time_ms) {
                if (!running) return false;

                while (true) {
                    uint64_t curr_time_ms = time_ms - loop_num * loop_time;

                    while (action_index < actions.size()) {
                        MacroAction& action = actions[action_index];

                        if (curr_time_ms >= action.time_ms) {
                            std::cout << action.output.code << ' ' << action.output.value << '\n';
                            // io_control.execute(action.out_info);
                            ++action_index;
                        } else {
                            break;
                        }
                    }

                    if (
                        curr_time_ms >= loop_time ||
                        // Never true if loop_count is 0
                        loop_num == loop_count - 1 && curr_time_ms >= last_time
                    ) {
                        ++loop_num;

                        if (loop_count == 0 || loop_num < loop_count) {
                            action_index = 0;
                        } else {
                            return false;
                        }
                    } else {
                        break;
                    }
                }

                return true;
            });

            running = false;
        }};
    }

    void stop() {
        if (!running) return;
        running = false;

        if (run_thread.joinable()) run_thread.join();
    }
};
