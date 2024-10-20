import socket

def master_client_program():
    # host = '192.168.1.100'  # Server IP
    # port = 5000  # Server port
    host = socket.gethostname() # Initiate connection to server
    port = 5000  # Server port number    
    client_socket = socket.socket() # Initiate connection to server
    client_socket.connect((host, port))    

    # Send initial identifer
    indentification_data = "master"
    client_socket.send(indentification_data.encode())

    # Maintain connection till Server resolves client distribution
    while True:
        data = client_socket.recv(1024).decode()  # receive response
        print('Received from server: ' + data)  # show in terminal
        break
    client_socket.close()  # close the connection

def master_host():
    host = socket.gethostname() # Get hostname
    port = 5000 # Define port number
    master_socket = socket.socket() # Create socket instance
    master_socket.bind((host, port)) # Bind the server to the host and port

if __name__ == '__main__':
    master_client_program()