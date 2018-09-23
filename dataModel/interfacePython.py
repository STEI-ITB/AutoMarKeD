from binding_python import ietf_interfaces
import pyangbind.lib.pybindJSON as pybindJSON
import json

model = ietf_interfaces()
new_interface = model.interfaces.interface.add('GigabitEthernet4')
# print new_interface.get()

## setting new interfaces description
new_interface.description = 'NETCONF-CONFIGURED PORT'
new_interface.enabled = "True"
#new_interface.type = "True"
#new_interface.link_up_down_trap_enable = "Enabled"

# print new_interface.get()['description']

ipv4add = new_interface.ipv4.address.add('4.4.4.4')
ipv4add.netmask = '255.255.255.0'
new_interface.ipv4.enabled = "True"
new_interface.ipv4.forwarding = "True"
new_interface.ipv4.mtu = 1500

new_interface.ipv4.forwarding = "True"
# print ipv4.get()

ipv6add = new_interface.ipv6.address.add('2222:2222:2222:2222:2222:2222:2222:2222')
new_interface.ipv6.enabled = "True"
new_interface.ipv6.forwarding = "True"
new_interface.ipv6.dup_addr_detect_transmits = 1
new_interface.ipv6.mtu = 1500
new_interface.ipv6.autoconf.create_global_addresses = "True"
new_interface.ipv6.autoconf.create_temporary_addresses = "False"
new_interface.ipv6.autoconf.temporary_valid_lifetime = 604800
new_interface.ipv6.autoconf.temporary_preferred_lifetime = 86400


json_data = pybindJSON.dumps(model, mode='ietf')

with open('interface.json', 'w') as f:
     f.write(json_data)
