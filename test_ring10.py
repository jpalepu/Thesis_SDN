from mininet.net import Mininet
from mininet.node import RemoteController
from mininet.cli import CLI
from mininet.link import TCLink

net = Mininet(controller=None, link=TCLink)

# Adding controllers (2 controllers instead of 3)
c1 = net.addController('c1', controller=RemoteController, ip='127.0.0.1', port=6633)
c2 = net.addController('c2', controller=RemoteController, ip='127.0.0.1', port=6634)

# Adding switches
switches = []
for i in range(1, 6):  # Reduced to 5 switches (as ring topology requires less switches with fewer hosts)
    switch = net.addSwitch(f's{i}', protocols='OpenFlow13')
    switch.start([c1, c2])
    switches.append(switch)

# Adding hosts (10 hosts)
hosts = []
for i in range(1, 11):
    host = net.addHost(f'h{i}', ip=f'10.0.0.{i}/24')
    hosts.append(host)

# Creating ring topology between switches
for i in range(len(switches)):
    net.addLink(switches[i], switches[(i + 1) % len(switches)])

# Connecting hosts to switches (Distribute 10 hosts across 5 switches)
net.addLink(hosts[0], switches[0])
net.addLink(hosts[1], switches[0])
net.addLink(hosts[2], switches[1])
net.addLink(hosts[3], switches[1])
net.addLink(hosts[4], switches[2])
net.addLink(hosts[5], switches[2])
net.addLink(hosts[6], switches[3])
net.addLink(hosts[7], switches[3])
net.addLink(hosts[8], switches[4])
net.addLink(hosts[9], switches[4])

net.start()
CLI(net)
net.stop()

