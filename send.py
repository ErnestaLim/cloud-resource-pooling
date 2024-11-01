import pickle
import socket

def recursive_call():
    client_socket = socket.socket() # Initiate connection to server

    try:
        client_socket.connect(('192.168.1.5', 8786))
    except ConnectionRefusedError:
        print("Failed to connect to server. Retrying ...")
        recursive_call()
        return

    print("Connected to server. Sending task ...")

    # Send request
    client_socket.send("do_llm_eval;bernard;160m".encode())

    print("Task sent. Awaiting results ...")

    while True:
        try:
            response = client_socket.recv(1024)

            # If server disconnect
            if response == b'':
                print("Server disconnected with empty string. Trying to reconnect ...")
                recursive_call()
                return
        except (ConnectionAbortedError, ConnectionResetError):
            print("Server disconnected with error. Trying to reconnect ...")
            recursive_call()
            return

        results = pickle.loads(response)
        
        if results is not None:
            print(results)
            break

if __name__ == "__main__":
    recursive_call()