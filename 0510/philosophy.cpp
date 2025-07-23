#include<iostream>
#include<thread>
#include<mutex>

//via: https://www.cnblogs.com/pigdragon/p/6951475.html
const int NUM_THREADS = 5;

std::mutex chopstick[NUM_THREADS];

void philosopher(int id){
    while(true){

        int left = id;
        int right = (id + 1) % NUM_THREADS;

        std::this_thread::sleep_for(std::chrono::milliseconds(1000));
        std::cout<<"Philosopher "<<id<<" is thinking\n";

        if (try_lock(chopstick[left], chopstick[right]) == -1){
            //via: https://stackoverflow.com/questions/4362459/check-to-see-if-a-pthread-mutex-is-locked-or-unlocked-after-a-thread-has-locked & http://www.cplusplus.com/reference/mutex/try_lock/
            std::cout<<"Philosopher "<<id<<" is eating\n";
        }else{
            chopstick[left].lock();
            chopstick[right].lock();
            continue;
        }

        chopstick[left].unlock();
        chopstick[right].unlock();

        std::cout<<"Philosopher "<<id<<" is putting down chopstick\n";
    }
}


int main(int argc, char * argv[]){

    std::thread philosophers[NUM_THREADS];

    for(int i = 0; i < NUM_THREADS; i++){
        philosophers[i] = std::thread(philosopher, i);
    }

    for(int i = 0; i < NUM_THREADS; i++){
        philosophers[i].join();
    }

    return 0;
}