OS Chat Room App 💻
===
```OS Chat Room App``` is a multi-user multi-transaction application. the server can be hosted on a UNIX/LINUX environment while the client can be on a different environment such as Windows OS. This application implements concepts of thread synchronization (semaphores), multithreading and socket programming. Multiple users can connect to one of many chat rooms created by the server after launching a python application.
![Chat-Preview](https://cdn.discordapp.com/attachments/868924230102818896/916048859174699048/unknown.png)

---
 ## 🌴 Quick Start
 note: server can be hosted on a UNIX/LINUX environment
 
 **Server-side (Ubuntu 11.1.0):**
  Port-forward VM with the settings:
  ```
  Protocol: TCP
  Host IP: 127.0.0.1
  Host Port: 1236
  Guest IP: 
  Guest Port: 1236
  ```
  Install **gcc** complier using :
 ```$ sudo apt install g++ ```
 Clone the repository using :
 ```$ git clone https://github.com/AndrewLou2/OS-chatroom-app.git```
 Compile objects and executable files by using:
 ```$ make```
 Start the server:
 ```$ ./Server```

**Client-side (Windows 10):**
Clone the repository using :
 ```$ git clone https://github.com/AndrewLou2/OS-chatroom-app.git```
 Run the client app  using:
 ``` python chatosapp.py```
 
## 📐 Design Process

 **UI Design:**

 ![](https://cdn.discordapp.com/attachments/868924230102818896/916054324830949376/unknown.png)
 
 **UML Use Case Diagram:**

 ![](https://cdn.discordapp.com/attachments/868924230102818896/916056012291702844/UML-Use-Case.png)

 **UML Deployment Diagram:**

 ![](https://cdn.discordapp.com/attachments/868924230102818896/916056012014899200/UML-Deployment.png)
