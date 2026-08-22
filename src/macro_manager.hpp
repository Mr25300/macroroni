#include "macro.hpp"

#include <vector>

class MacroManager {
    IOController& io_control;
    std::vector<Macro> macros{};

public:
    MacroManager(IOController& io)
        : io_control{io}
    {
        io_control.listen([this](IOInfo input) {
            for (Macro& macro : macros) {
                if (macro.is_running() && input == macro.start_trigger) macro.start();
                else if (input == macro.stop_trigger) macro.stop();
            }
        });
    }

    ~MacroManager() {
        io_control.stop_listening();
    }
};
