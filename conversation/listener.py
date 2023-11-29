import socket
import datetime

# Create a socket object
listener_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Define the listener address and port
listener_address = ('localhost', 5555)  # Change 'localhost' to the listener's IP if on different machines
listener_id = 12214737

# Bind the socket to the listener's address and port
listener_socket.bind(listener_address)

# Listen for incoming connections
listener_socket.listen(1)

print("Listener is ready to receive pings...")

def listener(que):
    while True:
        # Wait for a connection
        user_socket, user_address = listener_socket.accept()

        print(f"Connection established with {user_address}")

        # Receive a message from the user
        message = user_socket.recv(1024).decode()

        if message == "ping":
            # Get current time and vehicle count (replace with your vehicle count logic)
            current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            vehicle_count = que.get() # Replace with the actual vehicle count logic

            # Prepare the response message
            response_message = f"Time: {current_time}, Listener ID: {listener_id}, Vehicle Count: {vehicle_count}"

            # Send the response to the user
            user_socket.sendall(response_message.encode())

        # Close the connection with the user
        user_socket.close()
