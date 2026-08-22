#pragma once

#include <chrono>
#include <thread>

template <typename Callback>
void run_timer(uint64_t interval, Callback&& callback) {
    using std::chrono::steady_clock;
    using std::chrono::time_point;
    using std::chrono::milliseconds;
    using std::chrono::microseconds;
    using std::chrono::duration_cast;

    microseconds interval_micro{interval};
    time_point init_time = steady_clock::now();

    while (true) {
        time_point start_time = steady_clock::now();
        uint64_t diff_time = duration_cast<milliseconds>(start_time - init_time).count();

        if (!callback(diff_time)) break;

        // TODO: add correction for extra time callback and sleep_for take

        std::this_thread::sleep_for(interval_micro);
    }
}
