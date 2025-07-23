#include <iostream>
#include <thread>


class ThreadGuard{
    std::thread t_;
public:
    ThreadGuard (std::thread t):t_(std::move(t)){};
    ~ThreadGuard ();
    ThreadGuard(ThreadGuard&) = delete;
    ThreadGuard operator =(ThreadGuard&)= delete;
};