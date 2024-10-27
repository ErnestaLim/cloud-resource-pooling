import os
import base64
from email.message import EmailMessage
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

import socket
import threading

# Define the broader scope for full Gmail access
SCOPES = ['https://mail.google.com/']

def authenticate():
    """Authenticate the user and return valid credentials."""
    creds = None
    # Check if token.json exists and load credentials from it
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    
    # If there are no valid credentials available, request new ones
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        
        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())
    return creds

def gmail_send_message(email):
    """Send an email using the Gmail API."""
    creds = authenticate()

    try:
        # Create a Gmail service
        service = build('gmail', 'v1', credentials=creds)

        # Create the email message
        message = EmailMessage()
        message.set_content('A master node has connected')
        message['To'] = email # change depending on user's email, could be accepted as a argument
        message['From'] = 'resourcepoolingbot@gmail.com'
        message['Subject'] = 'New connection to Server'

        # Encode the message
        encoded_message = base64.urlsafe_b64encode(message.as_bytes()).decode()

        # Create the request to send the email
        create_message = {'raw': encoded_message}
        
        # Send the email
        send_message = (
            service.users()
            .messages()
            .send(userId="me", body=create_message)
            .execute()
        )

        print(f'Message Id: {send_message["id"]}')
    except HttpError as error:
        print(f'An error occurred: {error}')
        send_message = None

    return send_message

def email_server():
    # Create a socket object
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # Bind the socket to a host and port
    host = socket.gethostbyname(socket.gethostname()) # Get the server hostname or IP
    port = 61000        # You can choose any port you prefer
    server_socket.bind((host, port))

    # Enable the server to accept connections (max 5 queued connections)
    server_socket.listen(5)
    print(f'Server listening on {host}:{port}')

    while True:
        # Accept a connection
        client_socket, addr = server_socket.accept()
        print(f'Connection from {addr}')

        # Handle the connection in a separate thread
        threading.Thread(target=handle_client, args=(client_socket,)).start()

def handle_client(client_socket):
    with client_socket:
        # Receive the email address from the client
        email = client_socket.recv(1024).decode()
        print(f'Received email address: {email}')
        # Send the email
        gmail_send_message(email)


if __name__ == "__main__":
    email_server()