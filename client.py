import socket
import threading

def receive_messages(client_socket):
    while True:
        data = client_socket.recv(1024).decode()
        if not data:
            break
        print(data)

# function to handle user input in a separate thread
def handle_user_input(client_socket, username):
    receive_thread = threading.Thread(target=receive_messages, args=(client_socket,))
    receive_thread.start()

    while True:
        # Get user input
        user_input = input(f"{username}: ")

        # Send the user input to the server
        client_socket.send(user_input.encode())

        # Check if the user wants to exit
        if user_input.lower().strip() == 'bye':
            break

    client_socket.close()

def clientFunc():
    # port number and addres
    portNum = 8002
    clientHostName = socket.gethostbyname(socket.gethostname())
    
    # create socket
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    print("To exit program type bye on the client end")
    print("Enter Username:")
    userName = input()
    print(f"{userName} has connected to server")

    # connect to server
    client.connect((clientHostName, portNum))

    # Send the username immediately after connecting
    client.send(userName.encode())

    handle_user_input(client, userName)

if __name__ == '__main__':
    clientFunc()