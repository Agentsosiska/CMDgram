import socket
import threading

# Server configuration
HOST = '0.0.0.0'  # Listen on all available interfaces
PORT = 55555

# Dictionary to store {random_id: client_socket}
clients = {}

def handle_client(client_socket, client_id):
    print(f"[NEW CONNECTION] ID {client_id} connected.")
    
    while True:
        try:
            # Format: "TARGET_ID:MESSAGE"
            data = client_socket.recv(1024).decode('utf-8')
            if not data:
                break
            
            if ":" in data:
                target_id, message = data.split(":", 1)
                
                if target_id in clients:
                    target_socket = clients[target_id]
                    target_socket.send(f"\n[From {client_id}]: {message}".encode('utf-8'))
                else:
                    client_socket.send(f"[System] ID {target_id} not found.".encode('utf-8'))
            else:
                client_socket.send("[System] Invalid format. Use ID:Message".encode('utf-8'))
                
        except:
            break

    print(f"[DISCONNECTED] ID {client_id} left.")
    del clients[client_id]
    client_socket.close()

def start_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((HOST, PORT))
    server.listen()
    print(f"[LISTENING] Server is running on port {PORT}...")

    while True:
        conn, addr = server.accept()
        # Receive the random ID the client generated
        client_id = conn.recv(1024).decode('utf-8')
        clients[client_id] = conn
        
        thread = threading.Thread(target=handle_client, args=(conn, client_id))
        thread.start()

if __name__ == "__main__":
    start_server()