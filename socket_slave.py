import socket

def client_program():
    # host = '192.168.1.100'  # Server IP
    # port = 5000  # Server port

    host = socket.gethostbyname(socket.gethostname()) # Initiate connection to server
    port = 5000  # Server port number    
    client_socket = socket.socket() # Initiate connection to server
    client_socket.connect((host, port))    
    identification_data = "slave"
    client_socket.send(identification_data.encode()) # Send initial identifer

    # Maintain connection till Server sends Master Node IP
    while True:
        data = client_socket.recv(1024).decode()  # Receive master IP
        print('Received master IP & Port: ' + data)
        ack_data = "ACK"
        client_socket.send(ack_data.encode()) # Send ACK
        break
    
    client_socket.close() # close the connection
    return data

if __name__ == '__main__':
    master_ip = client_program()