from mininet.net import Mininet
from mininet.node import RemoteController, OVSSwitch
from mininet.cli import CLI
from mininet.link import TCLink
from mininet.log import setLogLevel
from time import sleep

def createNetwork():
    net = Mininet(switch=OVSSwitch, link=TCLink)
    
    # Add controllers with specific control domains
    c1 = net.addController('c1', controller=RemoteController, ip='127.0.0.1', port=6633)
    c2 = net.addController('c2', controller=RemoteController, ip='127.0.0.1', port=6634)
    c3 = net.addController('c3', controller=RemoteController, ip='127.0.0.1', port=6635)
    
    # Add switches with OpenFlow 13
    switches = []
    for i in range(5):
        switch = net.addSwitch(f's{i+1}', protocols='OpenFlow13')
        switches.append(switch)
    
    # Add hosts and connect them
    hosts = []
    for i in range(20):
        host = net.addHost(f'h{i+1}')
        hosts.append(host)
        # Connect each host to two switches for redundancy
        switch_index1 = i % 5
        switch_index2 = (i + 2) % 5  # Changed pattern for better distribution
        net.addLink(host, switches[switch_index1])
        net.addLink(host, switches[switch_index2])
    
    # Connect switches in mesh topology
    for i in range(len(switches)):
        for j in range(i + 1, len(switches)):
            net.addLink(switches[i], switches[j])
    
    # Build network
    net.build()
    
    # Start controllers
    c1.start()
    c2.start()
    c3.start()
    
    # Start switches with controller assignments
    switches[0].start([c1, c2])
    switches[1].start([c1, c2])
    switches[2].start([c2, c3])
    switches[3].start([c2, c3])
    switches[4].start([c1, c3])
    
    # Enable STP on all switches
    for switch in switches:
        switch.cmd('ovs-vsctl set Bridge', switch, 'stp_enable=true')
    
    # Wait for STP to converge
    sleep(10)
    
    # Return the network for further manipulation or testing
    return net

if __name__ == '__main__':
    setLogLevel('info')
    net = createNetwork()
    CLI(net)
    net.stop()
