# client code CSC 138 Project
import socket
import threading

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

    user_input_thread = threading.Thread(target=handle_user_input, args=(client, userName))
    user_input_thread.start()

    message = input(str(userName) + ": ")
  
    # receive and display messages from the server
    while True:
        data = client.recv(1024).decode()
        if not data:
            break
        print(data)
  
    client.close()
  
  
if __name__ == '__main__':
      clientFunc()