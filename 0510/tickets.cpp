#include <stdlib.h>
#include <iostream>
#include <thread>
#include <atomic>
#include <mutex>

std::mutex tmutex;

// void sell(std::atomic<int> *tickets, int num){
//     for(int i = 0; i < num; i++){
//         *tickets = *tickets - 1;
//         // std::cout << "Selling ticket...\n";
// }

// void sellref(std::atomic<int> &tickets, int num){
//     for(int i = 0; i < num; i++){
//         if(ticket == 0){
//             std::cout << "Sold Out " << i << " Tickets\n";
//             break;
//         }
//         tickets--;
//     }
// }

// void refund(std::atomic<int> &tickets, int num){
//     for(int i = 0; i < num; i++){
//         tickets++;
//     }
// }

// void sell(int *tickets, int num){
//     for(int i = 0; i < num; i++){
//         // tmutex.lock();
//         std::lock_guard<std::mutex> lg(tmutex);
//         *tickets = *tickets - 1;
//         // std::cout << "Selling ticket...\n";
//         // tmutex.unlock();
//     }
// }

void sellref(int& tickets, int num){
    for(int i = 0; i < num; i++){
        // tmutex.lock();
        // std::lock_guard<std::mutex> guard(tmutex);
        std::lock_guard<std::mutex> lg(tmutex);

        if(tickets == 0){
            std::cout << "Sold Out " << i << " Tickets\n";
            // tmutex.unlock();
            break;
        }
        tickets--;
        // tmutex.unlock();
    }
}

void refund(int& tickets, int num){
    for(int i = 0; i < num; i++){
        std::lock_guard<std::mutex> lg(tmutex);
        // tmutex.lock();
        tickets++;
        // tmutex.unlock();
    }
}

int main(int argc, char * argv[]){
    int total = atoi(argv[1]),
        back = atoi(argv[2]),
        tickets = total;
    // std::atomic<int> tickets(total);


    // std::thread w1(sell, &tickets, total);              // 传指针
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