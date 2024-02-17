"""Simple HTML Server to serve a local static web page."""

import http.server
import socketserver
import os
import platform

try:
    import requests

    REQUESTS_OK = True
except:
    REQUESTS_OK = False
import threading


class MyServer:
    def __init__(self):
        # Avoid the range of numbers registered with the Internet Assigned
        # Numbers Authority (IANA)
        self.port = 50063
        self.node = platform.node()
        self.host = "localhost"
        self.old_dir = os.getcwd()
        self.site_dir = os.path.join(
            os.path.dirname(os.path.abspath(__file__)), "check_dialog"
        )
        os.chdir(self.site_dir)
        self.Handler = http.server.SimpleHTTPRequestHandler
        self.httpd = socketserver.TCPServer((self.host, self.port), self.Handler)
        self.host_and_port = """http://{0}:{1}""".format(self.host, str(self.port))
        self.ok_message = """
* The `http.server` is serving `{0}`.
* The platform node is `{1}`.
* Use the class `stop` command to shut down the server.
""".format(
            self.host_and_port, self.node
        )

    def start(self):
        print(self.ok_message)
        thread = threading.Thread(target=self.httpd.serve_forever)
        thread.start()

    def stop(self):
        self.httpd.shutdown()
        os.chdir(self.old_dir)

    def is_valid_url(self, url=""):  # -> bool
        """Test if the server works, If the length of `url` is `0` then the`
        procedure tests the locally running server.and port."""
        if not REQUESTS_OK:
            return False
        if len(url) == 0:
            url = self.host_and_port
        try:
            response = requests.get(url)
            return response.status_code == 200
        except:
            return False


def main():
    """Test the `MyServer` class."""
    # Usage
    server = MyServer()
    server.start()


if __name__ == "__main__":
    main()
