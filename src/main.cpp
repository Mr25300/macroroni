#include "macro.hpp"
#include "io_linux.hpp"

int main() {
#if defined(__linux__)
    LinuxIOController io_control{};
#else
    #error "Unsupported platform"
#endif

    Macro macro{io_control, {
        {{1, 42, 1}, 1000}, // Press shift
        {{1, 35, 1}, 1000}, // Press "h"
        {{1, 35, 0}, 1000}, // Release "h"
        {{1, 18, 1}, 1000}, // Press "e"
        {{1, 18, 0}, 1000}, // Release "e"
        {{1, 38, 1}, 1000}, // Press "l"
        {{1, 38, 0}, 1000}, // Release "l"
        {{1, 38, 1}, 1000}, // Press "l"
        {{1, 38, 0}, 1000}, // Release "l"
        {{1, 24, 1}, 1000}, // Press "o"
        {{1, 24, 0}, 1000}, // Release "o"
        {{1, 35, 1}, 1000}, // Press "h"
        {{1, 35, 0}, 1000}, // Release "h"
        {{1, 18, 1}, 1000}, // Press "e"
        {{1, 18, 0}, 1000}, // Release "e"
        {{1, 38, 1}, 1000}, // Press "l"
        {{1, 38, 0}, 1000}, // Release "l"
        {{1, 38, 1}, 1000}, // Press "l"
        {{1, 38, 0}, 1000}, // Release "l"
        {{1, 24, 1}, 1000}, // Press "o"
        {{1, 24, 0}, 1000}, // Release "o"
        {{1, 35, 1}, 1000}, // Press "h"
        {{1, 35, 0}, 1000}, // Release "h"
        {{1, 18, 1}, 1000}, // Press "e"
        {{1, 18, 0}, 1000}, // Release "e"
        {{1, 38, 1}, 1000}, // Press "l"
        {{1, 38, 0}, 1000}, // Release "l"
        {{1, 38, 1}, 1000}, // Press "l"
        {{1, 38, 0}, 1000}, // Release "l"
        {{1, 24, 1}, 1000}, // Press "o"
        {{1, 24, 0}, 1000}, // Release "o"
        {{1, 42, 1}, 1000} // Release shift
    }};
    macro.run();

    return 0;
}
