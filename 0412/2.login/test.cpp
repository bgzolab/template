#include <iostream>
#include <sys/types.h>
#include <sys/stat.h>
#include <fcntl.h>
#include <unistd.h>
#include <string.h>
int main() {
    char buffer[80];
    int fd;
    std::string tmp="myfifo";
    const char* FIFO = tmp.c_str();
    unlink(FIFO);
    if(mkfifo(FIFO, 0666) == -1){
        std::cout<<"error";
    }
    // printf("%d\n");
    if(fork() > 0){
        char s[] = "hello!\n";
        fd = open(FIFO, O_WRONLY);
        write(fd, s, sizeof(s));
        close(fd);
    } else {
        fd = open(FIFO, O_RDONLY);
        read(fd, buffer, 80);
        printf("%s", buffer);
        close(fd);
    }
}