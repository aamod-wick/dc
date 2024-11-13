import socket


def rent_car(car_model):
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(('127.0.0.1', 9999))


    # Send the car model to the server
    client.send(car_model.encode())


    # Receive the server's response
    response = client.recv(1024).decode()
    print(response)


    client.close()


# Example of renting a car
rent_car('Toyota Camry')
