
import socket


class CarRentalClient:
    def __init__(self, host, port):
        self.host = host
        self.port = port


    def get_available_vehicles(self):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            try:
                s.connect((self.host, self.port))  
                s.send("GET_VEHICLES".encode('ascii'))


                available_cars = s.recv(4096).decode('ascii')  
                print(available_cars)
                return available_cars
            except Exception as e:
                return f"Error: Unable to connect to server - {e}"


    def book_vehicle(self, vehicle_id):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            try:
                s.connect((self.host, self.port))
                s.send(vehicle_id.encode('ascii'))  


                response = s.recv(1024).decode('ascii')  
                print(response)  
                return response
            except Exception as e:
                return f"Error: Unable to connect to server - {e}"


if __name__ == "__main__":
    client = CarRentalClient('localhost', 8888)  


    client.get_available_vehicles()


    vehicle_to_book = input("Enter the vehicle ID to book: ").strip()
    client.book_vehicle(vehicle_to_book)
-0