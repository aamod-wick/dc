
import socket
import threading


vehicles = {
    "vehicle1": {"model": "Sedan", "available": True},
    "vehicle2": {"model": "SUV", "available": True},
    "vehicle3": {"model": "Hatchback", "available": True},
}


def handle_client(client_socket):
    try:
        print(f"New client connected.")


        # Receive client request
        client_request = client_socket.recv(1024).decode('ascii').strip()


        if client_request == "GET_VEHICLES":
            # Send available cars to the client
            available_cars = "\nAvailable Cars:\n"
            for vehicle_id, vehicle_info in vehicles.items():
                if vehicle_info["available"]:
                    available_cars += f"{vehicle_id} - {vehicle_info['model']}\n"
            client_socket.send(available_cars.encode('ascii'))
        else:
            # Process booking
            requested_car = client_request
            print(f"Client requested to book: {requested_car}")


            if requested_car in vehicles and vehicles[requested_car]["available"]:
                vehicles[requested_car]["available"] = False  # Mark the car as booked
                response = f"{requested_car} has been successfully booked."
            else:
                response = f"{requested_car} is not available or does not exist."


            # Send booking confirmation to client
            client_socket.send(response.encode('ascii'))


    except Exception as e:
        print(f"Error handling client: {e}")
    finally:
        client_socket.close()
        print("Client disconnected.")


def start_server(port):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('0.0.0.0', port))
    server_socket.listen(5)
    print(f"Server started on port {port} and waiting for clients...")


    while True:
        client_socket, addr = server_socket.accept()
        print(f"Connected to {addr}")
        client_handler = threading.Thread(target=handle_client, args=(client_socket,))
        client_handler.start()


if __name__ == "__main__":
    import sys
    if len(sys.argv) != 2:
        print("Usage: python car_rental_server.py <port>")
        sys.exit(1)


    port = int(sys.argv[1])
    start_server(port)