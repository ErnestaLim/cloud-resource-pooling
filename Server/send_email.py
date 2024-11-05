import socket

def send_email():
    host = 'email' # Initiate connection to server
    port = 61000  # Server port number    
    client_socket = socket.socket() # Initiate connection to server
    client_socket.connect((host, port))    
    
    # Send initial identifer
    email = 'resourcepoolingbot@gmail.com'
    client_socket.send(email.encode())