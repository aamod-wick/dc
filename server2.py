import socket
import threading
import pickle

# Vehicle data
vehicles = {
    "vehicle1": {"model": "Sedan", "available": True},
    "vehicle2": {"model": "SUV", "available": True},
    "vehicle3": {"model": "Hatchback", "available": True},
}

# List of other server addresses for replication
replication_servers = [("127.0.0.1", 9001), ("127.0.0.1", 9002)]


def replicate_data(data, origin_server=None):
    """Replicate data to all other servers."""
    for server in replication_servers:
        if server == origin_server:
            continue  # Skip replication to the originating server
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.connect(server)
                s.sendall(pickle.dumps(data))
        except Exception as e:
            print(f"Error replicating data to {server}: {e}")


def handle_client(client_socket, address):
    """Handle incoming client requests."""
    try:
        # Send available cars to the client
        available_cars = "\nAvailable Cars:\n"
        for vehicle_id, vehicle_info in vehicles.items():
            if vehicle_info["available"]:
                available_cars += f"{vehicle_id} - {vehicle_info['model']}\n"

        client_socket.send(available_cars.encode('ascii'))

        # Receive requested car from the client
        requested_car = client_socket.recv(1024).decode('ascii').strip()
        if requested_car in vehicles and vehicles[requested_car]["available"]:
            # Mark the car as not available and replicate to other servers
            vehicles[requested_car]["available"] = False
            response = f"{requested_car} has been successfully booked."

            # Replicate the updated data to other servers
            replicate_data(vehicles)
        else:
            response = f"{requested_car} is not available or does not exist."

        client_socket.send(response.encode('ascii'))
    finally:
        client_socket.close()


def replicate_updates():
    """Listen for replication updates from other servers."""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as replication_socket:
        replication_socket.bind(("0.0.0.0", 9001))  # Replication port
        replication_socket.listen(5)
        print("Replication server listening on port 9001")

        while True:
            conn, addr = replication_socket.accept()
            with conn:
                data = pickle.loads(conn.recv(4096))
                global vehicles
                vehicles = data
                print(f"Replication data received from {addr}: {data}")


def start_server():
    """Start the main server to handle client connections."""
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    host = "127.0.0.1"
    port = 8001
    server_socket.bind((host, port))

    server_socket.listen(5)
    print(f"Server listening on {host}:{port}")

    # Start the replication listener in a separate thread
    threading.Thread(target=replicate_updates, daemon=True).start()

    while True:
        client_socket, addr = server_socket.accept()
        print(f"Connected to {addr}")
        threading.Thread(target=handle_client, args=(client_socket, addr)).start()


if __name__ == "__main__":
    start_server()
