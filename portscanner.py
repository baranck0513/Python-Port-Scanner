import socket
import threading
from queue import Queue

target = input("Enter the target IP address: ")
port_range = input("Enter the port range (for example 20-80): ")

try:
    start_port, end_port = map(int, port_range.split('-'))
    if start_port > end_port:
        print("Invalid port range. Start port should be less than or equal to end port.")
        exit()
except ValueError:
    print("Invalid input. Please enter the port range in the correct format (for example 20-80).")
    exit()

queue = Queue()

def scan_port(port):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.settimeout(1)
        try:
            result = sock.connect_ex((target, port))
            if result == 0:
                print(f"Port {port} is open")
        except socket.timeout:
            pass 
        except socket.error:
            pass  

def worker():
    while not queue.empty():
        port = queue.get()
        scan_port(port)
        queue.task_done()

for port in range(start_port, end_port + 1):
    queue.put(port)

print(f"Starting port scan on {target} from port {start_port} to {end_port}")

num_threads = 100
threads = []
for _ in range(num_threads):
    t = threading.Thread(target=worker)
    t.daemon = True
    t.start()
    threads.append(t)

queue.join()

print("Port scanning completed.")
