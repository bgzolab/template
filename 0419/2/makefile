GCC=g++
CFLAG=-c
OFLAG=-o

SEXE=serMain
SOBJ=serMain.o server.o

CEXE=cliMain
COBJ=cliMain.o client.o message.o

all:${SEXE} ${CEXE}
${SEXE}:${SOBJ}
	${GCC} ${OFLAG} $@ $^

${CEXE}:${COBJ}
	${GCC} ${OFLAG} $@ $^

%.o:%.cpp
	${GCC} ${CFLAG} $^

clean:
	rm *.o