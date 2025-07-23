#include <iostream>
#include <sys/types.h>
#include <sys/stat.h>
#include <fcntl.h>
#include <unistd.h>
#include <string.h>
#include "client.h"
#include "message.h"

void process(const int rfd, const int wfd){
    while(true){
        Message m;
        memset(&m, 0, sizeof(m));
        std::cin>>m;
        if(std::cin.eof()) break;
        // m.status="S";
        write(wfd, &m, sizeof(m));
        read(rfd, &m, sizeof(m));
        std::cout<<m<<std::endl;
    }
}

void client(const char* ser, const char* cli){
    int wfd, rfd;
    do{
        if(mkfifo(cli, 0664) == -1){
            std::cerr<<"mkfifo wrong\n";
            break;
        }
        wfd = open(ser, O_WRONLY);
        if(wfd==-1){
            std::cout<<"open error"<<std::endl;
            break;
        }
        rfd = open(cli, O_RDONLY);
        if(rfd==-1){
            std::cout<<"open error"<<std::endl;
            break;
        }
        process(rfd, wfd);
    }while(0);
    close(wfd);
}
