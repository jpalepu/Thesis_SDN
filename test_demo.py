from mininet.net import Mininet
from mininet.node import Controller, RemoteController
from mininet.topo import Topo
from mininet.link import TCLink
from mininet.cli import CLI
from mininet.log import setLogLevel

class TreeTopo(Topo):
    def build(self):
        # Create the root switch
        root_switch = self.addSwitch('s0')

        # List of switches to be added
        switches = []
        
        # Create the 14 additional switches
        for i in range(1, 16):
            switches.append(self.addSwitch(f's{i}'))

        # Create the tree structure, connect switches to each other
        self.addLink(root_switch, switches[0])  # Root to first switch
        self.addLink(root_switch, switches[1])  # Root to second switch
        
        # Create the rest of the tree hierarchy
        for i in range(2, 8, 2):
            self.addLink(switches[i], switches[i + 1])  # Connect pairs of switches

        # Now connect hosts to leaf switches
        hosts = []
        host_id = 1
        for i in range(7, 15, 2):
            for j in range(2):
                host = self.addHost(f'h{host_id}')
                hosts.append(host)
                self.addLink(host, switches[i + j])
                host_id += 1

def run():
    setLogLevel('info')

    # Create network with custom tree topology
    topo = TreeTopo()
    net = Mininet(topo=topo, controller=RemoteController, link=TCLink)

    # Add two controllers (on different ports)
    net.addController('c1', controller=RemoteController, ip='127.0.0.1', port=6633)
    net.addController('c2', controller=RemoteController, ip='127.0.0.1', port=6634)

    # Start the network
    net.start()

    # Start the CLI for interaction
    CLI(net)

    # Stop the network
    net.stop()

if __name__ == '__main__':
    run()

