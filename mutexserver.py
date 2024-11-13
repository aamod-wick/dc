import socket
import threading

# List of available cars in the system
cars = {
    "1": {"model": "Toyota Camry", "available": True},
    "2": {"model": "Honda Accord", "available": True},
    "3": {"model": "Ford Mustang", "available": True},
    "4": {"model": "Tesla Model 3", "available": True},
}

# Token for mutual exclusion (only the thread with the token can rent/return)
token_available = True
request_queue = []  # Queue of client requests for the token
token_lock = threading.Lock()

# Function to handle client connections
def handle_client(client_socket, addr):
    print(f"[INFO] New connection established from {addr}")
    try:
        while True:
            # Receive client request
            request = client_socket.recv(1024).decode()
            if not request:
                break

            command = request.split()

            if command[0] == "view":
                response = view_cars()
            elif command[0] in ["rent", "return"] and len(command) > 1:
                # Clients request the token for rent/return operations
                with token_lock:
                    request_queue.append((client_socket, command))
                process_requests()
                continue  # Don't send response immediately for rent/return
            else:
                response = "[ERROR] Invalid command"

            # Send the response back to the client
            client_socket.send(response.encode())
    except Exception as e:
        print(f"[ERROR] Exception in client handler: {e}")
    finally:
        print(f"[INFO] Connection closed from {addr}")
        client_socket.close()

# Function to view available cars
def view_cars():
    available_cars = [f"ID: {car_id}, Model: {car_info['model']}" 
                      for car_id, car_info in cars.items() if car_info["available"]]
    if not available_cars:
        return "[INFO] No cars available for rent"
    return "\n".join(available_cars)

# Function to rent a car
def rent_car(car_id):
    if car_id in cars and cars[car_id]["available"]:
        cars[car_id]["available"] = False
        return f"[INFO] You have successfully rented {cars[car_id]['model']}."
    else:
        return f"[INFO] Car ID {car_id} is either unavailable or does not exist."

# Function to return a car
def return_car(car_id):
    if car_id in cars and not cars[car_id]["available"]:
        cars[car_id]["available"] = True
        return f"[INFO] You have successfully returned {cars[car_id]['model']}."
    else:
        return f"[INFO] Car ID {car_id} is either already available or does not exist."

# Function to process client requests for mutual exclusion
def process_requests():
    global token_available
    if token_available and request_queue:
        token_available = False
        client_socket, command = request_queue.pop(0)  # Get the next request

        if command[0] == "rent":
            response = rent_car(command[1])
        elif command[0] == "return":
            response = return_car(command[1])

        # Send the response to the client
        client_socket.send(response.encode())
        
        # Release the token after processing
        release_token()

# Function to release the token and allow the next request to be processed
def release_token():
    global token_available
    with token_lock:
        token_available = True
        process_requests()  # Process the next request if any are waiting

# Main server function
def start_server():
    server_ip = "127.0.0.1"
    server_port = 5555
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((server_ip, server_port))
    server.listen(5)
    print(f"[INFO] Server started at {server_ip}:{server_port}")

    while True:
        client_socket, addr = server.accept()
        # Create a new thread to handle the client connection
        client_handler = threading.Thread(target=handle_client, args=(client_socket, addr))
        client_handler.start()

# Run the server
if __name__ == "__main__":
    start_server()
