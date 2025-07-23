GCC=g++
CFLAG=-c
OFLAG=-o
LIB=-pthread

EXE=prod_cons
OBJ=prod_cons.o producer.o consumer.o mq.o message.o

# all:${EXE}
${EXE}:${OBJ}
	${GCC} ${OFLAG} $@ $^ ${LIB}

%.o:%.cpp
	${GCC} ${CFLAG} $^

clean:
	rm *.o