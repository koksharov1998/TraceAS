import json
import re
import subprocess
import sys
import urllib.request

help_words = {'/?', '-h', '--help', '-help'}

if len(sys.argv) != 2 or sys.argv[1] in help_words:
    print(
        '\nThis utility can make tracing to the specified node and show intermediate nodes and their autonomous system\nUse parameter -i to use interactive mode\n\nUSAGE: python trace.py  [IPAddressOrDomainName]\n\nExample: python trace.py ya.ru')
    sys.exit()
else:
    if sys.argv[1] == '-i':
        print('Please enter IP address or domain name:')
        ip = input()
    else:
        ip = sys.argv[1]

try:
    tracing = subprocess.check_output('tracert -4 -d ' + ip, shell=True).decode('cp866')
except subprocess.CalledProcessError:
    print("Check you Internet connection.")
    sys.exit()


def get_information_about_ip(ip):
    return json.loads(urllib.request.urlopen('https://ipinfo.io/' + ip + '/json').read())


rslt = re.findall('\d+.\d+.\d+.\d+', tracing)[1:]

full_information = []

for ip in rslt:
    info = get_information_about_ip(ip)
    if 'bogon' in info:
        full_information.append(str(len(full_information) + 1) + '\t' + info['ip'])
    else:
        full_information.append(
            str(len(full_information) + 1) + '\t' + info['ip'] + '\t' + info['country'] + '\t' + info['org'])

for note in full_information:
    print(note)
