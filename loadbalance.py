import socket
import threading

# List of backend servers (ports where the car rental servers are running)
backend_servers = [8001, 8002]
current_server = 0
lock = threading.Lock()

def forward_request(client_socket):
    global current_server
    with lock:
        # Select server in a round-robin fashion
        backend_server_port = backend_servers[current_server]
        current_server = (current_server + 1) % len(backend_servers)

    try:
        # Forward the request to the selected backend server
        backend_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        backend_socket.connect(('127.0.0.1', backend_server_port))

        # Receive client request
        car_model = client_socket.recv(1024).decode()
        backend_socket.send(car_model.encode())

        # Receive server response and forward it back to the client
        server_response = backend_socket.recv(1024).decode()
        client_socket.send(server_response.encode())

        # Get confirmation or cancellation from the client
        user_response = client_socket.recv(1024).decode()
        backend_socket.send(user_response.encode())

        # Forward the final confirmation or cancellation message back to the client
        final_response = backend_socket.recv(1024).decode()
        client_socket.send(final_response.encode())
    finally:
        backend_socket.close()
        client_socket.close()

def start_load_balancer(port):
    load_balancer = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    load_balancer.bind(('0.0.0.0', port))
    load_balancer.listen(5)
    print(f"Load balancer listening on port {port}")

    while True:
        client_socket, addr = load_balancer.accept()
        print(f"Accepted connection from {addr}")
        threading.Thread(target=forward_request, args=(client_socket,)).start()

if __name__ == "__main__":
    # Run two load balancers on different ports
    load_balancer_ports = [9001, 9002]
    for port in load_balancer_ports:
        threading.Thread(target=start_load_balancer, args=(port,)).start()
