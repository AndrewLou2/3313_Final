
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
	std::string input;
	ByteArray data;
	try
	{
		socket.Open(); //open the socket
		while (true)
		{
			std::cout << "Enter a string, or done to terminate the client, or close to shutdown the server." << std::endl;
			getline(std::cin, input);

			data = *new ByteArray(input);
			if (input == "done" || input == "close")
			{
				socket.Write(data);
				std::cout << "Client closed." << std::endl;
				break;
			}
			else
			{
				socket.Write(data);
				socket.Read(data);
				if (data.ToString() == "close" || data.ToString() == "") //if Close recieved or an empty string, server is closed
				{
					std::cout << "Server Closed... Terminating Client" << std::endl;
					break; //shutdown if sent Close
				}

				std::cout << data.ToString() << std::endl;
			}
		}
		socket.Close();
	}
	catch (...)
	{ //Server not open, send error msg
		std::string errorMsg = "Server is not open... terminating Client";
		std::cout << errorMsg << std::endl;
	}
	return 0;
};