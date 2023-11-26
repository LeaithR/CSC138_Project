# client code CSC 138 Project
import socket
import threading

client = socket.socket(socket.AF.INET, socket.SOCK_STREAM)
clientHostName = socket.gethostbyname(socket.gethostname())
portNum = 8002

# function to handle user input in a separate thread
def handle_user_input(client_socket, username):
    while True:
        # Get user input
        user_input = input(f"{username}: ")
        # Send the user input to the server
        client_socket.send(user_input.encode())
        # Check if the user wants to exit
        if user_input.lower().strip() == 'bye':
            break
    # Close the client socket after the 'bye' command is received        
    client_socket.close()
    
def clientFunc():
    # port number and address
    
    # connect to server
    client.connect((clientHostName, portNum))
    
    # receive and display messages from the server
    while True:
        data = client.recv(1024).decode()
        if not data:
            break
        print(data)

  
    client.close()
  
  
if __name__ == '__main__':
      clientFunc()