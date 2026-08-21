#include "macro.hpp"
#include "io_linux.hpp"

int main() {
#if defined(__linux__)
    LinuxIOController io_control{};
#else
    #error "Unsupported platform"
#endif
    // Takes about 30ms for the virtual input device to spawn in background

    Macro macro{io_control, 5, 500, {
        {{1, 42, 1}, 10}, // Press shift
        {{1, 35, 1}, 10}, // Press "h"
        {{1, 35, 0}, 10}, // Release "h"
        {{1, 18, 1}, 20}, // Press "e"
        {{1, 18, 0}, 20}, // Release "e"
        {{1, 38, 1}, 30}, // Press "l"
        {{1, 38, 0}, 30}, // Release "l"
        {{1, 38, 1}, 40}, // Press "l"
        {{1, 38, 0}, 40}, // Release "l"
        {{1, 24, 1}, 50}, // Press "o"
        {{1, 24, 0}, 50}, // Release "o"
        {{1, 42, 0}, 50} // Release shift
    }};
    // macro.add_action({{1, 30, 1}, 100});
    // macro.add_action({{1, 31, 1}, 100});
    // uint32_t id = macro.add_action({{1, 32, 1}, 100});

    macro.run();

    // macro.remove_action(id);
    // macro.run();

    return 0;
}
