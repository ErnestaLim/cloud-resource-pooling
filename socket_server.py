import socket
import threading

def handle_client(conn, address):
    client_type = conn.recv(1024).decode()
    # Save client IP to text file
    print(f"Connection from {client_type} : {address}")
    with open('client.txt', 'a') as file:
        file.write(f"{address[0], address[1], client_type}\n")
    retry_counter = 0

    while True:
        try:
            # When Master connects, send Master IP to Slave for connection
            data = f"Connect to node {client_type} {address[0]}:{address[1]}" # TO BE CHANGED TO MASTER DETAILS DURING IMPLEMENTATION
            conn.send(data.encode())
            
            # Blocking call - Till receive ACK from client
            received_data = conn.recv(1024).decode()
            if received_data == "ACK": # If server received ACK from client, release connection
                print(f"Connection from {address} released to master node.")
                break
        except:
            print(f"Something went wrong with client {address}. No ACK received.")
            retry_counter += 1 # Retry handling for disconnections or errors
            if retry_counter == 2: # Break after retrying twice
                break
    
    delete_ip(address) # Delete IP from server list
    conn.close()  # Close the connection when client disconnects

def server_program():
    # host = '192.168.1.100'  # Server IP
    # port = 5000  # Server port number
    host = socket.gethostname() # Get the server hostname or IP
    port = 5000 # Define server port    
    server_socket = socket.socket() # Create socket instance
    server_socket.bind((host, port)) # Bind the server to the host and port

    server_socket.listen(10) # Listen for up to X clients simultaneously
    print(f"Server listening on {host}:{port}")

    while True:
        conn, address = server_socket.accept() # Accept new connections
        client_thread = threading.Thread(target=handle_client, args=(conn, address)) # Create a new thread for each client
        client_thread.start()

def delete_ip(client):
    try:
        with open('client.txt', 'r') as file:
            lines = file.readlines()
        lines = [line for line in lines if line.strip() != client[0]] # Filter out the IP of the disconnected client
        with open('client.txt', 'w') as file: # Rewrite the file without the disconnected client's IP
            file.writelines(lines)
    # Exception if any
    except FileNotFoundError:
        print("IP file not found.")
    except Exception as e:
        print(f"Error removing IP: {e}")

if __name__ == '__main__':
    server_program()
