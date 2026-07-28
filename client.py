import socket
import threading
import json
import sys

SERVER_IP = '127.0.0.1'  # Change to your host's IP address
PORT = 55555

def receive_messages(server_file):
    """Continuously reads incoming line-delimited JSON messages from the server."""
    while True:
        try:
            line = server_file.readline()
            if not line:
                print("\n[Disconnected from server]")
                break
            
            data = json.loads(line.strip())
            msg_type = data.get("type")

            if msg_type == "message":
                sender = data.get("sender")
                content = data.get("content")
                print(f"\n[From {sender}]: {content}")
                print("To (ID:Message) > ", end="", flush=True)

            elif msg_type == "system":
                content = data.get("content")
                print(f"\n[System]: {content}")
                print("To (ID:Message) > ", end="", flush=True)

        except Exception:
            print("\n[Error] Connection to server lost.")
            break

def start_client():
    logo = r"""
     ____ __  __ ____                               
    / ___|  \/  |  _ \  __ _ _ __ __ _ _ __ ___  
   | |   | |\/| | | | |/ _` | '__/ _` | '_ ` _ \ 
   | |___| |  | | |_| | (_| | | | (_| | | | | | |
    \____|_|  |_|____/ \__, |_|  \__,_|_| |_| |_|
                       |___/                      
    """
    print(logo)

    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        client.connect((SERVER_IP, PORT))
    except Exception as e:
        print(f"Could not connect to server: {e}")
        return

    # Wrap raw socket in a file interface for line-based reading/writing
    server_file = client.makefile('rw', buffering=1, encoding='utf-8')

    # Read server init message to get assigned ID
    init_line = server_file.readline()
    init_data = json.loads(init_line.strip())
    my_id = init_data.get("id")

    print(f"--- Welcome to CMDgram ---")
    print(f"YOUR ANONYMOUS ID: {my_id}")
    print("Commands:")
    print("  - Type 'ID:Message' to text someone (e.g., A1B2C:Hello)")
    print("  - Type '/list' to see who is online")
    print("  - Type '/exit' to quit\n")

    # Start incoming message thread
    thread = threading.Thread(target=receive_messages, args=(server_file,), daemon=True)
    thread.start()

    while True:
        try:
            user_input = input("To (ID:Message) > ").strip()
            if not user_input:
                continue

            if user_input.lower() == '/exit':
                print("Goodbye!")
                break

            elif user_input.lower() == '/list':
                payload = json.dumps({"action": "list"}) + "\n"
                server_file.write(payload)
                server_file.flush()

            elif ":" in user_input:
                target_id, message = user_input.split(":", 1)
                payload = json.dumps({
                    "action": "send",
                    "target": target_id.strip(),
                    "message": message.strip()
                }) + "\n"
                server_file.write(payload)
                server_file.flush()
            else:
                print("[System] Invalid format. Use 'ID:Message', '/list', or '/exit'")

        except (KeyboardInterrupt, EOFError):
            break

    client.close()

if __name__ == "__main__":
    start_client()