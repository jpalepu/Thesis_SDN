#!/usr/bin/env python

from mininet.net import Mininet
from mininet.node import RemoteController
from mininet.cli import CLI
from mininet.link import TCLink

# Initialize network
net = Mininet(controller=None, link=TCLink)

# Adding controllers
c1 = net.addController('c1', controller=RemoteController, ip='127.0.0.1', port=6633)
c2 = net.addController('c2', controller=RemoteController, ip='127.0.0.1', port=6634)

# Adding switches (5 switches)
switches = []
for i in range(1, 6):
    switch = net.addSwitch(f's{i}', protocols='OpenFlow13')
    switches.append(switch)
    
# Start switches and connect to controllers immediately
for switch in switches:
    switch.start([c1, c2])

# Adding hosts (10 hosts)
hosts = []
for i in range(1, 11):
    host = net.addHost(f'h{i}', ip=f'10.0.0.{i}/24')
    hosts.append(host)

# Mesh topology: Connect every switch to every other switch
for i in range(len(switches)):
    for j in range(i + 1, len(switches)):
        net.addLink(switches[i], switches[j])

# Connect hosts to switches (two hosts per switch)
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

# Start network
net.start()
CLI(net)
net.stop()