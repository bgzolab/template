#include <stdlib.h>
#include <iostream>
#include <thread>
#include <atomic>
#include <mutex>

#include "tickets.h"


int main(int argc, char * argv[]){
    int total = atoi(argv[1]),
        back = atoi(argv[2]),
        tickets = total;

    std::thread w1(sellref, std::ref(tickets), total);
    std::thread w2(sellref, std::ref(tickets), total);  // 传引用
    std::thread w3(sellref, std::ref(tickets), total);
    std::thread w4(refund, std::ref(tickets), back);

    w1.join();
    w2.join();
    w3.join();
    w4.join();

    std::cout<<tickets<<std::endl;
    return 0;
}