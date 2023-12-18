import json
import socket
import threading
import uuid


class Socket:
    def __init__(self):
        self.server_id = str(uuid.uuid4())
        self.json_data = None
        self.client_socket = None

    def handle_client(self, client_socket, client_address):
        self.client_socket = client_socket

        while True:
            data = client_socket.recv(1024).decode("utf-8")

            if not data.strip():
                pass

            if data.strip():
                try:
                    # Parse the JSON data
                    if self.json_data is None:
                        return None
                    else:
                        self.json_data = json.loads(data)
                except json.JSONDecodeError as e:
                    print("Error decoding JSON:", e)

            if data.strip() == "Loaded":
                self.send_msg(self.server_id)

            client_socket.close()

    def send_msg(self, info_dict):
        if self.client_socket:
            try:
                # Convert the dictionary to a JSON string
                json_data = json.dumps(info_dict)

                # Send the JSON data to the Java client
                self.client_socket.send(json_data.encode("utf-8"))

            except json.JSONEncoder as e:
                print(f"Error encoding JSON: {e}")

    def start_server(self, ip: str, port: int):
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.bind((ip, port))
        server_socket.listen(5)  # Maximum 5 connections in the queue

        print(f"Server listening on port {port}...")

        while True:
            # Wait for a connection
            client_socket, client_address = server_socket.accept()
            print("Accepted connection from:", client_address)

            # Start a new thread to handle the client
            client_handler = threading.Thread(target=self.handle_client, args=(client_socket, client_address,))
            client_handler.start()


if __name__ == '__main__':
    S = Socket()
    S.start_server("127.0.0.1", 12345)
