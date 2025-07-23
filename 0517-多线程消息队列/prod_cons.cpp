#include <thread>
#include "mq.h"
#include "producer.h"
#include "consumer.h"

int main(int argc, char* argv[]){
    MQ mq;
    std::thread p(producer, std::ref(mq));
    std::thread c(consumer, std::ref(mq));
    p.join();
    c.join();
    return 0;
}


    // // Create a producer and consumer thread
    // pthread_t producer, consumer;

    // // Create a message queue
    // int msgqid = msgget(IPC_PRIVATE, IPC_CREAT | 0666);

    // // Create a message
    // Message msg;

    // // Create a producer thread
    // pthread_create(&producer, NULL, producer_thread, (void*)&msgqid);

    // // Create a consumer thread
    // pthread_create(&consumer, NULL, consumer_thread, (void*)&msgqid);

    // // Wait for the producer thread to finish
    // pthread_join(producer, NULL);

    // // Wait for the consumer thread to finish
    // pthread_join(consumer, NULL);

    // // Remove the message queue
    // msgctl(msgqid, IPC_RMID, NULL);

    // return 0;