from concurrent.futures import ThreadPoolExecutor, as_completed
import subprocess
import socket
import platform
import sys
import netcommon

import piper_read_text
class PingLocals(object):
    """"""

    def __init__(self) -> None:
        """
        Discover live hosts on a local IPv4 network.
        """
        self.active_hosts = None

    def ping(self, ip):
        system = platform.system()
        if system == "Windows":
            cmd = ["ping", "-n", "1", "-w", "1000", ip]
        elif system == "Darwin":  # macOS
            cmd = ["ping", "-c", "1", "-W", "1000", ip]
        else:  # Linux and others
            cmd = ["ping", "-c", "1", "-W", "1", ip]

        try:
            subprocess.check_output(cmd, stderr=subprocess.DEVNULL)
            return True
        except subprocess.CalledProcessError:
            return False

    def ping_sweep(self, ip_base="192.168.1.", start=1, end=254, max_workers=50):
        """
        Perform a parallel ping sweep over the specified IP range.

        Args:
            ip_base (str): The first three octets of the network, ending with a dot.
            start (int): The starting value for the last octet (inclusive).
            end (int): The ending value for the last octet (inclusive).
            max_workers (int): Number of threads to use in the pool.

        Returns:
            List of tuples: Each tuple contains (ip, hostname) for active hosts.
        """
        if self.active_hosts:
            return self.active_hosts

        ip_list = [f"{ip_base}.{i}" for i in range(start, end + 1)]

        active_hosts = []

        def ping_and_resolve(ip):
            """
            Returns (ip, hostname) if ping succeeds, otherwise None.
            Assumes a 'ping(ip)' function is defined elsewhere.
            """

            if self.ping(ip):  # ping() returns True on success
                hostname = socket.getfqdn(ip)
                return ip, hostname
            return None

        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            future_to_ip = {executor.submit(ping_and_resolve, ip): ip for ip in ip_list}

            for future in as_completed(future_to_ip):
                result = future.result()
                if result:  # skip None results
                    active_hosts.append(result)

        # Return the list of active (ip, hostname) tuples
        self.active_hosts = active_hosts
        return active_hosts

    def guess_range_min(self):  # -> Tuple[str, int]:
        """
        Determine the network prefix and the lowest IP within
        that /24 subnet by rounding the last octet down to the
        nearest 10.

        Returns:
            A tuple where the first element is the dotted-decimal
            network prefix (e.g. "192.168.0") and the second element
            is the rounded-down last octet (e.g. 100).
        """
        # Try to get the actual host IP; fall back to a default
        ip = netcommon.get_host_ip() or "192.168.0.101"

        # Split into “prefix” and “last octet”
        prefix, last_octet = ip.rsplit(".", 1)
        octet_int = int(last_octet)

        # Round that octet down to the nearest ten
        min_octet = octet_int - (octet_int % 10)

        return prefix, min_octet

    def valid_local_machine_addresses(self, _ignore=None):  # -> (list | None)
        """Return sorted list of responsive hosts on local LAN,
        excluding this machine & loopback."""
        if not _ignore:
            _ignore = ["127.0.0.1", netcommon.get_host_ip()]
        if self.active_hosts:
            active_hosts = self.active_hosts
        else:
            ip_base, start = self.guess_range_min()
            active_hosts = self.ping_sweep(ip_base, start, start + 20)
        valid_hosts = []
        for test_host in active_hosts:
            if not test_host:
                continue
            if not test_host[0] in _ignore:
                valid_hosts.append(test_host[0])
        if valid_hosts:
            return sorted(valid_hosts)
        return None


def main1():
    _ping_locals = PingLocals()
    output_file = ""
    if len(sys.argv) > 2:
        print("Usage: python script.py <output_file>")
        sys.exit(1)
    if len(sys.argv) == 2:
        output_file = sys.argv[1]
    ip_base, start = _ping_locals.guess_range_min()
    active_devices = _ping_locals.ping_sweep(ip_base, start, start + 32)
    if output_file:
        with open(output_file, "w", encoding="utf-8") as f:
            for ip, hostname in active_devices:
                print(f"{ip} - {hostname}")
                f.write(f"{ip}\n")
        print(
            f"""Scan complete. {len(active_devices)} active IPs written to
{output_file}."""
        )
    else:
        for ip, hostname in active_devices:
            print(f"{ip} - {hostname}")
    print(_ping_locals.valid_local_machine_addresses())

def main():
    _piperc = piper_read_text.PiperTTSClass()
    print(_piperc.piper_voice_dir)

if __name__ == "__main__":
    main()


