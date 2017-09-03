import re
import subprocess
import globals
import socket

class Networking():
    """Set up networking"""

    serverIp = "localhost"

    def __init__(self):
        self.scanForServer()


    def scanForServer(self):
        arp_out =subprocess.check_output(['arp','-a']).decode("utf-8")
        test = re.findall( r'[0-9]+(?:\.[0-9]+){3}', arp_out)

        for ip in test:
            if self.tryConnect(ip):
                print('Server ' + ip + ' is alive.')
                self.serverIp = ip
                break

    def tryConnect(self, ip):
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(0.10)
            s.connect((ip, globals.PORT))
            s.close()
            return True
        except socket.error:
            return False

        