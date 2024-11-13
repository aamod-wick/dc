import socket


SERVER_IP = "127.0.0.1"
SERVER_PORT = 5555


def send_request(server_id, request):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((SERVER_IP, SERVER_PORT + server_id))
        s.send(request.encode())
        response = s.recv(1024).decode()
        print(response)


if __name__ == "__main__":
    server_id = int(input("Enter the server ID to connect to: "))
    while True:
        request = input("Enter command (view, rent <car_id>, return <car_id>): ")
        send_request(server_id, request)
