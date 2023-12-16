import json
import socket
import threading
import uuid


class Socket:
    def __init__(self):
        self.server_id = str(uuid.uuid4())

        self.javaruntime = None
        self.sysinfo = None
        self.memory = None
        self.cpu = None
        self.uptime = None
        self.tps = None
        self.worldinfo = None
        self.diskspace = None
        self.playerinfo = None
        self.client_socket = None

    def handle_client(self, client_socket):
        self.client_socket = client_socket
        while True:
            # Receive and process statistics data
            data = client_socket.recv(1024).decode("utf-8")
            if not data:
                break  # Break the loop if no data is received

            if data.strip():
                try:
                    # Parse the JSON data
                    json_data = json.loads(data)
                    print(json_data)

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

                except json.JSONDecodeError as e:
                    print("Error decoding JSON:", e)

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
        self.send_msg(self.server_id)

        print(f"Server listening on port {port}...")

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
    S.start_server("0.0.0.0", 12345)
