import argparse
import pickle
import time
import socket

def recursive_call(username: str, llm_name: str):
    reconnection_flag = 1

    while reconnection_flag == 1:
        client_socket = socket.socket()
        try:
            client_socket.connect(('192.168.1.5', 8786))
            reconnection_flag = 0
            print("Connected to server. Sending task ...")
            client_socket.send(f"do_llm_eval;{username};{llm_name}".encode()) # Send request
            print("Task sent. Awaiting results ...")

            while True: 
                try:
                    response = client_socket.recv(1024) # Await response
                except ConnectionAbortedError:
                    print("Server disconnected. Trying to reconnect ...")
                    reconnection_flag = 1
                    break

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
    # Set up argument parser
    parser = argparse.ArgumentParser(description='Client program to connect to a server.')
    parser.add_argument('--username', type=str, default="guest", help='Username to use for the task')
    parser.add_argument('--llm_name', type=str, default="EleutherAI/pythia-160m", help='LLM namespace from Hugging Face')
    args = parser.parse_args()
    
    recursive_call(args.username, args.llm_name)