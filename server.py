import socket
import threading

# Shared data structure for car inventory
cars = {
    'Toyota Camry': 2,
    'Honda Civic': 3,
    'Ford Mustang': 1
}

# Lock for thread-safe access to the shared data
lock = threading.Lock()

def handle_client(client_socket):
    try:
        # Receive the car model requested by the client
        car_model = client_socket.recv(1024).decode()

        with lock:
            if cars.get(car_model, 0) > 0:
                cars[car_model] -= 1
                client_socket.send(f"Car '{car_model}' reserved. Type 'confirm' or 'cancel':".encode())
            else:
                client_socket.send("Car not available.".encode())
                client_socket.close()
                return

        user_response = client_socket.recv(1024).decode()

        with lock:
            if user_response.lower() == 'confirm':
                client_socket.send("Car booked successfully!".encode())
            else:
                cars[car_model] += 1
                client_socket.send("Reservation canceled.".encode())

    finally:
        client_socket.close()

def start_server(port):
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(('0.0.0.0', port))
    server.listen(5)
    print(f"Server listening on port {port}")

    while True:
        client_socket, addr = server.accept()
        print(f"Accepted connection from {addr}")
        client_handler = threading.Thread(target=handle_client, args=(client_socket,))
        client_handler.start()

# Run servers on different ports
if __name__ == "__main__":
    server_ports = [8001, 8002]
    for port in server_ports:
        threading.Thread(target=start_server, args=(port,)).start()
