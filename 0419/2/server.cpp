#include <iostream>
#include <sys/ipc.h>
#include <sys/msg.h>
#include <string.h>
#include <sys/types.h>
#include <unistd.h>
#include <unordered_map>
#include <stdio.h>
#include <string.h>

#include "message.h"
#include "server.h"

const int PROID=100;
std::unordered_map<std::string, std::string> umap; // compaare name & passwd

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

void han_mes(Message &m){
    if( umap.find( std::string(m.name) ) == umap.end()){
        m.status = 'N';
        return;
    }
    if( umap[std::string(m.name)] == std::string(m.passwd))
        m.status = 'O';
     else
        m.status = 'P';
    // std::cout<<umap[std::string(m.name)];
    // std::cout<<m.passwd<<std::endl;
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
    load_config();
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