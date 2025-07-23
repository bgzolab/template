#include<iostream>
#include <stdlib.h>
#include <thread>
#include <atomic>
#include <mutex>

std::mutex tmutex;

struct Account{
    int balance;
    std::string aid;
    // Account():balance(0){}
    Account(std::string id, int balance):aid(id), balance(balance){}
};

std::ostream& operator <<(std::ostream& os, const Account& acc){
    os << "Balance: " << acc.balance << " Account ID: " << acc.aid;
    return os;
}

void withdraw(Account& acc, int amount){
    std::lock_guard<std::mutex> lg(tmutex);
    if(acc.balance < amount){
        std::cout << "Insufficient Funds\n";
        return;
    }
    acc.balance -= amount;
    std::cout << "Withdrawal Successful"<<acc<<"\n";
}


void deposit(Account& acc, int amount){
    std::lock_guard<std::mutex> lg(tmutex);
    acc.balance += amount;
    std::cout << "Deposit Successful "<<acc<<" \n";
}

int main(int argc, char* argv[]){
    Account account("100001", 50000);
    std::thread t1(withdraw, std::ref(account), 60000);
    std::thread t2(withdraw, std::ref(account), 30000);
    std::thread t3(deposit, std::ref(account), 10000);
    std::thread t4(deposit, std::ref(account), 5000);

    t1.join();
    t2.join();
    t3.join();
    t4.join();

    std::cout<<account<<std::endl;
}
