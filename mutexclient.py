# client.py
import socket

def start_client():
    server_ip = "127.0.0.1"
    server_port = 5555

    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((server_ip, server_port))
    print("[INFO] Connected to the server")

    try:
        while True:
            # Display options to the user
            print("\nChoose an option:")
            print("1. View available cars (view)")
            print("2. Rent a car (rent <car_id>)")
            print("3. Return a car (return <car_id>)")
            print("4. Exit")

            # Get user input
            choice = input("Enter your choice: ").strip()

            # If the user wants to exit
            if choice.lower() == "exit":
                print("[INFO] Exiting...")
                break

            # Send the user input as a command to the server
            client.send(choice.encode())

            # Receive and display the response from the server
            response = client.recv(1024).decode()
            print(f"Server Response: {response}")

    except Exception as e:
        print(f"[ERROR] Exception in client: {e}")
    finally:
        print("[INFO] Closing connection")
        client.close()

# Run the client
if __name__ == "__main__":
    start_client()
