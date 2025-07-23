#include <iostream>
#include <sys/types.h>
#include <sys/ipc.h>
#include <sys/sem.h>
#include <sys/shm.h>
#include "client.h"
#include "message.h"
#include "mysem.h"

const int PROJID = 10;
const int SHMSIZ = 4096;
const int SEMSIZ = 2;
const int SMUTEX = 0; //第一个信号量
const int CMUTEX = 1; //第一个信号量

void process(Message* pm, int semid){
    while(true){
        std::cin >> (*pm);
        if(std::cin.eof()) break;
        pm->status='S';
        sem_v(semid, SMUTEX);
        sem_p(semid, CMUTEX);
        std::cout<<(*pm)<<std::endl;
    }
}

void client(const char* shmname, const char* semname){
    int shmid, semid;
    do{
        key_t shmkey = ftok(shmname, PROJID);
        if(shmkey == -1){
            std::cerr<<"ftok shmname wrong.\n";
            break;
        }
        key_t semkey = ftok(semname, PROJID);
        if(semkey == -1){
            std::cerr<<"ftok semname wrong.\n";
            break;
        }
        shmid = shmget(shmkey, SHMSIZ, IPC_CREAT | 0664);
        
        if(shmid == -1){
            std::cerr<<"shmget wrong.\n";
            break;
        }//生成物理内存, 还未连接到进程
        semid = semget(semkey, SEMSIZ, IPC_CREAT | 0664);
        if(semid == -1){
            std::cerr<<"shmget wrong.\n";
            break;
        }//创建信号量集
        Message* pm= (Message*)shmat(shmid, NULL, 0);
        process(pm, semid);
    }while(0);
}
