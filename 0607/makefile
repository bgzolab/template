GCC=g++
CFLAG=-c
OFLAG=-o
SLIB=-pthread
SEXE=serMain
SOBJ=serMain.o server.o 
# message.o
CEXE=cliMain
COBJ=cliMain.o client.o 
# message.o

all:${SEXE} ${CEXE}
${SEXE}:${SOBJ}
	${GCC} ${OFLAG} $@ $^ ${SLIB}

${CEXE}:${COBJ}
	${GCC} ${OFLAG} $@ $^

%.o:%.cpp
	${GCC} ${CFLAG} $^

clean:
	rm *.o
	rm ${SEXE} ${CEXE}
