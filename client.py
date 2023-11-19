# client code CSC 138 Project
import socket
 
 
def clientFunc():
    # port number and address
    portNum = 8002
    clientHostName = socket.gethostbyname(socket.gethostname())
 
     # create socket
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  
     # 
    print("To exit program type bye on client end")
    print("Enter Username:")
    userName = input()
    print(str(userName) + " has connected to server")
  
     # connect to server
    client.connect((clientHostName, portNum))
  
    message = input(str(userName) + ": ")
  
     # send and recieve messages
    while message.lower().strip() != 'bye':
         client.send(message.encode())
         data = client.recv(1024).decode()
  
         print(data)
         message = input(str(userName) + ": ")
  
    client.close()
  
  
if __name__ == '__main__':
      clientFunc()
