
#include <iostream>
#include <sys/types.h>
#include <sys/stat.h>
#include <fcntl.h>
#include <unistd.h>
#include <string.h>
#include "server.h"
#include "message.h"

void handle_mes(Message& m){
    switch(m.op){
        case '+':
            m.res = m.oprand1 + m.oprand2;
            break;
        case '-':
            m.res = m.oprand1 - m.oprand2;
            break;
        case '*':
            m.res = m.oprand1 * m.oprand2;
            break;
        case '/':
            if(m.oprand2 == 0) break; 
            m.res = m.oprand1 / m.oprand2;
            break;
        default:
            break;
    }
}


void process(const int rfd, const int wfd){
    while(true){
        Message m;
        memset(&m, 0, sizeof(m));
        int len = read(rfd, &m, sizeof(m));
        if(len<=0){
            std::cerr<<"cient close\n";
            break;
        }
        handle_mes(m);
        write(wfd, &m, sizeof(m));
    }
}

void server(const char* ser, const char*cli){
    int rfd, wfd;
    do{
        if(mkfifo(ser,0644) == -1){
            std::cerr<<"mkfifo ser wrong\n";
            break;
        }
        rfd = open(ser, O_RDONLY);
        if(rfd == -1){
            std::cerr<<"open wrong\n";
            break;
        }
        int wfd = open(cli, O_WRONLY);
        if(wfd == -1){
            std::cerr<<"open wrong\n";
            break;
        }
        process(rfd, wfd); 
    }while(0);
    
    close(rfd);
}
