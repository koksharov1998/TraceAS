import socket
import struct
import subprocess
import sys
import urllib.request
import re

try:
    ip = sys.argv[1]
except IndexError:
    ip = 'ya.ru'

tracing = subprocess.check_output('tracert -4 -d ' + ip, shell=True).decode('cp866')
print(tracing)
rslt = re.findall('\d+.\d+.\d+.\d+', tracing)[1:]
print(rslt)



def get_information_about_ip():
    return urllib.request.urlopen('https://ipinfo.io/8.8.8.8/json').read()


def get_from_ICMP():
    # слушает, если видит icmp в свою сторону - пишет отправителя, тип и код.

    def listen(host):
        s = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_ICMP)
        s.bind((host, 0))
        s.ioctl(socket.SIO_RCVALL, socket.RCVALL_ON)

        while 1:
            data = s.recvfrom(65535)[0]
            ip_header = data[0:20]
            ip_struct = struct.unpack('!BBHHHBBH4s4s', ip_header)

            if socket.inet_ntoa(ip_struct[9]) == host:
                print('{} --> icmp: Type: {}, Code: {}'.format(socket.inet_ntoa(ip_struct[8]),
                                                               *struct.unpack('BB', data[20:22])))

    listen(socket.gethostbyname(socket.gethostname()))
    return 0


# print(sys.argv)
# print(os.name)
# print(os.system('echo o'))
# os.system('ping 8.8.8.8')
print(get_information_about_ip())
# ip = sys.argv[1]
# a = subprocess.check_output('ping ' + ip, shell=True)
# print(a.decode('cp866'))
# print(get_from_tracert(ip))
# https://ipinfo.io/8.8.8.8/json
