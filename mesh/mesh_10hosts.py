# Generated by Claude-3.5-Sonnet

from mininet.net import Mininet
from mininet.node import RemoteController
from mininet.cli import CLI
from mininet.log import setLogLevel

def createNetwork():
    net = Mininet()
    
    # Add controllers
    c1 = net.addController('c1', controller=RemoteController, ip='127.0.0.1', port=6633)
    c2 = net.addController('c2', controller=RemoteController, ip='127.0.0.1', port=6634)
    c3 = net.addController('c3', controller=RemoteController, ip='127.0.0.1', port=6635)
    
    # Add switches
    switches = []
    for i in range(5):
        switch = net.addSwitch(f's{i+1}')
        switches.append(switch)
    
    # Add hosts
    hosts = []
    for i in range(10):
        host = net.addHost(f'h{i+1}')
        hosts.append(host)
        # Connect each host to two switches for redundancy
        switch_index1 = i % 5
        switch_index2 = (i + 1) % 5
        net.addLink(host, switches[switch_index1])
        net.addLink(host, switches[switch_index2])
    
    # Connect switches in a full mesh topology
    for i in range(len(switches)):
        for j in range(i + 1, len(switches)):
            net.addLink(switches[i], switches[j])
    
    net.start()
    CLI(net)
    net.stop()

if __name__ == '__main__':
    setLogLevel('info')
    createNetwork() 