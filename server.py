# Server code CSC 138 Project
import socket
#import threading
#import sys
  
  
def serverFunc():
    print("hello")
    # port number and address
    portNum = 8002
    serverHostName = socket.gethostbyname(socket.gethostname())
    address = (serverHostName, portNum)
 
     # create socket bind to address
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(address)
  
     # limit number of clients regsitered to server
    server.listen(10)
  
    conn, address =  server.accept()
    print("The Chat Server Started!")
    print("Connected with " + str(address))
  
     # send and recieve messages
    while True:
         data = conn.recv(1024).decode()
         if not data:
             break
         print(str(data))
         data = input(' -->')
         conn.send(data.encode())
    conn.close()
  
  
if __name__ == "__main__":
      serverFunc()
