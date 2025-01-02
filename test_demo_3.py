from mininet.topo import Topo
from mininet.net import Mininet
from mininet.node import Controller
from mininet.link import TCLink
from mininet.util import dumpNodeConnections

class TreeTopo(Topo):
    def __init__(self, depth=3, fanout=5, **opts):
        """
        Create a tree topology.
        depth: how deep the tree will be
        fanout: how many switches each switch will have
        """
        Topo.__init__(self, **opts)
        
        # Create the tree with switches
        self.depth = depth
        self.fanout = fanout
        self.switches = {}

        # Create root switch
        root = self.addSwitch('s1')
        
        # Create hosts and switches
        self.createTree(root, 2, self.depth)
        
    def createTree(self, parent_switch, current_level, max_depth):
        """Recursive function to create the tree structure"""
        if current_level > max_depth:
            return
        
        num_switches = self.fanout
        parent_name = parent_switch.name
        
        # Add child switches and hosts
        for i in range(1, num_switches + 1):
            switch_name = f"s{len(self.switches) + 2}" # Increment switch id
            switch = self.addSwitch(switch_name)
            self.addLink(parent_switch, switch)
            
            # Add hosts to this switch
            for j in range(1, self.fanout + 1):
                host_name = f"h{len(self.switches) + 2}"
                host = self.addHost(host_name)
                self.addLink(switch, host)
            
            # Recursively add more switches below
            self.createTree(switch, current_level + 1, max_depth)

def run():
    topo = TreeTopo(depth=3, fanout=5)
    net = Mininet(topo=topo, controller=None, link=TCLink)
    
    # Create two controllers and connect them to the network
    controller1 = Controller('c1', port=6633)
    controller2 = Controller('c2', port=6634)
    net.addController(controller1) 
    net.addController(controller2)
    
    # Start the network
    net.start()
    
    # Dump the connections to see the network structure
    dumpNodeConnections(net.hosts)
    
    # Start Ryu controller (ensure it's running in the background)
    print("Starting Ryu Controller (use the ryu-manager command to run the controller)")
    
    # Interact with the network
    net.pingAll()
    
    # Run the network
    net.interact()
    
    # Stop the network
    net.stop()

if __name__ == '__main__':
    run()

