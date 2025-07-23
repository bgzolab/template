#include <stdlib.h>
#include <thread>

#include "threadguard.h"
#include "narc.h"

int main(int argc, char* argv[]){
    int n = atoi (argv[1]);

    Narcissistic pf(n);
    std::thread t(pf);
    ThreadGuard tg(std::move(t));

    return 0;
}
