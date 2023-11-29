import socket

# Create a socket object
user_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Define the listener's address and port
listener_address = ('localhost', 5555)  # Change 'localhost' to the listener's IP if on different machines

# Connect to the listener
user_socket.connect(listener_address)

# Send a ping message to the listener
user_socket.sendall("ping".encode())

# Receive the response from the listener
response = user_socket.recv(1024).decode()

print(f"Listener response: {response}")

# Close the connection
user_socket.close()
