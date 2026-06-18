import asyncio
import socket
import sys
import time

# Standard ports for infrastructure scanning
TARGET_PORTS = [21, 22, 23, 25, 53, 80, 110, 135, 139, 443, 445, 1433, 3306, 3389, 8080]

async def check_port(ip_address: str, port: int) -> int:
    """
    Asynchronously attempts to establish a connection to a specific port.
    Returns the port number if successful, otherwise returns None.
    """
    try:
        connection = asyncio.open_connection(ip_address, port)
        reader, writer = await asyncio.wait_for(connection, timeout=1.0)
        print(f"  [SUCCESS] Port {port:<5} -> STATUS: OPEN")
        writer.close()
        await writer.wait_closed()
        return port
    except (asyncio.TimeoutError, ConnectionRefusedError, OSError):
        return None

async def main():
    print("-" * 60)
    print("  NETWORK UTILITIES: HIGH-SPEED ASYNCHRONOUS PORT SCANNER  ")
    print("-" * 60)
    
    target_host = input("[INPUT] Enter target hostname or IP address: ").strip()
    if not target_host:
        print("[ERROR] Target hostname cannot be empty.")
        sys.exit(1)
    
    try:
        target_ip = socket.gethostbyname(target_host)
        print(f"[INFO] Resolved target: {target_host} -> {target_ip}")
        print("[INFO] Initializing concurrent port scan...\n")
    except socket.gaierror:
        print(f"[ERROR] Failed to resolve hostname: '{target_host}'")
        sys.exit(1)

    start_time = time.time()

    # Create and execute concurrent tasks for all targeted ports
    tasks = [check_port(target_ip, port) for port in TARGET_PORTS]
    await asyncio.gather(*tasks)

    end_time = time.time()
    execution_time = end_time - start_time
    
    print("\n" + "-" * 60)
    print(f"[INFO] Scan finished execution in {execution_time:.2f} seconds.")
    print("-" * 60)

if __name__ == "__main__":
    # Ensure modern async loop implementation approach
    asyncio.run(main())
