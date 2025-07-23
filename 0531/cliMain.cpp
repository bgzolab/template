#include <stdlib.h>

#include "client.h"
int main(int argc, char*argv[]){
    client (argv[1], atoi(argv[2]));
    return 0;
}