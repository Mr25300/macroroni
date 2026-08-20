#if defined(__linux__)

#pragma once

#include "io.hpp"

#include <fcntl.h>
#include <unistd.h>
#include <linux/uinput.h>

struct LinuxIOController : IOController {
    void execute(const IOInfo& info) {
        return;
    }
};

#endif
