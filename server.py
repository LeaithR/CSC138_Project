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
    
    while True:
        try:
            message = client_socket.recv(1024).decode().strip()
            if not message:
                continue

            #Split message by the spaces
            parts = message.split(' ', 1)
            #parts[0] should have the command...
            command = parts[0]
            username = parts[1] if len(parts) > 1 else None

#Start of JOIN command stuff
            if command == "JOIN":
                if len(client_list) >= max_clients:
                    print("Too Many Users")
                    client_socket.send( "Too Many Users".encode())
                    client_socket.close()
                    break
                if username in client_list:
                    client_socket.send("Already Registered".encode())
                    client_socket.close()
                    break

                client_list[username] = client_socket
                print(f"{username} Joined the Chatroom")
#End of JOIN command stuff

#Start of LIST command stuff
            elif command == 'LIST':
                if username in client_list:
                    client_socket.send('\n'.join(client_list.keys()).encode())
                else:
                    client_socket.send(b"Not Registered?")
#End of LIST command stuff

#Start of MESG command stuff
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
#End of MESG command stuff

#Start of BCST command stuff
            elif command == "BCST":
                if username not in client_list:
                    client_socket.send(b"You are not registered!")
                    continue
                #check if the message len is good, if not there isn't a message to send...
                if len(parts) < 2:
                    client_socket.send("Usage: BCST <some_message_text")
                    continue
            
                bcmsg = parts[1]
                #For this if the recipient is in the list, send message, if it is the sender
                #Send a "username is sending a broadcast"?
                for recipient, recipient_socket in client_list.items():
                    if recipient == username:
                        recipient_socket.send(f"{username} is sending a broadcast")
                        recipient_socket.send(f"{username}: {bcmsg}".encode)
                    elif recipient != username:
                        recipient_socket.send(f"{username}: {bcmsg}".encode)
#End of BCST command stuff

#Start of QUIT command stuff 
            #The QUIT command, should find the client in list, delete that data
            #Then send to client that they are disconnected
            #TODO: find a way to send a "username" left message to every user NOT the one leaving
            elif command == "QUIT":
                if username in client_list:
                    del client_list[username]
                    client_socket.send(f"{username} is quitting the chat server")
                    break

#End of QUIT command stuff

#If we end up in the else statement, its a unknown command
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
    if(sys.argv) != 2:
        print("Usage: python server.py <port>")
        sys.exit(1)
    
    port = int(sys.argv[1])
    create_server(port)


if __name__ == "__main__":
    main()
