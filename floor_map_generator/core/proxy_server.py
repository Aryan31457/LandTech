import socket
from threading import Thread


# External server details
EXTERNAL_SERVER_HOST = '192.168.1.100'
EXTERNAL_SERVER_PORT = 5000

# Local proxy server details
PROXY_SERVER_HOST = '127.0.0.1'
PROXY_SERVER_PORT = 4000  # Port for frontend to connect to

def handle_client(client_socket):
    """Handles communication with the frontend and relays data to the external server."""
    try:
        # Receive data from the frontend
        client_data = client_socket.recv(1024).decode('utf-8')

        # Forward data to the external server
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as external_socket:
            external_socket.connect((EXTERNAL_SERVER_HOST, EXTERNAL_SERVER_PORT))
            external_socket.send(client_data.encode('utf-8'))

            # Receive response from external server
            response = external_socket.recv(4096).decode('utf-8')

        # Send the response back to the frontend
        client_socket.send(response.encode('utf-8'))

    except Exception as e:
        error_message = f"Error occurred: {str(e)}"
        client_socket.send(error_message.encode('utf-8'))

    finally:
        client_socket.close()

def start_proxy_server():
    """Starts the proxy server to listen for frontend connections."""
    proxy_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    proxy_socket.bind((PROXY_SERVER_HOST, PROXY_SERVER_PORT))
    proxy_socket.listen(5)

    print(f"Proxy server running on {PROXY_SERVER_HOST}:{PROXY_SERVER_PORT}...")
    while True:
        client_socket, _ = proxy_socket.accept()
        thread = Thread(target=handle_client, args=(client_socket,))
        thread.start()
