#include <unistd.h>
#include "client.h"

int main(int argc, char* argv[]){
    unlink(argv[2]);
    client(argv[1], argv[2]);
    return 0;
}
