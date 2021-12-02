#include "thread.h"
#include "socketserver.h"
#include <algorithm>
#include <stdlib.h>
#include <time.h>
#include "Semaphore.h"
#include <list>
#include <vector>
#include <thread>

using namespace Sync;

class SocketThread : public Thread
{
private:
	//declaration of variables
	Socket &socket;

	ByteArray data;

	bool &terminate;

	int roomNum;

	int portNum;

	std::vector<SocketThread *> &socketThreadsHolder;

public:
	//constuctor
	SocketThread(Socket &socket, std::vector<SocketThread *> &clientSockThr, bool &terminate, int portNum) : socket(socket), socketThreadsHolder(clientSockThr), terminate(terminate), portNum(portNum)
	{
	}

	~SocketThread()
	{
		this->terminationEvent.Wait();
	}

	//getters methods
	Socket &GetSocket()
	{
		return socket;
	}

	const int GetChatRoom()
	{
		return roomNum;
	}

	virtual long ThreadMain()
	{
		// portNum[int] parse to -> portNum[String]
		std::string stringPort = std::to_string(portNum);

		// generating semaphores based off port number
		Semaphore clientBlock(stringPort);

		try
		{
			// Gathers bytestream data.
			socket.Read(data);

			std::string chatRoomString = data.ToString();
			chatRoomString = chatRoomString.substr(1, chatRoomString.size() - 1);
			roomNum = std::stoi(chatRoomString);
			std::cout << "Current number of chat rooms: " << roomNum << std::endl;

			while (!terminate)
			{
				int socketResult = socket.Read(data);
				// terminate when sockets are closed on the client side
				if (socketResult == 0)
					break;

				std::string recv = data.ToString();
				if (recv == "shutdown\n")
				{

					clientBlock.Wait();

					// Iterate to select and erase this socket thread
					socketThreadsHolder.erase(std::remove(socketThreadsHolder.begin(), socketThreadsHolder.end(), this), socketThreadsHolder.end());

					clientBlock.Signal();

					std::cout << "A client is shutting off from the server" << std::endl;
					break;
				}

				// A forward slash is used as the first character to change the chat room number
				if (recv[0] == '/')
				{
					// Split string
					std::string stringChat = recv.substr(1, recv.size() - 1);

					// parse the integer for the chat room nums
					roomNum = std::stoi(stringChat);
					std::cout << "A client just joined a room!" << roomNum << std::endl;
					continue;
				}

				// Calls the semaphore blocking call so the threads can enter
				clientBlock.Wait();
				for (int i = 0; i < socketThreadsHolder.size(); i++)
				{
					SocketThread *clientSocketThread = socketThreadsHolder[i];
					if (clientSocketThread->GetChatRoom() == roomNum)
					{
						Socket &clientSocket = clientSocketThread->GetSocket();
						ByteArray sendBa(recv);
						clientSocket.Write(sendBa);
					}
				}
				// Exit critical section.
				clientBlock.Signal();
			}
		}
		// Catch string-thrown exceptions
		catch (std::string &s)
		{
			std::cout << s << std::endl;
		}
		// Catch thrown exceptions
		catch (std::exception &e)
		{
			//Output exception to console
			std::cout << "A client forcefully exited their chat app!" << std::endl;
		}
		std::cout << "A client has left!" << std::endl;
		return 0;
	}
};

class ServerThread : public Thread
{
private:
	//Declaration of variables
	SocketServer &server;

	std::vector<SocketThread *> socketThrHolder;

	int portNum;

	int roomNum;

	bool terminate = false;

public:
	ServerThread(SocketServer &server, int roomNum, int portNum)
		: server(server), roomNum(roomNum), portNum(portNum)
	{
	}

	~ServerThread()
	{

		// Close the client sockets.
		for (auto thread : socketThrHolder)
		{
			try
			{
				// Close the socket.
				Socket &toClose = thread->GetSocket();
				toClose.Close();
			}
			//Catching all exceptions
			catch (...)
			{
			}
		}
		std::vector<SocketThread *>().swap(socketThrHolder);
		terminate = true;
	}

	virtual long ThreadMain()
	{
		while (true)
		{
			try
			{
				// portNum[int] parse to -> portNum[String]
				std::string stringPortNum = std::to_string(port);

				// Generating semaphores based off port number
				Semaphore serverBlock(stringPortNum, 1, true);

				// Sends the number of clients to front-end
				std::string allChats = std::to_string(roomNum) + '\n';

				// Byte array conversion
				ByteArray allChats_conv(allChats);

				// Waits for front-end connection
				Socket sock = server.Accept();

				// Sends the number of chats.
				sock.Write(allChats_conv);
				Socket *newConnection = new Socket(sock);

				Socket &socketReference = *newConnection;
				socketThrHolder.push_back(new SocketThread(socketReference, std::ref(socketThrHolder), terminate, portNum));
			}
			// Catch string-thrown exception
			catch (std::string error)
			{
				std::cout << "ERROR: " << error << std::endl;
				// Exit thread
				return 1;
			}
			// Catch unexpected shutdown
			catch (TerminationException terminationException)
			{
				std::cout << "Server has shut down!" << std::endl;
				// Exit with exception thrown.
				return terminationException;
			}
		}
	}
};

int main(void)
{
	// VM Port
	int portNum = 1236;

	// Declaration of the number of rooms for the chatroom
	int roomNum = 6;

	std::cout << "3313 Final Server" << std::endl
			  << "Type done to exit the server gracefully" << std::endl;

	// Creating server
	SocketServer server(portNum);

	// Creating server threads
	ServerThread st(server, roomNum, portNum);

	// Wait for user input
	FlexWait cinWaiter(1, stdin);
	cinWaiter.Wait();
	std::cin.get();

	// Shut down and clean up the server
	server.Shutdown();

	std::cout << "Bye-bye!" << std::endl;
}