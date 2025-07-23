mypipes: mypipes.o client.o server.o
	g++ -o mypipes mypipes.o client.o server.o
mypipes.o:  mypipes.cpp
	g++ -c mypipes.cpp
client.o: client.cpp
	g++ -c client.cpp
server.o: server.cpp
	g++ -c server.cpp
clean:
	rm *.o
	rm mypipes