# from mininet.net import Mininet
# from mininet.node import RemoteController, OVSSwitch
# from mininet.cli import CLI
# from mininet.log import setLogLevel

# def createNetwork():
#     net = Mininet(switch=OVSSwitch)

#     # Add controllers
#     c1 = net.addController('c1', controller=RemoteController, ip='127.0.0.1', port=6633)
#     c2 = net.addController('c2', controller=RemoteController, ip='127.0.0.1', port=6634)
#     c3 = net.addController('c3', controller=RemoteController, ip='127.0.0.1', port=6635)
    
#     # Add switches with OpenFlow 13
#     switches = []
#     for i in range(5):
#         switch = net.addSwitch(f's{i+1}', protocols='OpenFlow13')
#         switches.append(switch)
    
#     # Add hosts and connect them
#     hosts = []
#     for i in range(30):
#         host = net.addHost(f'h{i+1}')
#         hosts.append(host)
#         # Connect each host to two switches for redundancy
#         switch_index1 = i % 5
#         switch_index2 = (i + 3) % 5
#         net.addLink(host, switches[switch_index1])
#         net.addLink(host, switches[switch_index2])
    
#     # Connect switches in mesh topology
#     for i in range(len(switches)):
#         for j in range(i + 1, len(switches)):
#             net.addLink(switches[i], switches[j])
    
#     # Build network
#     net.build()
    
#     # Start controllers
#     c1.start()
#     c2.start()
#     c3.start()
    
#     # Start switches with controller assignments
#     switches[0].start([c1, c2])
#     switches[1].start([c1, c2])
#     switches[2].start([c2, c3])
#     switches[3].start([c2, c3])
#     switches[4].start([c1, c3])
    
#     # Enable STP on all switches
#     for switch in switches:
#         switch.cmd('ovs-vsctl set Bridge', switch, 'stp_enable=true')
    
#     net.start()
#     CLI(net)
#     net.stop()

# if __name__ == '__main__':
#     setLogLevel('info')
#     createNetwork()


from mininet.net import Mininet
from mininet.node import RemoteController, OVSSwitch
from mininet.cli import CLI
from mininet.link import TCLink
from mininet.log import setLogLevel
from time import sleep

def createNetwork():
    # Initialize the network with specific switch and link types
    net = Mininet(switch=OVSSwitch, link=TCLink)

    # Add controllers
    c1 = net.addController('c1', controller=RemoteController, ip='127.0.0.1', port=6633)
    c2 = net.addController('c2', controller=RemoteController, ip='127.0.0.1', port=6634)
    c3 = net.addController('c3', controller=RemoteController, ip='127.0.0.1', port=6635)

    # Add switches with OpenFlow 13 protocol
    switches = []
    for i in range(5):
        switch = net.addSwitch(f's{i+1}', protocols='OpenFlow13')
        switches.append(switch)

    # Add hosts and connect them to switches
    hosts = []
    for i in range(30):
        host = net.addHost(f'h{i+1}')
        hosts.append(host)
        # Connect each host to two switches for redundancy
        switch_index1 = i % 5
        switch_index2 = (i + 3) % 5
        net.addLink(host, switches[switch_index1])
        net.addLink(host, switches[switch_index2])

    # Connect switches in a mesh topology
    for i in range(len(switches)):
        for j in range(i + 1, len(switches)):
            net.addLink(switches[i], switches[j])

    # Build the network
    net.build()

    # Start the controllers
    c1.start()
    c2.start()
    c3.start()

    # Start switches and assign them to controllers
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

    # Start the CLI for interaction
    CLI(net)

    # Stop the network after CLI exit
    net.stop()

if __name__ == '__main__':
    setLogLevel('info')
    createNetwork()



# Changes Made from 1 and 2nd code is this:

#     Used Mininet(switch=OVSSwitch, link=TCLink) to specify switch and link types.
#     Set protocols='OpenFlow13' for each switch.
#     Called net.build() before starting controllers and switches.
#     Explicitly started controllers with c1.start(), c2.start(), and c3.start().
#     Enabled STP on switches using ovs-vsctl.
#     Added a sleep(10) to wait for STP convergence.