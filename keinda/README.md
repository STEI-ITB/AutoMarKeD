# Network Configuration using Bash CLI via NETCONF Protocol with YANG Data Model

Programs for network configuration via NETCONF Protocol for Cisco IOS-XR. Available for interface configuration and OSPF configuration.

## Environment Setup

To use the programs, there are some requirements that needed to be installed in the environment. Use the package manager [pip](https://pip.pypa.io/en/stable/) to install the requirements : :

```bash
pip install ncclient
pip install pyang
pip install pyangbind
```

After the requirements are installed, do pointing for [PyangBind](https://github.com/robshakir/pyangbind) with commands :

```bash
PYBINDPLUGIN=`python -c 'import pyangbind; import os; print ("{}/plugin".format(os.path.dirname(pyangbind.__file__)))'`
echo $PYBINDPLUGIN
```

## Usage

To use the program, simply use these command for each program ([interface.py](https://github.com/STEI-ITB/AutoMarKeD/blob/master/keinda/int/interface.py) and [ospf.py](https://github.com/STEI-ITB/AutoMarKeD/blob/master/keinda/ospf/ospf.py)) and make sure that the Python module and jtox driver for respective programs are available in the same folder.

```bash
python <program_name>.py -a <host_address> -p <host_port> -u <host_username> -w <host_password> -f <config_filename>.txt
```
Each config can be changed by editing or creating configuration file. For example, interface configuration and OSPF configuration respectively :

```text
interface GigabitEthernet0/0/0/0
    ipv4 address 1.1.1.1 255.255.255.0
!
interface GigabitEthernet0/0/0/1
    ipv4 address 2.2.2.1 255.255.255.0
!
```

```text
router ospf 1
    area 0
        interface GigabitEthernet0/0/0/0
        !
        interface GigabitEthernet0/0/0/1
        !
    !
!
```
