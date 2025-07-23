GCC=g++
CFLAG=-c
OFLAG=-o
SEXE=serMain
SOBJ=serMain.o server.o mysem.o mysig.o
CEXE=cliMain
COBJ=cliMain.o client.o mysem.o message.o

all:${SEXE} ${CEXE}
${SEXE}:${SOBJ}
	${GCC} ${OFLAG} $@ $^

${CEXE}:${COBJ}
	${GCC} ${OFLAG} $@ $^

%.o:%.cpp
	${GCC} ${CFLAG} $^

clean:
	rm *.o
