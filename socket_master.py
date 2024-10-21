import socket
import time

def master_client_program():
    # host = '192.168.1.100'  # Server IP
    # port = 5000  # Server port
    host = socket.gethostname() # Initiate connection to server
    port = 5000  # Server port number    
    client_socket = socket.socket() # Initiate connection to server
    client_socket.connect((host, port))    

    # Send initial identifer
    identification_data = "master"
    client_socket.send(identification_data.encode())

    # Simulate waiting for other script to call
    time.sleep(1)
    client_socket.send("request".encode())

    # Maintain connection till Server resolves client distribution
    while True:
        data = client_socket.recv(1024).decode()  # receive response
        print('Received from server: ' + data)  # show in terminal
        break
    client_socket.close()  # close the connection

if __name__ == '__main__':
    master_client_program()