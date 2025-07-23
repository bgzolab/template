#include "mq.h"

void MQ::put(Message m){
    // std::lock_guard<std::mutex> lk(mu);
    // q.push(m);
    // non_empty.notify_one();
    std::unique_lock<std::mutex> lk(mu);
    non_full.wait(lk, [this]{return q.size() < maxSize;});
    q.push(m);
    non_empty.notify_one();
}

Message MQ::get(){
    std::unique_lock<std::mutex> ul(mu);
    non_empty.wait(ul, [this]{return !q.empty();});
    Message m = q.front();
    q.pop();
    return m;
}