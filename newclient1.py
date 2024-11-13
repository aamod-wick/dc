import socket

def request_car(host, port):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((host, port))

        # Receive and display available cars
        available_cars = s.recv(1024).decode('ascii')
        print(available_cars)

        # Prompt the user to enter the car they want to book
        requested_car = input("Enter the vehicle ID to book: ").strip()
        s.send(requested_car.encode('ascii'))

        # Receive and display the response
        response = s.recv(1024).decode('ascii')
        print(response)

if __name__ == "__main__":
    # Connect to server (change the host/port to connect to different servers)
    host = "127.0.0.1"
    port = 8001  # Ensure this matches the server's listening port
    request_car(host, port)
