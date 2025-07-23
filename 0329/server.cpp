#include "server.h"
#include <string.h>
#include <stdio.h>
#include <unistd.h>
#include <stdlib.h>
#include <cerrno>
#include <sys/types.h>
#include <sys/stat.h>
#include <fcntl.h>

#define MAXLINE 4096

void server(int readfd,int writefd){
    char buf[MAXLINE];
    ssize_t n = read(readfd,buf,MAXLINE);
    if(n ==0){
        fprintf(stderr,"error\n");
        exit(-1);
    }
    buf[n] = '\0';
    int fd = open(buf,O_RDONLY);
    if(fd < 0){
        snprintf(buf+n,sizeof(buf)-n,"can't open: %s\n",strerror(errno));
        n = strlen(buf);
        write(writefd,buf,n);
    } else {
        while( (n = read(fd,buf,MAXLINE)) > 0)
            write(writefd,buf,n);
    }
    close(fd);
}