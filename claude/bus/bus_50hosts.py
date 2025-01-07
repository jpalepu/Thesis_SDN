from mininet.net import Mininet
from mininet.node import RemoteController
from mininet.cli import CLI
from mininet.log import setLogLevel

def createNetwork():
    net = Mininet()
    
    # Add controllers with specific control domains
    c1 = net.addController('c1', controller=RemoteController, ip='127.0.0.1', port=6633)
    c2 = net.addController('c2', controller=RemoteController, ip='127.0.0.1', port=6634)
    c3 = net.addController('c3', controller=RemoteController, ip='127.0.0.1', port=6635)
    
    # Add switches
    switches = []
    for i in range(10):
        switch = net.addSwitch(f's{i+1}')
        switches.append(switch)
    
    # Add hosts and connect them
    hosts = []
    for i in range(50):
        host = net.addHost(f'h{i+1}')
        hosts.append(host)
        switch_index = i // 5  # Distribute 5 hosts per switch (50/10)
        net.addLink(host, switches[switch_index])
    
    # Connect switches in bus topology
    for i in range(len(switches)-1):
        net.addLink(switches[i], switches[i+1])
    
    # Assign switches to controllers
    switches[0].start([c1, c2])   # First switch controlled by c1 and c2
    switches[1].start([c1, c2])   # Second switch controlled by c1 and c2
    switches[2].start([c1, c2])   # Third switch controlled by c1 and c2
    switches[3].start([c2, c3])   # Fourth switch controlled by c2 and c3
    switches[4].start([c2, c3])   # Fifth switch controlled by c2 and c3
    switches[5].start([c2, c3])   # Sixth switch controlled by c2 and c3
    switches[6].start([c1, c3])   # Seventh switch controlled by c1 and c3
    switches[7].start([c1, c3])   # Eighth switch controlled by c1 and c3
    switches[8].start([c1, c3])   # Ninth switch controlled by c1 and c3
    switches[9].start([c1, c2])   # Tenth switch controlled by c1 and c2
    
    net.start()
    CLI(net)
    net.stop()

if __name__ == '__main__':
    setLogLevel('info')
    createNetwork()