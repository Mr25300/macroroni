#include "macro.hpp"
#include "io_linux.hpp"

int main() {
    LinuxIOController io_control{};

    Macro macro{io_control, {
        {{1, 30, 1}, 1000}, // Press "a"
        {{1, 30, 0}, 2000}, // Release "a"
        {{1, 48, 1}, 2000}, // Press "b"
        {{1, 46, 1}, 2000}, // Press "c"
        {{1, 48, 1}, 3000}, // Release "b"
        {{1, 46, 1}, 3000} // Release "c"
    }};
    macro.run();

    return 0;
}
