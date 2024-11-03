import pickle
import time
import socket

class LLMEvalClient:
    def __init__(self, server_ip='192.168.1.5', server_port=8786):
        self.server_ip = server_ip
        self.server_port = server_port

    def do_llm_eval(self, username: str, llm_name: str):
        """Connects to the server and requests an LLM evaluation task."""
        while True:
            with socket.socket() as client_socket:
                try:
                    client_socket.connect((self.server_ip, self.server_port))
                    print("Connected to server. Sending task...")
                    task_request = f"do_llm_eval;{username};{llm_name}"
                    client_socket.send(task_request.encode())

                    print("Task sent. Awaiting results...")
                    response = client_socket.recv(4096)
                    
                    if response:
                        results = pickle.loads(response)
                        print("Received results:", results)
                        return results
                    else:
                        print("Empty response from server, retrying...")
                
                except (ConnectionRefusedError, ConnectionResetError, ConnectionAbortedError):
                    print("Connection error. Retrying in 10 seconds...")
                    time.sleep(10)
                except pickle.UnpicklingError:
                    print("Error in response format. Check server-side response.")
                    break
                except Exception as e:
                    print("An unexpected error occurred:", str(e))
                    break
