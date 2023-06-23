#REMEMBER! SCANNING THE NETWORK WITHOUT PERMISSION IS PROHIBITED! DO NOT USE THE SCANNER ON A PUBLIC NETWORK!
#FOR PERSONAL USE ONLY!

import logging
import time
import pickle

# Suppress log messages from the 'scapy.runtime' module
logging.getLogger("scapy.runtime").setLevel(logging.ERROR)

from scapy.all import *


# Subject interface
class NetworkScanner:
    def scan_network(self, target_ip):
        pass


# Real subject
class RealNetworkScanner(NetworkScanner):
    def scan_network(self, target_ip):
        # Perform an ARP scan on the network using scapy's srp function
        # The Ether layer sets the destination MAC address to broadcast address "ff:ff:ff:ff:ff:ff"
        # The ARP layer sets the destination IP address to the target IP address
        # The srp function sends the packet and returns a list of answered and unanswered packets
        responses, _ = srp(Ether(dst="ff:ff:ff:ff:ff:ff") / ARP(pdst=target_ip), timeout=5, verbose=2)

        # Extract the response packets from the tuples and return them
        answered = [response[1] for response in responses]
        return answered


# Proxy
class NetworkScannerProxy(NetworkScanner):
    def __init__(self):
        # Create an instance of the RealNetworkScanner class and initialize the scan cache
        self.real_scanner = RealNetworkScanner()
        self.cache_file = "scan_cache.pkl"
        self.scan_cache = self.load_cache()

    def scan_network(self, target_ip):
        if target_ip in self.scan_cache:
            cached_data, expiration_time = self.scan_cache[target_ip]
            current_time = time.time()

            if current_time <= expiration_time:
                # If the cached data is still valid, retrieve and return it
                print("Retrieving cached scan results...")
                return cached_data

        # Perform a network scan using the real network scanner
        print("Performing network scan...")
        answered = self.real_scanner.scan_network(target_ip)

        # Update the cache with new devices and expiration time
        updated_cache = self.update_cache(answered, target_ip)
        self.scan_cache = updated_cache

        # Save the updated cache to the file
        self.save_cache()

        return answered

    def update_cache(self, new_devices, target_ip):
        updated_cache = {}
        current_time = time.time()

        for device in new_devices:
            ip = device.psrc
            if ip in self.scan_cache:
                # Update the expiration time for existing devices
                _, expiration_time = self.scan_cache[ip]
                updated_cache[ip] = (device, expiration_time)
            else:
                # Add new devices to the cache with the current time as the expiration time
                updated_cache[ip] = (device, current_time + (10 * 60))  # Set expiration time to 10 minutes

        # Copy the remaining devices from the existing cache
        for ip, data in self.scan_cache.items():
            if ip not in updated_cache:
                updated_cache[ip] = data

        # Update the cache for the target IP
        if target_ip in updated_cache:
            _, expiration_time = updated_cache[target_ip]
            updated_cache[target_ip] = (new_devices, expiration_time)

        return updated_cache

    def load_cache(self):
        try:
            with open(self.cache_file, "rb") as file:
                return pickle.load(file)
        except (FileNotFoundError, EOFError):
            return {}

    def save_cache(self):
        with open(self.cache_file, "wb") as file:
            pickle.dump(self.scan_cache, file)


# Client code
def main():
    proxy = NetworkScannerProxy()
    target_ip = "192.168.0.0/24"

    # Perform the scan using the network scanner proxy
    answered = proxy.scan_network(target_ip)

    # Print scan results
    print("Scanning complete. Found devices:")
    for packet in answered:
        print("IP: {}\tMAC: {}".format(packet.psrc, packet.hwsrc))

    print()

    # Print the cache
    print("Current cache:")
    for ip, (data, expiration_time) in proxy.scan_cache.items():
        #print("IP: {}".format(ip))
        print("Devices:")
        for packet in data:
            print("  IP: {}\tMAC: {}".format(packet.psrc, packet.hwsrc))
        print("Expiration Time: {}".format(expiration_time))
        print()

    # Update the cache if it's empty or the data has expired
    if target_ip not in proxy.scan_cache or time.time() > proxy.scan_cache[target_ip][1]:
        proxy.scan_cache[target_ip] = (answered, time.time() + (10 * 60))  # Update the cache with expiration time

    # Save the updated cache to the file
    proxy.save_cache()


if __name__ == "__main__":
    main()
