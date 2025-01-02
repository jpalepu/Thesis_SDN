#In a star topology, all switches are connected to a central switch (hub). The hosts are connected to the switches.
from mininet.net import Mininet
from mininet.node import RemoteController
from mininet.cli import CLI
from mininet.link import TCLink

net = Mininet(controller=None, link=TCLink)

# Adding controllers
c1 = net.addController('c1', controller=RemoteController, ip='127.0.0.1', port=6633)
c2 = net.addController('c2', controller=RemoteController, ip='127.0.0.1', port=6634)

# Adding switches (5 switches, with one central hub)
central_switch = net.addSwitch('s1', protocols='OpenFlow13')
central_switch.start([c1, c2])

# Adding other switches (4 peripheral switches)
switches = [central_switch]
for i in range(2, 6):
    switch = net.addSwitch(f's{i}', protocols='OpenFlow13')
    switch.start([c1, c2])
    switches.append(switch)

# Adding hosts (10 hosts)
hosts = []
for i in range(1, 11):
    host = net.addHost(f'h{i}', ip=f'10.0.0.{i}/24')
    hosts.append(host)

# Star topology: Connect all switches to the central switch
for i in range(1, len(switches)):
    net.addLink(switches[0], switches[i])

# Connect hosts to switches
net.addLink(hosts[0], switches[1])
net.addLink(hosts[1], switches[1])
net.addLink(hosts[2], switches[2])
net.addLink(hosts[3], switches[2])
net.addLink(hosts[4], switches[3])
net.addLink(hosts[5], switches[3])
net.addLink(hosts[6], switches[4])
net.addLink(hosts[7], switches[4])
net.addLink(hosts[8], switches[4])
net.addLink(hosts[9], switches[4])

net.start()
CLI(net)
net.stop()
