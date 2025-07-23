#include <iostream>
#include <sys/types.h>
#include <sys/ipc.h>
#include <sys/sem.h>
#include <sys/shm.h>
#include <sys/signal.h>
#include <unordered_map>
#include <stdio.h>
#include <string.h>

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
std::unordered_map<std::string, std::string> umap; // compaare name & passwd

void han_mes(Message* pm){
    if( umap.find( std::string(pm->name) ) == umap.end()){
        pm->status = 'N';
        return;
    }
    if( umap[std::string(pm->name)] == std::string(pm->passwd))
        pm->status = 'O';
     else
        pm->status = 'P';

}

void process(Message* pm, const int semid){
    signal(SIGINT, han_int);
    while(flag){
        sem_p(semid, SMUTEX); //0-1 无法执行, 只能等待
        han_mes(pm);
        sem_v(semid, CMUTEX);
    }
}

void load_config(){
    FILE *fp;
    char line[40];
    char *p;
    int i=0;
    fp=fopen("./config","r");
    if(fp==NULL){
        printf("open config.txt failed\n");
        exit(1);
    }
    while(fgets(line,40,fp)!=NULL){
        std::string name, passwd;
        p=strtok(line,",");
        name = p;
        p=strtok(NULL,",");
        passwd = p;
        passwd = p[strlen(p)-1]=='\n' ? passwd.substr(0,passwd.size()-1) : passwd;
        umap[name] = passwd;
        i++;
    }
    fclose(fp);
}

void server (const char* shmname, const char* semname){
    load_config();
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
