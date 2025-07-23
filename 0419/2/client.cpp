#include <iostream>
#include <sys/ipc.h>
#include <sys/msg.h>
#include <string.h>
#include <sys/types.h>
#include <unistd.h>

#include "message.h"
#include "client.h"

const int PROID=100;

void process(const int msgid, const long msgtype){
    while(true){
        Message m;
        memset(&m, 0 ,sizeof(m));
        std::cin>>m;
        if(std::cin.eof()) break;
        m.status = 'S';
        m.mtype = msgtype;
        long rtype = getpid();
        m.rtype = rtype;
        msgsnd(msgid, &m, sizeof(m)-sizeof(long), 0);
        msgrcv(msgid, &m, sizeof(m)-sizeof(long), rtype, 0);
        std::cout << m << std::endl;
    }
}
void client(const char* msgname, const long msgtype){
    int msgid;
    do{
        key_t msgkey = ftok(msgname, PROID);
        if(msgkey==-1){
            std::cerr<<"ftok error"<<std::endl;
            break;
        }
        msgid = msgget(msgkey, IPC_CREAT|0644);
        if(msgkey==-1){
            std::cerr<<"megget error"<<std::endl;
            break;
        }
        process(msgid, msgtype);
    }while(0);
}