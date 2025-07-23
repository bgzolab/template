//via:
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <sys/types.h>
#include <sys/wait.h>

int main(){
    int fd[2];
    int pid,line;
    char msg[BUFSIZ];
    //阻塞标志

    int parentFlag = 1;// 1阻塞 2不阻塞
    int childFlag = 1;// 2阻塞 1不阻塞

    printf( "程序开始 \n ");
    if( pipe(fd) < 0 ){
        perror( "建立管道失败:");
    }
    printf( "建立管道成功 \n ");

    pid = fork();
    if( pid < 0){
    perror( "建立进程失败");
    exit( 1);
    } else if(pid == 0){
        printf( "子进程开始 \n ");
        printf( "1子进程写入: \n ");
        while( 1 ){
            if(childFlag== 2){
                childFlag= 1;
                printf( "子进程阻塞,进入父进程 \n\n ");
            } else{
                childFlag++;
            }
            scanf( "%s",msg);

            close(fd[ 0]); //关闭读
            write(fd[ 1],msg, strlen(msg)+ 1); //开始写
            printf( "子进程写入完成 \n\n ");
            if ( strcmp(msg, "EOF") == 0){
                printf( "子进程结束通讯 \n ");
                break;
            }
        } //while

        printf( "子进程结束 \n ");
        _exit( 0);
    } else{
        printf( " \n 父进程开始 \n ");
    while( 1 ){
        if(parentFlag== 1){
            parentFlag++;
            printf( "父进程阻塞,进入子进程 \n\n ");
        }
        if(childFlag== 2) {
            printf( "2子进程写入: \n ");
        } else{
            childFlag= 2;
        }

        close(fd[ 1]); //关闭写
        read(fd[ 0],msg,BUFSIZ); //开始读

        if(parentFlag== 2){
            parentFlag= 1;
            printf( "父进程解除阻塞 \n ");
            printf( "父进程开始读取 \n ");
            printf( "父进程读取:%s \n ",msg);

            if ( strcmp(msg, "EOF") == 0){
                printf( "父进程结束通讯 \n ");
                break;
            }
            printf( "父进程读取完成 \n\n ");
        }
    } //while
    wait( NULL); //等待子进程执行完
    printf( "父进程结束 \n ");
    }
    printf( "程序结束 \n ");
    return 0;
}
