from mininet.topo import Topo
from mininet.net import Mininet
from mininet.node import Controller, RemoteController
from mininet.cli import CLI
from mininet.log import setLogLevel

class TreeTopo(Topo):
    def __init__(self, depth=3, fanout=2, **opts):
        super(TreeTopo, self).__init__(**opts)
        self.depth = depth
        self.fanout = fanout
        self.switch_count = 0
        self.host_count = 0
        self.addTree(depth, fanout)

    def addTree(self, depth, fanout):
        if depth > 0:
            for i in range(fanout):
                switch = self.addSwitch('s{}'.format(self.switch_count))
                self.switch_count += 1
                self.addTree(depth - 1, fanout)
                if depth == 1:
                    for j in range(fanout):
                        host = self.addHost('h{}'.format(self.host_count))
                        self.host_count += 1
                        self.addLink(host, switch)

def create_network():
    topo = TreeTopo(depth=3, fanout=2)
    net = Mininet(topo=topo, controller=None)
    
    # Add Ryu controllers
    c1 = net.addController('c1', controller=RemoteController, ip='127.0.0.1', port=6633)
    c2 = net.addController('c2', controller=RemoteController, ip='127.0.0.1', port=6634)
    
    net.start()
    CLI(net)
    net.stop()

if __name__ == '__main__':
    setLogLevel('info')
    create_network()
