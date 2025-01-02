#!/usr/bin/env python

from mininet.net import Mininet
from mininet.node import Controller, OVSSwitch, RemoteController
from mininet.cli import CLI
from mininet.log import setLogLevel
from mininet.link import TCLink

def createNetwork():
    # Initialize Mininet
    net = Mininet(controller=RemoteController, switch=OVSSwitch, link=TCLink)
    
    # Add controllers
    c1 = net.addController('c1', controller=RemoteController, ip='127.0.0.1', port=6633)
    c2 = net.addController('c2', controller=RemoteController, ip='127.0.0.1', port=6634)
    
    # Create switches (15 switches)
    switches = []
    for i in range(15):
        switch = net.addSwitch(f's{i+1}')
        switches.append(switch)
    
    # Create hosts (30 hosts)
    hosts = []
    for i in range(30):
        host = net.addHost(f'h{i+1}')
        hosts.append(host)
    
    # Create tree topology
    # Level 1: Connect first switch to controllers
    # Level 2: Connect switches 2-5 to switch 1
    # Level 3: Connect remaining switches to level 2 switches
    
    # Level 1
    switches[0].start([c1, c2])
    
    # Level 2 connections
    for i in range(1, 5):
        net.addLink(switches[0], switches[i])
        switches[i].start([c1, c2])
    
    # Level 3 connections
    sw_index = 5
    for i in range(1, 5):
        for j in range(3):
            if sw_index < len(switches):
                net.addLink(switches[i], switches[sw_index])
                switches[sw_index].start([c1, c2])
                sw_index += 1
    
    # Connect hosts to switches
    # Distribute hosts evenly among leaf switches
    host_index = 0
    for i in range(5, len(switches)):
        hosts_per_switch = len(hosts) // (len(switches) - 5)
        for j in range(hosts_per_switch):
            if host_index < len(hosts):
                net.addLink(switches[i], hosts[host_index])
                host_index += 1
    
    # Start network
    net.build()
    net.start()
    
    return net

if __name__ == '__main__':
    setLogLevel('info')
    network = createNetwork()
    CLI(network)
    network.stop()
