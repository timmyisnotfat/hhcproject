import socket

def sctp_server(server_ip, server_port):
    sctp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM, socket.IPPROTO_SCTP)
    sctp_socket.bind((server_ip, server_port))
    sctp_socket.listen(5)

    print(f"SCTP Server listening on {server_ip}:{server_port}")

    while True:
        client_socket, client_address = sctp_socket.accept()
        print(f"Connection from {client_address}")

        while True:
            try:
                data = client_socket.recv(1024)
                if not data:
                    break
                print(f"Received data: {data.decode()}")

                response = b"Server received: " + data
                client_socket.send(response)
            except Exception as e:
                print(f"Error: {e}")
                break

        print(f"Closing connection from {client_address}")
        client_socket.close()

# Example usage:
server_ip = "10.0.0.1"
server_port = 5201

sctp_server(server_ip, server_port)

