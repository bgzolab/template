#include <stdlib.h>
#include "server.h"

int main(int argc, char* argv[]){
    server(argv[1], atol(argv[2]));
    return 0;
}
