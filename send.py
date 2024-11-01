import pickle
import time
import socket

def recursive_call():
    reconnection_flag = 1

    while reconnection_flag == 1:
        client_socket = socket.socket()
        try:
            client_socket.connect(('192.168.1.5', 8786))
            reconnection_flag = 0
            print("Connected to server. Sending task ...")
            client_socket.send("do_llm_eval;bernard;160m".encode()) # Send request
            print("Task sent. Awaiting results ...")

            while True: 
                response = client_socket.recv(1024) # Await response

                if response == b'': # If response is empty, reconnect
                    print("Server disconnected with empty string. Trying to reconnect ...")
                    reconnection_flag = 1
                    break
                else: 
                    # Process response
                    results = pickle.loads(response)
                    if results is not None:
                        print(results)
                        break
            
        except (ConnectionRefusedError, ConnectionResetError):
            print("Failed to connect to server. Retrying ...")
            reconnection_flag = 1
            client_socket.close()
            time.sleep(10)

if __name__ == "__main__":
    recursive_call()