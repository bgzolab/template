lineApp: main.o line.o dot.o
	cc -o lineApp main.o line.o dot.o

main.o: main.cpp
	cc -c main.cpp

line.o: line.cpp
	cc -c line.cpp

dot.o: dot.cpp
	cc -c dot.cpp

