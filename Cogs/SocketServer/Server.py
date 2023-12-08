import json
import socket
import threading


class Socket:
    def __init__(self):
        self.javaruntime = None
        self.sysinfo = None
        self.memory = None
        self.cpu = None
        self.uptime = None
        self.tps = None
        self.worldinfo = None
        self.diskspace = None
        self.playerinfo = None

    def handle_client(self, client_socket):
        while True:
            # Receive and process statistics data
            data = client_socket.recv(1024).decode("utf-8")
            if not data:
                break  # Break the loop if no data is received

            if data.strip():
                try:
                    # Parse the JSON data
                    json_data = json.loads(data)

                    # Access individual values from the JSON data
                    self.javaruntime = json_data['JavaRuntime']
                    self.sysinfo = json_data['SystemInfo']
                    self.memory = json_data['Memory']
                    self.cpu = json_data['CPU']
                    self.uptime = json_data['ServerUpTime']
                    self.tps = json_data['Tps']
                    self.worldinfo = json_data['WorldInfo']
                    self.diskspace = json_data['DiskSpace']
                    self.playerinfo = json_data['PlayerStatistics']

                    print(self.getJavaRuntime())


                except json.JSONDecodeError as e:
                    print("Error decoding JSON:", e)

        client_socket.close()

    def start_server(self):
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
            client_handler = threading.Thread(target=self.handle_client, args=(client_socket,))
            client_handler.start()

    def getJavaRuntime(self):
        return self.javaruntime

    def getSysInfo(self):
        return self.sysinfo

    def getMemoryInfo(self):
        return self.memory

    def getCpuInfo(self):
        return self.cpu

    def getUpTime(self):
        return self.uptime

    def getTps(self):
        return self.tps

    def getWorldInfo(self):
        return self.worldinfo

    def getDiskSpace(self):
        return self.diskspace

    def getPlayerInfo(self):
        return self.playerinfo


if __name__ == '__main__':
    S = Socket()
    S.start_server()