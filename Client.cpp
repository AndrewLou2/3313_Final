
#include "thread.h"
#include "socket.h"
#include <iostream>
#include <stdlib.h>
#include <time.h>

using namespace Sync;

int main(void)
{
	// Welcome the user 
	std::cout << "SE3313 Lab 3 Client" << std::endl;

	// Create our socket
	Socket socket("127.0.0.1", 3000);
	//To write to socket and read from socket. You may use ByteArray 
	//socket.Write(data);
	//socket.Read(data);

	socket.Close();

	return 0;
}
