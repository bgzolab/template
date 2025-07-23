#include <iostream>
#include <sys/ipc.h>
#include <sys/msg.h>
#include <string.h>
#include <sys/types.h>
#include <unistd.h>

#include "message.h"
#include "server.h"

const int PROID=100;

void han_mes(Message &m){
    switch(m.op){
        case 0:
            m.res = m.oprand1 + m.oprand2;
            break;
        case 1:
            m.res = m.oprand1 - m.oprand2;
            break;
        case 2:
            m.res = m.oprand1 * m.oprand2;
            break;
        case 3:
            if(m.oprand2==0){
                m.res = 0;
                m.status = 'E';
                break;
            }
            m.res = m.oprand1 / m.oprand2;
            break;
        default:
            break;
    }
}

void process(const int msgid, const long msgtype){
    while(true){
        Message m;
        memset(&m, 0 ,sizeof(m));
        msgrcv(msgid, &m, sizeof(m)-sizeof(long), msgtype, 0);
        long rtype = m.rtype; //知道是哪个客户端发过来的.
        han_mes(m);
        m.mtype = rtype;
        msgsnd(msgid, &m, sizeof(m)-sizeof(long), 0);
    }
}
void server(const char* msgname, const long msgtype){
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