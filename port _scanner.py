import socket
import threading
from datetime import datetime

print("=" * 50)
print("        MULTITHREADED PORT SCANNER")
print("=" * 50)

target = input("Enter Target IP Address: ")

open_ports = []
lock = threading.Lock()

start_time = datetime.now()

semaphore = threading.Semaphore(100)


def scan_port(port):
    with semaphore:
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(0.5)

            result = s.connect_ex((target, port))

            if result == 0:
                with lock:
                    open_ports.append(port)
                print(f"[+] Port {port} is OPEN")

        except socket.error:
            pass

        finally:
            s.close()


threads = []

for port in range(1, 1025):
    thread = threading.Thread(target=scan_port, args=(port,))
    thread.start()
    threads.append(thread)

for thread in threads:
    thread.join()

end_time = datetime.now()

print("\n" + "=" * 50)
print("        SCAN COMPLETED")
print("=" * 50)

if open_ports:
    print("Open Ports:")
    for port in sorted(open_ports):
        print(port)
else:
    print("No open ports found.")

print(f"\nTotal Open Ports: {len(open_ports)}")
print(f"Time Taken: {end_time - start_time}")