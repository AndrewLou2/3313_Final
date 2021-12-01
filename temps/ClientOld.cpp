#include "thread.h"
#include "socket.h"
#include <iostream>
#include <stdlib.h>
#include <time.h>

using namespace Sync;

int main(void)
{

    std::string myString;
    while (true)
    {
        std::cout << "Please input your data" << std::endl;
        std::getline(std::cin, myString);
        if (myString = "done")
        {
            std::cout << "Server shutting down" << std::endl;
            break;
        }

        try
        {
            Socket clientSocket("127.0.0.1", 2000);
            int x = clientSocket.Open();
            ByteArray array(myString);
            int y = clientSocket(array);

            if (myString == "close")
            {
                sleep(50);
                Socket closeSocket("127.0.0.1", 2000);
                closeSocket.Open();

                ByteArray closeArray("Take care!");
                closeSocket.Write(closeArray);
                closeSocket.Close();
                break;
            }

            ByteArray warningArray("Text should be cleared!");
            int z = clientSocket.Read(warningArray);

            std::string returnStr = warningArray.ToString();
            std::cout << returnStr << std::endl;
            std::cout << std::endl;
            D
                clientSocket.Close();
        }
        catch (std::string &s)
        {
            std::cout << "Server is offline" << std::endl;
            break;
        }
    }
}
