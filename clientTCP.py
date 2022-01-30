import os
import socket
import signal
import sys
import psutil
import time

def signal_handler(sig, frame):
    print('\nDone!')
    sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)
print('Press Ctrl+C to exit...')

##

ip_addr = "200.139.139.195"
tcp_port = 5005
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

sock.connect((ip_addr, tcp_port))

while True:
        
        try:
            cpu = "CPU utili: " + str(psutil.cpu_percent()) + "%\n"
            mem = "% of physical memory in use: " + str(psutil.virtual_memory()[2]) + "%\n"
            pid = os.getpid()
            p_process = psutil.Process(pid)
            inst_mem = p_process.memory_info()[0]/2**20
            inst_msg = "Memory used by curr py instance in MBs: " + str(inst_mem) + "\n"
            available = "% of available memory: " + str(psutil.virtual_memory()[1]*100/psutil.virtual_memory()[0]) + "\n" 
            sock.send((cpu).encode())
            sock.send((mem).encode())
            sock.send((inst_msg).encode())
            sock.send((available).encode())
            response = sock.recv(4096).decode()
            print('\nServer response: {}'.format(response))
        except (socket.timeout, socket.error):
            print('Server error. Done!')
            sys.exit(0)
        if len(sys.argv) == 2:
            time.sleep(int(sys.argv[1]))
        else:
            time.sleep(5)

