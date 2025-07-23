#include <stdlib.h>
#include <thread>

#include "threadguard.h"
#include "amic.h"

int main(int argc, char* argv[]){
    int n = atoi (argv[1]);
    int m = atoi (argv[2]);

    Amicable pf(n, m);
    std::thread t(pf);
    ThreadGuard tg(std::move(t));

    return 0;
}
