import socket
import threading
import random
import string

SERVER_IP = '127.0.0.1' # -----> Change to your host's public IP <-----
PORT = 55555

def generate_id(length=5):
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=length))

def receive_messages(client_socket):
    while True:
        try:
            message = client_socket.recv(1024).decode('utf-8')
            if message:
                print(message)
                print("To (ID:Message) > ", end="")
        except:
            print("[Error] Connection lost.")
            client_socket.close()
            break

def start_client():
    logo = """
     ____ __  __ ____                               
    / ___|  \/  |  _ \  __ _ _ __ __ _ _ __ ___  
   | |   | |\/| | | | |/ _` | '__/ _` | '_ ` _ \ 
   | |___| |  | | |_| | (_| | | | (_| | | | | | |
    \____|_|  |_|____/ \__, |_|  \__,_|_| |_| |_|
                       |___/                      
    """
    print(logo)
    
    my_id = generate_id()
    print(f"--- Welcome to CMDgram ---")
    print(f"YOUR ANONYMOUS ID: {my_id}")
    print(f"Instructions: To text someone, type 'ID:Message'\n")

    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        client.connect((SERVER_IP, PORT))
        client.send(my_id.encode('utf-8'))
    except:
        print("Could not connect to server.")
        return

    thread = threading.Thread(target=receive_messages, args=(client,))
    thread.daemon = True
    thread.start()

    while True:
        msg = input("To (ID:Message) > ")
        if msg.lower() == 'exit':
            break
        client.send(msg.encode('utf-8'))

if __name__ == "__main__":
    start_client()