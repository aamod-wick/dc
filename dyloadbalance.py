
import socket
import threading


servers = [("127.0.0.1", 9999), ("127.0.0.1", 10000), ("127.0.0.1", 10001)]
connections = {server: 0 for server in servers}  # Keep track of connections


def get_least_connection_server():
    least_connected_server = min(connections, key=connections.get)
    print(f"Selected server: {least_connected_server} with {connections[least_connected_server]} connections")
    return least_connected_server


def handle_client(client_socket):
    server = get_least_connection_server()
    connections[server] += 1


    try:
        proxy_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        proxy_socket.connect(server)


        client_request = client_socket.recv(1024)
        proxy_socket.sendall(client_request)


        while True:
            server_response = proxy_socket.recv(4096)
            if not server_response:
                break
            client_socket.sendall(server_response)


    except Exception as e:
        print(f"Error handling client: {e}")
    finally:
        proxy_socket.close()
        client_socket.close()
        connections[server] -= 1  
        print(f"Connection to {server} closed. Current load: {connections}")


def start_load_balancer():
    load_balancer = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    load_balancer.bind(("0.0.0.0", 8888))  
    load_balancer.listen(5)
    print("Load Balancer started on port 8888.")


    while True:
        client_socket, addr = load_balancer.accept()
        print(f"Accepted connection from {addr}")


        client_handler = threading.Thread(target=handle_client, args=(client_socket,))
        client_handler.start()


if __name__ == "__main__":
    start_load_balancer()
