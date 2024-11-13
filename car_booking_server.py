import socket
import threading


# Shared data structure
cars = {
    'Toyota Camry': 1,
    'Honda Civic': 1,
    'Ford Mustang': 1
}


# Lock for thread-safe access to the shared data
lock = threading.Lock()


def handle_client(client_socket):
    # Receive the car model requested by the client
    car_model = client_socket.recv(1024).decode()


    with lock:
        # Check if the car is available
        if cars.get(car_model, 0) > 0:
            # Book the car
            cars[car_model] -= 1
            client_socket.send("Car booked successfully!".encode())
        else:
            client_socket.send("Car not available.".encode())


    client_socket.close()


def start_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(('0.0.0.0', 9999))
    server.listen(5)
    print("Server listening on port 9999")


    while True:
        client_socket, addr = server.accept()
        print(f"Accepted connection from {addr}")
        client_handler = threading.Thread(target=handle_client, args=(client_socket,))
        client_handler.start()


start_server()