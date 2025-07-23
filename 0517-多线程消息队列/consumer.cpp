#include <fstream>

#include "consumer.h"
#include "message.h"

void process(Message &m){
    switch(m.op){
        case 0:
            m.res = m.oprand1 + m.oprand2;
            break;
        case 1:
            m.res = m.oprand1 - m.oprand2;
            break;
        case 2:
            m.res = m.oprand1 * m.oprand2;
            break;
        case 3:
            if(m.oprand2==0){
                m.res = 0;
                m.status = 'E';
                break;
            }
            m.res = m.oprand1 / m.oprand2;
            break;
        default: 
            break;
    }
    std::ofstream fout("log.txt", std::ios_base::app); // via: https://stackoverflow.com/questions/26084885/appending-to-a-file-with-ofstream
    fout<<m<<std::endl;
    fout.close();
}

void consumer(MQ& mq){
    while(true){
        Message msg = mq.get();
        process(msg);
    }
}