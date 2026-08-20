#pragma once

#include <cstdint>

struct IOInfo {
    uint16_t type;
    uint16_t code;
    int32_t value;
};

struct IOController {
    virtual void execute(const IOInfo& info) = 0;
};
