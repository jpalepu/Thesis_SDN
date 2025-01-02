from mininet.topo import Topo
from mininet.net import Mininet
from mininet.node import OVSSwitch, RemoteController
from mininet.cli import CLI
from mininet.log import setLogLevel

class TreeTopo(Topo):
    def build(self):
        # Number of hosts and switches
        num_hosts = 30
        num_switches = 15
        
        # Create root switch
        root_switch = self.addSwitch('s1')

        # Create intermediate switches and hosts
        switch_id = 2  # Starting switch number
        hosts_per_switch = num_hosts // 2  # Hosts to distribute among switches
        for i in range(1, num_switches + 1):
            switch = self.addSwitch(f's{i + 1}')
            # Create a host connected to each switch
            for h in range(hosts_per_switch):
                host = self.addHost(f'h{(i - 1) * hosts_per_switch + h + 1}')
                self.addLink(host, switch)

            # Create links from root to child switches
            if i <= 7:
                self.addLink(root_switch, switch)

        # Add links between switches to form the tree structure
        for i in range(2, num_switches + 1):
            parent_switch = self.getSwitch(i // 2)  # Parent switch
            self.addLink(parent_switch, self.getSwitch(i))  # Add link from parent to child

def run():
    setLogLevel('info')

    # Create the network with Mininet
    topo = TreeTopo()
    net = Mininet(topo=topo, controller=None)

    # Add two remote Ryu controllers
    controller1 = net.addController('c1', controller=RemoteController, ip='127.0.0.1', port=6653)
    controller2 = net.addController('c2', controller=RemoteController, ip='127.0.0.1', port=6654)

    # Start the network
    net.start()

    # Run CLI for interaction with the network
    CLI(net)

    # Stop the network
    net.stop()

if __name__ == '__main__':
    run()

