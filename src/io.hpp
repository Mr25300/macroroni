#pragma once

#include <cstdint>
#include <functional>

struct IOInfo {
    uint16_t type;
    uint16_t code;
    int32_t value;

    bool operator==(const IOInfo& other) const {
        return type == other.type && code == other.code && value == other.value;
    }
};

struct IOController {
    virtual void execute(const IOInfo& info) = 0;
    virtual void listen(std::function<void(IOInfo input)> callback) = 0;
    virtual void stop_listening() = 0;
};
