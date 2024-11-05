import socket
import time
from typing import List
from const import slave_nodes
import mysql.connector
from mysql.connector import Error
import os

storage_nodes: List[tuple] = []
db_config = {
    'user': os.getenv('DB_USER', 'root'),
    'password': os.getenv('DB_PASSWORD', 'root'),
    'host': os.getenv('DB_HOST', '127.0.0.1:3306'),
    'database': os.getenv('DB_NAME', 'cloud')
}

def storage_update():
    while True:
        downed_nodes = []

        for storage_node in storage_nodes:
            _socket = socket.socket() # Initiate connection to server

            try:
                _socket.settimeout(5.0)
                _socket.connect((storage_node[0], storage_node[1]))
            except (ConnectionRefusedError, OSError):
                downed_nodes.append(storage_node)
                print(f"{storage_node[0]}:{storage_node[1]} is down.")
                continue

            #print(f"{storage_node[0]}:{storage_node[1]} is alive.")
            _socket.close()
        
        # Remove all the downed nodes
        if len(downed_nodes) > 0:
            for downed_node in downed_nodes:
                storage_nodes.remove(downed_node)
                delete_storage_node(downed_node[0], downed_node[1])
                print(f"{downed_node[0]}:{downed_node[1]} has been removed from storage nodes.")

                if len(slave_nodes) > 0:
                    slave_nodes.pop() # remove it, so that slave_process will disconnect the slave
            
            # if there is not enough slave nodes, it's okay, we'll wait until new nodes join the network
            # socket_server.py will handle the creation of new storage nodes
        
        time.sleep(2)

def save_storage_node(ip, port):
    connection = mysql.connector.connect(**db_config)

    if connection.is_connected():
        cursor = connection.cursor()

        insert_query = """
        INSERT INTO Storage (ip_address, port)
        VALUES (%s, %s);
        """
        cursor.execute(insert_query, (ip, port))

        # Commit the transaction
        connection.commit()

        # Commit the transaction
        connection.commit()
        print("Record inserted successfully.")


def delete_storage_node(ip_address, port):
    try:
        # Connect to MySQL
        connection = mysql.connector.connect(**db_config)

        if connection.is_connected():
            cursor = connection.cursor()

            # Delete record based on IP address and port
            delete_query = "DELETE FROM Storage WHERE ip_address = %s AND port = %s;"
            cursor.execute(delete_query, (ip_address, port))

            # Commit the transaction
            connection.commit()
            print(f"Deleted storage node {ip_address}:{port} from Storage table.")

    except Error as e:
        print("Error while connecting to MySQL", e)

    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()
            print("MySQL connection closed.")