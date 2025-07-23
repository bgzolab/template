#ifndef XY_MQ
#define XY_MQ
//#pragma once


#include <queue>
#include <mutex>
#include <condition_variable>
#include "message.h"

const int maxSize = 4;

class MQ{
    std::queue<Message> q;
    std::mutex mu;
    std::condition_variable non_empty, non_full; //cv;
public:
    void put(Message m);
    Message get();
};

#endif
