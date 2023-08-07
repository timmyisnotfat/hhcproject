import socket
import time

def send_udp_packets(destination_ip, destination_port, interval_sec, num_packets):
    startTime = time.time()
    udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    udp_socket.settimeout(5)
    sent_packets = 0
    received_packets = 0
    rtt_sum = 0
    total_data_sent = 0  # Track total data sent in bytes
    lost_data = 0
    
    try:
        udp_socket.connect((destination_ip, destination_port))
    except:
        print("Connection Failure")
        return
    udp_socket.settimeout(0.05)  # Set socket timeout to 1 second

    for i in range(num_packets):
        data = b"Packet " + str(i).encode() + b" " * 1000
        start_time = time.time()
        total_data_sent += len(data)  # Count the data size
        udp_socket.sendto(data, (destination_ip, destination_port))
        sent_packets += 1

        try:
            
            response, _ = udp_socket.recvfrom(10240)
            received_packets += 1
            end_time = time.time()
            rtt = end_time - start_time
            rtt_sum += rtt
            response_text = response.decode().strip()
            if not response.decode:
                raise Exception("Empty response")
            print(f"Received response: {response_text}, RTT: {rtt:.6f}s")
            #print(f"Received response: {response.decode()}, RTT: {rtt:.6f}s")
        except socket.timeout:
            lost_data += len(data) 
            print(f"No response received for packet {i}")
        except Exception as e:
            print(f"No response received for packet {i}")
            #print(f"An error occurred: {e}")

        time.sleep(interval_sec)

    udp_socket.close()
    endTime = time.time()
    packet_loss_rate = 1 - (received_packets / sent_packets)
    avg_rtt = rtt_sum / received_packets if received_packets > 0 else 0
    # Calculate throughput in bytes per second
    total_time = interval_sec * num_packets
    throughput = (total_data_sent - lost_data) / (endTime - startTime) * 8

    print(f"Packet Loss Rate: {packet_loss_rate:.2%}")
    print(f"Average RTT: {avg_rtt:.6f}s")
    print(f"Throughput: {throughput:.2f} bits/sec")

# Example usage:
destination_ip = "10.0.0.1"
destination_port = 5201
#interval_sec = float(input("input interval in second : ")) # 100 milliseconds interval between packets
#num_packets = int(input("input number of packets : "))
interval_sec = 0.005
num_packets = 100
send_udp_packets(destination_ip, destination_port, interval_sec, num_packets)

