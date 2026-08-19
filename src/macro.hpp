#include <cstdint>
#include <vector>
#include <string>
#include <algorithm>
#include <chrono>
#include <thread>
#include <iostream>

struct MacroAction {
    const std::string out_id;
    const uint64_t start_ms;
    const uint64_t duration_ms;
};

class Macro {
    std::vector<MacroAction> actions{};

    bool running{};

public:
    Macro() = default;

    // Macro(std::vector<MacroAction> init_actions) : actions(init_actions) {
    //     std::sort(actions.begin(), actions.end(), [](const MacroAction& a, const MacroAction& b) {
    //         return a.start_ms < b.start_ms;
    //     });
    // }

    void update(uint64_t time_ms) {
        std::cout << time_ms << '\n';
    }

    void run() {
        using std::chrono::steady_clock;
        using std::chrono::milliseconds;
        using std::chrono::microseconds;
        using std::chrono::duration_cast;
        using std::chrono::time_point;

        running = true;

        time_point init_time = steady_clock::now();
        microseconds wait_time{1000};

        while (running) {
            time_point start_time = steady_clock::now();
            uint64_t diff_time = duration_cast<milliseconds>(start_time - init_time).count();

            update(diff_time);

            std::this_thread::sleep_for(wait_time);
        }
    }

    void stop() {
        running = false;
    }
};
