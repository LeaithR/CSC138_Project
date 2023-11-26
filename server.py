# Server code CSC 138 Project
import socket
import threading
import sys

#create a list for the current clients to send all messages to
client_list = {}
#keep the max at 10 only
max_clients = 10

#Handle the clients joining, given the socket and addr
# check if the length of client_list is more than the max(10)
# if its less then assign the client list with username w/
# socket, print out
# else: too many (more than 10), don't connect them
def handle_client(client_socket, addr):
    username = client_socket.recv(1024).decode()
    if len(client_list) < max_clients:
        client_list[username] = client_socket
        print(f"Connected with {addr}")
        print(f"{username} Joined the Chatroom")
    else:
        print("Too Many Users")
        client_socket.close()
        return
    
    while True:
        try:
            message = client_socket.recv(1024).decode().strip()
            if not message:
                continue

            #Split message by the spaces
            parts = message.split(' ', 1)
            #parts[0] should have the command...
            command = parts[0]

            if command == 'LIST':
                if username in client_list:
                    client_socket.send('\n'.join(client_list.keys()).encode())
                else:
                    client_socket.send(b"Not Registered?")

#TODO: make command stuff for BCST and QUIT



            elif command == "MESG":
                if username in client_list:
                    recipient, msg = parts[1].split(' ', 1)
                    if recipient in client_list:
                        recipient_socket = client_list[recipient]
                        recipient_socket.send(f"Nessage from {username}: {msg}".encode())
                    else:
                        client_socket.send(b"Unknown Recipient")
                else:
                    client_socket.send(b"Unregistered User")

            else:
                #If reach here unknown message, throw out
                client_socket.send(b"Unknown Message")

        except Exception as e:
            print("Error:", e)
            break


def create_server(port):
    svr_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    svr_socket.bind(("0.0.0.0", port))
    svr_socket.listen(10)
    print("The Chat Server Started")
    while True:
        client_socket, addr = svr_socket.accept()
        client_thread = threading.Thread(target=handle_client, args=(client_socket, addr))
        client_thread.start()
  

def main():
    if len(sys.argv) != 2:
        print("Usage: python server.py <port>")
        sys.exit(1)
    
    port = int(sys.argv[1])
    create_server(port)


if __name__ == "__main__":
    main()
