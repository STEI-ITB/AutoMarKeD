from ncclient import manager
import sys

host = str(sys.argv[1])
port = str(sys.argv[2])
username = str(sys.argv[3])
password = str(sys.argv[4])
filename = str(sys.argv[5])

def read_file(fn):
    with open(fn) as f:
        result = f.read()
    return result

xml = read_file(filename)

with manager.connect(host=host, port=port, username=username, password=password, hostkey_verify=False, device_params={'name': 'csr'}) as m:
    reply = m.edit_config(target='running', config=xml)

print("Success? {}".format(reply.ok))

## Using this File
## ptyhon sendXML.py {ip-address} {netconf-port} {username} {password} {file-name}
