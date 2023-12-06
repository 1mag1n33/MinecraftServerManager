import json
import socket
import threading


def handle_client(client_socket):
    while True:
        # Receive and process statistics data
        data = client_socket.recv(1024).decode("utf-8")
        if not data:
            break  # Break the loop if no data is received

        print("Received data:", data)

        if data.strip():
            try:
                # Parse the JSON data
                json_data = json.loads(data)

                # Access individual values from the JSON data
                memory = json_data['Memory']
                cpu = json_data['CPU']

                # Process the data as needed
                print("Memory:", memory)
                print("CPU:", cpu)

            except json.JSONDecodeError as e:
                print("Error decoding JSON:", e)

    client_socket.close()


def start_server():
    # Set up a server to receive statistics
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(("0.0.0.0", 12345))
    server_socket.listen(5)  # Maximum 5 connections in the queue

    print("Server listening on port 12345...")

    while True:
        # Wait for a connection
        client_socket, client_address = server_socket.accept()
        print("Accepted connection from:", client_address)

        # Start a new thread to handle the client
        client_handler = threading.Thread(target=handle_client, args=(client_socket,))
        client_handler.start()


if __name__ == '__main__':
    start_server()
