from mininet.net import Mininet
from mininet.node import RemoteController
from mininet.cli import CLI
from mininet.link import TCLink

net = Mininet(controller=None, link=TCLink)

# Adding controllers (6 controllers instead of 3)
c1 = net.addController('c1', controller=RemoteController, ip='127.0.0.1', port=6633)
c2 = net.addController('c2', controller=RemoteController, ip='127.0.0.1', port=6634)
c3 = net.addController('c3', controller=RemoteController, ip='127.0.0.1', port=6635)
c4 = net.addController('c4', controller=RemoteController, ip='127.0.0.1', port=6636)
c5 = net.addController('c5', controller=RemoteController, ip='127.0.0.1', port=6637)
c6 = net.addController('c6', controller=RemoteController, ip='127.0.0.1', port=6638)

# Adding switches (30 switches instead of 15)
switches = []
for i in range(1, 31):  # Adjusting the number of switches to 30
    switch = net.addSwitch(f's{i}', protocols='OpenFlow13')
    switch.start([c1, c2, c3, c4, c5, c6])  # Assigning all 6 controllers
    switches.append(switch)

# Adding hosts (100 hosts as previously)
hosts = []
for i in range(1, 101):  # Creating 100 hosts
    host = net.addHost(f'h{i}', ip=f'10.0.0.{i}/24')
    hosts.append(host)

# Creating tree topology (connecting switches)
for i in range(1, 30):  # Adjusting the tree links to 30 switches
    net.addLink(switches[i], switches[(i-1)//2])

# Connecting hosts to switches
# Distribute 100 hosts across 30 switches
host_count = 100
switch_count = len(switches)
hosts_per_switch = host_count // switch_count  # The basic number of hosts per switch

# Distribute hosts across the switches
host_idx = 0
for switch in switches:
    for _ in range(hosts_per_switch):
        if host_idx < host_count:
            net.addLink(hosts[host_idx], switch)
            host_idx += 1

# If there are remaining hosts (since 100 isn't evenly divisible by 30), distribute them
remaining_hosts = host_count % switch_count
for i in range(remaining_hosts):
    net.addLink(hosts[host_idx], switches[i])
    host_idx += 1

net.start()
CLI(net)
net.stop()
