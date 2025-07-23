#include "threadguard.h"

ThreadGuard::~ThreadGuard() {
    if (t_.joinable()) {
        t_.join();
    }
}
