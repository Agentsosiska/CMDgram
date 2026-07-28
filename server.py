import socket
import threading
import random
import string
import json

HOST = '0.0.0.0'
PORT = 55556

# Dictionary to store {client_id: (socket_file, raw_socket)}
clients = {}
clients_lock = threading.Lock()

def generate_unique_id(length=5):
    """Generates a random ID that is guaranteed not to conflict with existing clients."""
    while True:
        new_id = ''.join(random.choices(string.ascii_uppercase + string.digits, k=length))
        with clients_lock:
            if new_id not in clients:
                return new_id

def broadcast_system(message, recipient_file):
    """Utility function to send system notifications to a client."""
    payload = json.dumps({"type": "system", "content": message}) + "\n"
    recipient_file.write(payload)
    recipient_file.flush()

def handle_client(conn, addr):
    # Wrap socket with a file interface to cleanly read line-by-line (\n delimited)
    client_file = conn.makefile('rw', buffering=1, encoding='utf-8')
    client_id = generate_unique_id()

    with clients_lock:
        clients[client_id] = (client_file, conn)

    print(f"[NEW CONNECTION] {addr} assigned ID: {client_id}")

    # Send assigned ID back to the connected client
    welcome_payload = json.dumps({"type": "init", "id": client_id}) + "\n"
    client_file.write(welcome_payload)
    client_file.flush()

    try:
        while True:
            line = client_file.readline()
            if not line:
                break  # Client disconnected

            data = json.loads(line.strip())
            action = data.get("action")

            if action == "send":
                target_id = data.get("target")
                msg_content = data.get("message")

                with clients_lock:
                    target = clients.get(target_id)

                if target:
                    target_file, _ = target
                    out_payload = json.dumps({
                        "type": "message",
                        "sender": client_id,
                        "content": msg_content
                    }) + "\n"
                    target_file.write(out_payload)
                    target_file.flush()
                else:
                    broadcast_system(f"ID '{target_id}' not found.", client_file)

            elif action == "list":
                with clients_lock:
                    online_users = list(clients.keys())
                broadcast_system(f"Online users ({len(online_users)}): {', '.join(online_users)}", client_file)

    except Exception as e:
        print(f"[ERROR] Client {client_id}: {e}")
    finally:
        with clients_lock:
            if client_id in clients:
                del clients[client_id]
        conn.close()
        print(f"[DISCONNECTED] ID {client_id} left.")

def start_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # Enable SO_REUSEADDR to avoid "Address already in use" errors during quick restarts
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind((HOST, PORT))
    server.listen()
    print(f"[LISTENING] Server is running on port {PORT}...")

    while True:
        conn, addr = server.accept()
        thread = threading.Thread(target=handle_client, args=(conn, addr), daemon=True)
        thread.start()

if __name__ == "__main__":
    start_server()