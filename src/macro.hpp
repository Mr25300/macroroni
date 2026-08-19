#include <vector>
#include <string>
#include <algorithm>

struct MacroAction {
    const std::string out_id;
    const int start_ms;
    const int duration_ms;
};

class Macro {
    std::vector<MacroAction> actions;

public:
    Macro(std::vector<MacroAction> initActions) : actions(initActions) {
        std::sort(actions.begin(), actions.end(), [](const MacroAction& a, const MacroAction& b) {
            return a.start_ms < b.start_ms;
        });
    }
};
