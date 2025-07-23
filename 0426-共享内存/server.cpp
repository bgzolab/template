#include <iostream>
#include <sys/types.h>
#include <sys/ipc.h>
#include <sys/sem.h>
#include <sys/shm.h>
#include <sys/signal.h>

#include "server.h"
#include "message.h"
#include "mysem.h"
#include "mysig.h"

extern bool flag;

const int PROJID = 10;
const int SHMSIZ = 4096;
const int SEMSIZ = 2;
const int SMUTEX = 0; //第一个信号量
const int CMUTEX = 1; //第一个信号量

void han_mes(Message* pm){
    switch(pm->op){
        case 0:
            pm->res = pm->oprand1+pm->oprand2;
            break;
        case 1:
            pm->res = pm->oprand1-pm->oprand2;
            break;
        case 2:
            pm->res = pm->oprand1*pm->oprand2;
            break;
        case 3:
            if(pm->oprand2==0){
                pm->res = 0;
                pm->status = 'E';
                break;
            }
            pm->res = pm->oprand1/pm->oprand2;
            break;
        default:
            break;
    }
}

void process(Message* pm, const int semid){
    signal(SIGINT, han_int);
    while(flag){
        sem_p(semid, SMUTEX); //0-1 无法执行, 只能等待
        han_mes(pm);
        sem_v(semid, CMUTEX);
    }
}

void server (const char* shmname, const char* semname){
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
        sem_init(semid, SMUTEX, 0); 
        sem_init(semid, CMUTEX, 0);
        process(pm, semid);
        shmdt(pm);
    }while(0);

    shmctl(shmid, IPC_RMID, NULL);
    semctl(semid, 0, IPC_RMID);
}
