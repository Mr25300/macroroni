#include "macro.hpp"
#include "io_linux.hpp"

int main() {
#if defined(__linux__)
    LinuxIOController io_control{};
#else
    #error "Unsupported platform"
#endif
    // Takes about 30ms for the virtual input device to spawn in background

    Macro macro{io_control, 1, {
        {{1, 42, 1}, 100}, // Press shift
        {{1, 35, 1}, 100}, // Press "h"
        {{1, 35, 0}, 100}, // Release "h"
        {{1, 18, 1}, 200}, // Press "e"
        {{1, 18, 0}, 200}, // Release "e"
        {{1, 38, 1}, 300}, // Press "l"
        {{1, 38, 0}, 300}, // Release "l"
        {{1, 38, 1}, 300}, // Press "l"
        {{1, 38, 0}, 300}, // Release "l"
        {{1, 24, 1}, 400}, // Press "o"
        {{1, 24, 0}, 400}, // Release "o"
        {{1, 35, 1}, 500}, // Press "h"
        {{1, 35, 0}, 500}, // Release "h"
        {{1, 18, 1}, 600}, // Press "e"
        {{1, 18, 0}, 600}, // Release "e"
        {{1, 38, 1}, 700}, // Press "l"
        {{1, 38, 0}, 700}, // Release "l"
        {{1, 38, 1}, 800}, // Press "l"
        {{1, 38, 0}, 800}, // Release "l"
        {{1, 24, 1}, 900}, // Press "o"
        {{1, 24, 0}, 900}, // Release "o"
        {{1, 35, 1}, 1000}, // Press "h"
        {{1, 35, 0}, 1000}, // Release "h"
        {{1, 18, 1}, 1100}, // Press "e"
        {{1, 18, 0}, 1100}, // Release "e"
        {{1, 38, 1}, 1200}, // Press "l"
        {{1, 38, 0}, 1200}, // Release "l"
        {{1, 38, 1}, 1300}, // Press "l"
        {{1, 38, 0}, 1300}, // Release "l"
        {{1, 24, 1}, 1400}, // Press "o"
        {{1, 24, 0}, 1400}, // Release "o"
        {{1, 42, 0}, 1400} // Release shift
    }};
    // macro.add_action({{1, 30, 1}, 100});
    // macro.add_action({{1, 31, 1}, 100});
    // uint32_t id = macro.add_action({{1, 32, 1}, 100});

    macro.run();

    // macro.remove_action(id);
    // macro.run();

    return 0;
}
