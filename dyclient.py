import socket

def request_car(car_model, load_balancer_port):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(('127.0.0.1', load_balancer_port))

    # Send the car model to the load balancer
    client_socket.send(car_model.encode())

    # Receive response from the server
    response = client_socket.recv(1024).decode()
    print(f"Response: {response}")

    if 'reserved' in response:
        # Simulate a confirmation
        client_socket.send("confirm".encode())
        final_response = client_socket.recv(1024).decode()
        print(f"Final Response: {final_response}")
    
    client_socket.close()

# Test client connecting to load balancer
if __name__ == "__main__":
    load_balancer_port = 9001  # Load balancer 1
    request_car("Honda Civic", load_balancer_port)
