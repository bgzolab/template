
#include <iostream>
#include <sys/types.h>
#include <sys/stat.h>
#include <fcntl.h>
#include <unistd.h>
#include <string.h>
#include "server.h"
#include "message.h"

char _NAME[] = "admin";
char _PASSWD[] = "admin";

void handle_mes(Message& m){
	if( strcmp(_NAME, m.name)==0){
		if(strcmp(_PASSWD, m.passwd)==0){
			m.status= 1;
		}else{
			m.status= 2;
		}
		
	}else{
		m.status = 3;
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
