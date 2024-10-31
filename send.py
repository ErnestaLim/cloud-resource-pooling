import pickle
import socket

client_socket = socket.socket() # Initiate connection to server
client_socket.connect(('192.168.1.5', 8786))    

# Send request
client_socket.send("do_llm_eval;bernard;160m".encode())

while True:
    response = client_socket.recv(1024)
    results = pickle.loads(response)
    print(results)
    break