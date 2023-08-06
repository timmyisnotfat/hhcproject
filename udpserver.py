import socket

def udp_server(server_ip, server_port, timeout_sec):
    udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    udp_socket.bind((server_ip, server_port))

    print(f"UDP Server listening on {server_ip}:{server_port}")

    #udp_socket.settimeout(timeout_sec)  # Set the socket timeout for receiving

    while True:
        try:
            data, client_address = udp_socket.recvfrom(1024)
            print(f"Connection from {client_address}")
            print(f"Received data: {data.decode()}")

            response = b"Server received: " + data
            udp_socket.settimeout(timeout_sec)  # Set the socket timeout for receiving
            udp_socket.sendto(response, client_address)
        except socket.timeout:
            print("waiting......")
            continue
            break
        except Exception as e:
            print(f"Error: {e}")
            break

    udp_socket.close()

# Example usage:
server_ip = "10.0.0.1"
server_port = 5201
timeout_sec = 5 # Adjust this timeout value as needed

udp_server(server_ip, server_port, timeout_sec)
