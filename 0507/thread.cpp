#include <iostream>
#include <thread>
#include <stdlib.h>

class ThreadGuard{ 
    std::thread t_;
public:
    ThreadGuard (std::thread t):t_(std::move(t)){}
    ~ThreadGuard (){ // 析构一定会被调用
        if(t_.joinable()){
            t_.join();
        }
    }
    ThreadGuard(ThreadGuard&) = delete;
    ThreadGuard operator =(ThreadGuard&)= delete;
};

class Perfect{
    int n;
    int factorSum(int n){
        int sum=0;
        for(int i=1; i<n; i++){
            if(n%i==0) sum +=i;
        }
        return sum;
    }
public:
    Perfect(int n):n(n){}
    void operator()(){
        if(factorSum(n) == n){
            std:: cout<< "yes\n";
        }else{
            std:: cout<< "no\n";
        }
    }

};



// void isPerfect (const int n){ //thread function can not return type
// }

int main(int argc, char* argv[]){
    int n = atoi (argv[1]);
    // std::cout << (isPerfect(n)? "Yes\n" : "No\n") <<std::endl;
    // std::thread t(isPerfect, n);
    //t 线程对象 管理
    //function 真正的线程, 后面跟参数
    Perfect pf(n);
    std::thread t(pf);
    ThreadGuard tg(std::move(t)); //t对应的线程移动到 t -> t_

    //t.join();
    return 0;
}
