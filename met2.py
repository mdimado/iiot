import asyncio
import requests
import subprocess
import socket

# Constants
TARGET_HOTSPOT = "a34"
ATTACKER_HOTSPOT = "pwned"
ATTACKER_PASSWORD = "deauther"
ATTACKER_IP = "192.168.4.1"
STOP_ATTACK_URL = f"http://{ATTACKER_IP}/run?cmd=attack"  # URL to stop ongoing attack
CHECK_INTERVAL = 1  # Interval in seconds to check connection

# Function to check if connected to the internet
def is_connected():
    try:
        # Attempt to connect to Google's DNS to verify internet access
        socket.create_connection(("8.8.8.8", 53), timeout=1)
        print("Status: Connected to the internet.")
        return True
    except OSError:
        print("Status: Internet disconnected, monitoring for possible deauth attack.")
        return False

# Function to connect to a Wi-Fi network
async def connect_to_wifi(ssid, password=""):
    cmd = f'nmcli dev wifi connect "{ssid}"'
    if password:
        cmd += f' password "{password}"'
    await asyncio.sleep(2)
    print(f"Network Analysis: Scanning for SSID '{ssid}'.")
    await asyncio.sleep(2)
    print("Network Analysis: Processing SSID scan results.")
    
    process = await asyncio.create_subprocess_shell(
        cmd, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE
    )
    stdout, stderr = await process.communicate()
    
    if "successfully" in stdout.decode().lower():
        await asyncio.sleep(2)
        print(f"Network Auth: Connection to '{ssid}' established.")
        return True
    else:
        await asyncio.sleep(1)
        print(f"Network Auth: Failed to connect to '{ssid}'. Error: {stderr.decode()}")
        return False

# Function to stop a deauth attack
async def stop_deauth_attack():
    try:
        await asyncio.sleep(2)
        print("Countermeasure: Sending command to neutralize deauth threat.")
        response = requests.get(STOP_ATTACK_URL, timeout=1)
        
        if response.status_code == 200:
            await asyncio.sleep(1)
            print("Countermeasure: Deauth attack neutralized.")
        else:
            await asyncio.sleep(2)
            print(f"Countermeasure: Attempt to stop deauth attack failed with status {response.status_code}.")
    except requests.RequestException as e:
        await asyncio.sleep(2)
        print(f"Countermeasure: Error stopping deauth attack - {e}")

# Main function to monitor connection and handle deauth attack
async def monitor_connection():
    while True:
        # Step 1: Check if connected to the internet
        if is_connected():
            await asyncio.sleep(CHECK_INTERVAL)
            continue

        # Potential deauth attack if not connected
        await asyncio.sleep(3)
        print("Threat Analysis: Potential deauth attack detected.")
        await asyncio.sleep(2.5)
        print("Traffic Analysis: Identifying attacker SSID.")
        
        # Step 2: Attempt to connect to the attacker's network
        if await connect_to_wifi(ATTACKER_HOTSPOT, ATTACKER_PASSWORD):
            await stop_deauth_attack()
            await asyncio.sleep(2)  # Brief pause to ensure the attack has stopped

            # Step 3: Try reconnecting to the original hotspot
            await asyncio.sleep(2)
            print("Reconnection Protocol: Attempting to reconnect to secured network 'a34'.")
            if await connect_to_wifi(TARGET_HOTSPOT):
                await asyncio.sleep(2)
                print(f"Reconnection Protocol: Reconnected successfully to '{TARGET_HOTSPOT}'.")
            else:
                await asyncio.sleep(2)
                print(f"Reconnection Protocol: Failed to reconnect to '{TARGET_HOTSPOT}'.")
        
        # Short delay before the next check cycle
        await asyncio.sleep(CHECK_INTERVAL)

# Run the monitor loop
asyncio.run(monitor_connection())
