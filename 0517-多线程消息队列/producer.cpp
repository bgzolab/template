#include <string.h>
#include "producer.h"
#include "message.h"

void producer(MQ& mq){
    while(true){
        Message msg;
        memset(&msg, 0, sizeof(Message));
        std::cout << "plz enter expression: ";
        if(std::cin.eof()) break; //*****
        std::cin >> msg;
        mq.put(msg);
    }
}