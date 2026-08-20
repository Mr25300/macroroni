#include "macro.hpp"
#include "io_linux.hpp"

int main() {
#if defined(__linux__)
    LinuxIOController io_control{};
#else
    #error "Unsupported platform"
#endif
    // Takes about 30ms for the virtual input device to spawn in background

    Macro macro{io_control, 0, {
        {{1, 42, 1}, 0}, // Press shift
        {{1, 35, 1}, 0}, // Press "h"
        {{1, 35, 0}, 0}, // Release "h"
        {{1, 18, 1}, 100}, // Press "e"
        {{1, 18, 0}, 100}, // Release "e"
        {{1, 38, 1}, 200}, // Press "l"
        {{1, 38, 0}, 200}, // Release "l"
        {{1, 38, 1}, 300}, // Press "l"
        {{1, 38, 0}, 300}, // Release "l"
        {{1, 24, 1}, 400}, // Press "o"
        {{1, 24, 0}, 400}, // Release "o"
        {{1, 42, 0}, 500} // Release shift
    }};
    // macro.add_action({{1, 30, 1}, 100});
    // macro.add_action({{1, 31, 1}, 100});
    // uint32_t id = macro.add_action({{1, 32, 1}, 100});

    macro.run();

    // macro.remove_action(id);
    // macro.run();

    return 0;
}
