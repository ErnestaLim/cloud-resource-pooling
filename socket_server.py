import socket
import threading

def handle_client(conn, address):
    # Save client IP to text file
    print(f"Connection from {address}")
    with open('client.txt', 'a') as file:
        file.write(f"{address[0]}\n")

    while True:
        try:
            # When Master connects, send Master IP to Slave for connection
            data = "Connect to THIS MASTER NODE IP:PORT" # TO BE CHANGED DURING IMPLEMENTATION
            conn.send(data.encode())
            
            # Receive ack from client and break
            data = conn.recv(1024).decode()
            if not data: # If none, break the loop
                print(f"Connection from {address} released to master node")
                break
            print(f"From {address}: {data}")
            break

        except:
            # Handle disconnection or errors
            break
    
    print(f"Connection closed: {address}")
    print(address[0])
    delete_ip(address)
    conn.close()  # Close the connection when client disconnects

def server_program():
    host = socket.gethostname() # Get the server hostname or IP
    port = 5000 # Define server port    
    server_socket = socket.socket() # Create socket instance
    server_socket.bind((host, port)) # Bind the server to the host and port

    server_socket.listen(5) # Listen for up to X clients simultaneously
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
