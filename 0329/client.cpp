#include"client.h"
#include <string.h>
#include <stdio.h>
#include <unistd.h>

#define MAXLINE 4096

void client(int readfd,int writefd){
    size_t len;
    char buf[MAXLINE];
    fgets(buf,MAXLINE,stdin);
    len = strlen(buf);
    if(buf[len-1] == '\n')
          --len;
    write(writefd,buf,len);
    while( (len = read(readfd,buf,MAXLINE)) > 0)
          write(STDOUT_FILENO,buf,len);
}