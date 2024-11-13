import socket
import threading
import json
import time


# List of available cars in the system
cars = {
    "1": {"model": "Toyota Camry", "available": True},
    "2": {"model": "Honda Accord", "available": True},
    "3": {"model": "Ford Mustang", "available": True},
    "4": {"model": "Tesla Model 3", "available": True},
}


# Server configuration
SERVER_IP = "127.0.0.1"
BASE_PORT = 5555
MAX_SERVERS = 3


# Lamport Clock
lamport_clock = 0


# Server ID and peer servers
server_id = int(input("Enter Server ID: "))
servers = {i: f"{SERVER_IP}:{BASE_PORT + i}" for i in range(1, MAX_SERVERS + 1)}


def increment_clock():
    global lamport_clock
    lamport_clock += 1


def sync_clock(received_clock):
    global lamport_clock
    lamport_clock = max(lamport_clock, received_clock) + 1


def broadcast_update(update_data):
    """Broadcasts an update (e.g., car rented/returned) to all other servers"""
    update_data["clock"] = lamport_clock
    for sid, addr in servers.items():
        if sid != server_id:
            try:
                host, port = addr.split(":")
                with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                    s.connect((host, int(port)))
                    s.send(json.dumps(update_data).encode())
            except Exception as e:
                print(f"Failed to send update to server {sid}: {e}")


def process_update(update_data):
    """Processes an update received from another server (car rent/return)"""
    sync_clock(update_data["clock"])
    car_id = update_data["car_id"]
    action = update_data["action"]
   
    if action == "rent":
        cars[car_id]["available"] = False
        print(f"Lamport Clock: {lamport_clock} - Car {car_id} rented (sync from server {update_data['server_id']})")
    elif action == "return":
        cars[car_id]["available"] = True
        print(f"Lamport Clock: {lamport_clock} - Car {car_id} returned (sync from server {update_data['server_id']})")
def handle_client(client_socket):
    global lamport_clock
    while True:
        try:
            request = client_socket.recv(1024).decode().strip()
            if not request:
                break
            increment_clock()
            command = request.split()
           
            if command[0] == "view":
                response = view_cars()
            elif command[0] == "rent" and len(command) > 1:
                response = rent_car(command[1])
            elif command[0] == "return" and len(command) > 1:
                response = return_car(command[1])
            else:
                response = "Invalid command"
           
            client_socket.send(response.encode())
        except Exception as e:
            print(f"Error handling client request: {e}")
            break


    client_socket.close()


def view_cars():
    """ View all available cars """
    available_cars = [f"ID: {car_id}, Model: {car_info['model']}"
                      for car_id, car_info in cars.items() if car_info["available"]]
    if not available_cars:
        return "No cars available for rent"
    return "\n".join(available_cars)


def rent_car(car_id):
    """ Rent a car if it is available """
    if car_id in cars and cars[car_id]["available"]:
        cars[car_id]["available"] = False
        print(f"Lamport Clock: {lamport_clock} - Car {car_id} rented")
       
        # Broadcast the update to other servers
        update_data = {"action": "rent", "car_id": car_id, "server_id": server_id}
        broadcast_update(update_data)
        return f"You have successfully rented {cars[car_id]['model']}."
    else:
        return f"Car ID {car_id} is either unavailable or does not exist."


def return_car(car_id):
    """ Return a car if it was previously rented """
    if car_id in cars and not cars[car_id]["available"]:
        cars[car_id]["available"] = True
        print(f"Lamport Clock: {lamport_clock} - Car {car_id} returned")
       
        # Broadcast the update to other servers
        update_data = {"action": "return", "car_id": car_id, "server_id": server_id}
        broadcast_update(update_data)
       
        return f"You have successfully returned {cars[car_id]['model']}."
    else:
        return f"Car ID {car_id} is either already available or does not exist."


def start_server():
    """ Start the server to handle clients and synchronization with other servers """
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((SERVER_IP, BASE_PORT + server_id))
    server.listen(5)
    print(f"Server {server_id} started at {SERVER_IP}:{BASE_PORT + server_id}")


    while True:
        client_socket, addr = server.accept()
        threading.Thread(target=handle_client, args=(client_socket,)).start()


def receive_updates():
    """ Starts a listener to receive updates from other servers """
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as listener:
     listener.bind((SERVER_IP, BASE_PORT + server_id + 100))  # A separate port for update receiving
     listener.listen(5)
    print(f"Server {server_id} is listening for updates on port {BASE_PORT + server_id + 100}")
       
    while True:
        conn, addr = listener.accept()
        update_data = json.loads(conn.recv(1024).decode())
        process_update(update_data)
        conn.close()


if __name__ == "__main__":
    threading.Thread(target=start_server).start()
    threading.Thread(target=receive_updates).start()







