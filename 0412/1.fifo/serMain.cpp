#include <unistd.h>
#include "server.h"

int main(int argc, char*argv[]){
    unlink(argv[1]);
    server(argv[1], argv[2]);
    return 0;
}