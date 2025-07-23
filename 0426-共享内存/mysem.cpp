
#include <sys/types.h>
#include <sys/ipc.h>
#include <sys/sem.h>

#include "mysem.h"

void sem_init(const int semid, const int num, const int val){
    semum su;
    su.val = val;
    semctl(semid, num, SETVAL, su);
}
void sem_p(const int semid, const int num){
    struct sembuf sb;
    sb.sem_num=num;     //*
    sb.sem_op=-1;       //*
    sb.sem_flg=SEM_UNDO;//进程关闭之后没有对信号量做处理, 自动恢复
    semop(semid, &sb, 1);
}

void sem_v(const int semid, const int num){
    struct sembuf sb;
    sb.sem_num=num;     //*
    sb.sem_op=1;       //*
    sb.sem_flg=SEM_UNDO;//进程关闭之后没有对信号量做处理, 自动恢复
    semop(semid, &sb, 1);

}
