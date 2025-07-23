#include "tickets.h"
#include <stdlib.h>
#include <iostream>
#include <thread>
#include <atomic>
#include <mutex>

std::mutex tmutex;

void sellref(int& tickets, int num){
    for(int i = 0; i < num; i++){
        if(tickets == 0){
            std::cout << "Sold Out " << i << " Tickets\n";
            break;
        }
        tickets--;
    }
}

void refund(int& tickets, int num){
    for(int i = 0; i < num; i++){
        std::lock_guard<std::mutex> lg(tmutex);
        tickets++;
    }
}