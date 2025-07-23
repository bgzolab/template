#include <unistd.h>
#include <stdio.h>
#include <fcntl.h>
#include <string.h>
#include <stdlib.h>
#include <error.h>
#include <sys/types.h>
#include <sys/wait.h>

#include "client.h"
#include "server.h"

int main(){
    int fd1[2], fd2[2];

    pipe(fd1);
    pipe(fd2);

    int pid = fork();

    if(pid < 0){
        fprintf(stderr,"fork error\n");
        exit(-1);
    }else if(pid == 0){
        //子进程
        close(fd1[1]);
        close(fd2[0]);
        server(fd1[0],fd2[1]);

    }else{
        //父进程
        close(fd1[0]);
        close(fd2[1]);
        client(fd2[0],fd1[1]);

        waitpid(pid,NULL,0);

    }

    exit(0);
}
