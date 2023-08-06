import socket
import time

def send_tcp_packets(destination_ip, destination_port, interval_sec, num_packets):
    startTime = time.time()
    tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    #tcp_socket.connect((destination_ip, destination_port))
    tcp_socket.settimeout(10)  # Set socket timeout to 1 second

    sent_packets = 0
    received_packets = 0
    rtt_sum = 0
    total_data_sent = 0  # Track total data sent in bytes
    lost_data = 0
    
    try:
        tcp_socket.connect((destination_ip, destination_port))
    except socket.timeout:
        print("Connection Failure")
        return
    tcp_socket.settimeout(0.001)  # Set socket timeout to 1 second

    for i in range(num_packets):
        data = b"Packet " + str(i).encode()
        start_time = time.time()
        total_data_sent += len(data)  # Count the data size
        tcp_socket.send(data)
        sent_packets += 1

        try:
            response = tcp_socket.recv(1024)
            received_packets += 1
            end_time = time.time()
            rtt = end_time - start_time
            rtt_sum += rtt
            print(f"Received response: {response.decode()}, RTT: {rtt:.6f}s")
        except socket.timeout:
            lost_data += len(data) 
            print(f"No response received for packet {i} within 1 second")

        time.sleep(interval_sec)

    tcp_socket.close()
    endTime = time.time()
    packet_loss_rate = 1 - (received_packets / sent_packets)
    avg_rtt = rtt_sum / received_packets if received_packets > 0 else 0
    # Calculate throughput in bytes per second
    total_time = interval_sec * num_packets
    
    throughput = (total_data_sent - lost_data) / (endTime - startTime)

    print(f"Packet Loss Rate: {packet_loss_rate:.2%}")
    print(f"Average RTT: {avg_rtt:.6f}s")
    print(f"Throughput: {throughput:.2f} bytes/sec")

# Example usage:
destination_ip = "10.0.0.1"
destination_port = 5201
#interval_sec = 0.0001  # 100 milliseconds interval between packets
#num_packets = 10000

interval_sec = float(input("input interval in second : ")) # 100 milliseconds interval between packets
num_packets = int(input("input number of packets : "))


send_tcp_packets(destination_ip, destination_port, interval_sec, num_packets)
