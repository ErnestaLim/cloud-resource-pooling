import socket

def client_program():
    
    # Initiate connection to server
    host = socket.gethostname()
    port = 5000  # Server port number    
    client_socket = socket.socket() # Initiate connection to server
    client_socket.connect((host, port))

    # Maintain connection till Server sends Master IP
    while True:
        data = client_socket.recv(1024).decode()  # receive response
        print('Received from server: ' + data)  # show in terminal
        break
    client_socket.close()  # close the connection

if __name__ == '__main__':
    client_program()