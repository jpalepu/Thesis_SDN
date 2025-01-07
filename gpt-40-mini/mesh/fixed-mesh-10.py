# # from mininet.net import Mininet
# # from mininet.node import RemoteController
# # from mininet.cli import CLI
# # from mininet.log import setLogLevel
# # from time import sleep

# # def create_mesh_network(host_count=10, switch_count=5):
# #     """Create a full mesh topology network with specified hosts and switches."""
# #     net = Mininet()

# #     # Define controllers
# #     controllers = {
# #         'c1': ('127.0.0.1', 6633),
# #         'c2': ('127.0.0.1', 6634),
# #         'c3': ('127.0.0.1', 6635)
# #     }
    
# #     for name, (ip, port) in controllers.items():
# #         net.addController(name, controller=RemoteController, ip=ip, port=port)

# #     # # Add switches
# #     switches = [net.addSwitch(f's{i}') for i in range(1, switch_count + 1)]

# #     # Add hosts and connect them to multiple switches for redundancy
# #     hosts = []
# #     for i in range(1, host_count + 1):
# #         host = net.addHost(f'h{i}')
# #         hosts.append(host)
# #         switch1 = switches[i % switch_count]
# #         switch2 = switches[(i + 1) % switch_count]
# #         net.addLink(host, switch1)
# #         net.addLink(host, switch2)

# #     # Connect switches in a full mesh topology
# #     for i in range(len(switches)):
# #         for j in range(i + 1, len(switches)):
# #             net.addLink(switches[i], switches[j])

# #     # Assign switches to controllers for redundancy
# #     for i, switch in enumerate(switches):
# #         if i < 2:
# #             switch.start([net.get('c1'), net.get('c2')])
# #         elif i < 4:
# #             switch.start([net.get('c2'), net.get('c3')])
# #         else:
# #             switch.start([net.get('c1'), net.get('c3')])

# #     # Enable STP on switches to prevent loops
# #     for switch in switches:
# #         switch.cmd('ovs-vsctl set Bridge', switch, 'stp_enable=true')

# #     # Wait for STP to converge
# #     sleep(10)

# #     net.start()
# #     CLI(net)
# #     net.stop()

# # if __name__ == '__main__':
# #     setLogLevel('info')
# #     create_mesh_network()



# from mininet.net import Mininet
# from mininet.node import RemoteController, OVSSwitch
# from mininet.cli import CLI
# from mininet.link import TCLink
# from mininet.log import setLogLevel
# from time import sleep

# def create_mesh_network(host_count=10, switch_count=5):
#     """Create a full mesh topology network with specified hosts and switches."""
#     net = Mininet(switch=OVSSwitch, link=TCLink)

#     # Define controllers
#     print("*** Creating controllers")
#     controllers = {
#         'c1': ('127.0.0.1', 6633),
#         'c2': ('127.0.0.1', 6634),
#         'c3': ('127.0.0.1', 6635)
#     }
    
#     for name, (ip, port) in controllers.items():
#         net.addController(name, controller=RemoteController, ip=ip, port=port)

#     # Add switches with OpenFlow 13
#     print("*** Creating switches")
#     switches = [net.addSwitch(f's{i}', protocols='OpenFlow13') for i in range(1, switch_count + 1)]

#     # Add hosts and connect them to multiple switches for redundancy
#     print("*** Creating hosts and connecting them")
#     hosts = []
#     for i in range(1, host_count + 1):
#         host = net.addHost(f'h{i}', ip=f'10.0.0.{i}/24')
#         hosts.append(host)
#         switch1 = switches[i % switch_count]
#         switch2 = switches[(i + 1) % switch_count]
#         net.addLink(host, switch1)
#         net.addLink(host, switch2)

#     # Connect switches in a full mesh topology
#     print("*** Creating mesh connections between switches")
#     for i in range(len(switches)):
#         for j in range(i + 1, len(switches)):
#             net.addLink(switches[i], switches[j])

#     # Build network
#     net.build()

#     # Start controllers
#     print("*** Starting controllers")
#     for name in controllers:
#         net.get(name).start()

#     # Start switches with controller assignments
#     print("*** Starting switches with controller assignments")
#     for i, switch in enumerate(switches):
#         if i < 2:
#             switch.start([net.get('c1'), net.get('c2')])
#         elif i < 4:
#             switch.start([net.get('c2'), net.get('c3')])
#         else:
#             switch.start([net.get('c1'), net.get('c3')])

#     # Enable STP on switches to prevent loops
#     print("*** Enabling STP on switches")
#     for switch in switches:
#         switch.cmd('ovs-vsctl set Bridge', switch, 'stp_enable=true')

#     # Wait for STP to converge
#     print("*** Waiting for STP convergence...")
#     sleep(10)

#     print("*** Network is ready")
#     net.start()
#     CLI(net)
#     net.stop()

# if __name__ == '__main__':
#     setLogLevel('info')
#     create_mesh_network()



from mininet.net import Mininet
from mininet.node import RemoteController, OVSSwitch
from mininet.cli import CLI
from mininet.link import TCLink
from mininet.log import setLogLevel
from time import sleep

def create_mesh_network(host_count=10, switch_count=5):
    """Create a full mesh topology network with specified hosts and switches."""
    # Initialize Mininet with OVSSwitch and TCLink
    net = Mininet(switch=OVSSwitch, link=TCLink)

    # Define controllers
    controllers = {
        'c1': ('127.0.0.1', 6633),
        'c2': ('127.0.0.1', 6634),
        'c3': ('127.0.0.1', 6635)
    }
    
    # Add controllers
    for name, (ip, port) in controllers.items():
        net.addController(name, controller=RemoteController, ip=ip, port=port)

    # Add switches with OpenFlow 13 protocol
    switches = [net.addSwitch(f's{i}', protocols='OpenFlow13') for i in range(1, switch_count + 1)]

    # Add hosts and connect them to switches for redundancy
    hosts = [net.addHost(f'h{i}', ip=f'10.0.0.{i}/24') for i in range(1, host_count + 1)]
    for i, host in enumerate(hosts):
        switch1 = switches[i % switch_count]
        switch2 = switches[(i + 1) % switch_count]
        net.addLink(host, switch1)
        net.addLink(host, switch2)

    # Connect switches in a full mesh topology
    for i in range(len(switches)):
        for j in range(i + 1, len(switches)):
            net.addLink(switches[i], switches[j])

    # Build the network before starting controllers and switches
    net.build()

    # Start controllers
    for controller in net.controllers:
        controller.start()

    # Start switches with controller assignments for redundancy
    for i, switch in enumerate(switches):
        if i < 2:
            switch.start([net.get('c1'), net.get('c2')])
        elif i < 4:
            switch.start([net.get('c2'), net.get('c3')])
        else:
            switch.start([net.get('c1'), net.get('c3')])

    # Enable STP on switches to prevent loops
    for switch in switches:
        switch.cmd('ovs-vsctl set Bridge', switch, 'stp_enable=true')

    # Wait for STP to converge
    sleep(10)

    # Start the network
    net.start()
    CLI(net)
    net.stop()

if __name__ == '__main__':
    setLogLevel('info')
    create_mesh_network()
