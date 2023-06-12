#!/usr/bin/python
from mininet.net import Mininet
from mininet.node import Controller, RemoteController, OVSController
from mininet.node import CPULimitedHost, Host, Node
from mininet.node import OVSKernelSwitch, UserSwitch
from mininet.node import IVSSwitch
from mininet.cli import CLI
from mininet.log import setLogLevel, info
from mininet.link import TCLink, Intf
from subprocess import call

def myNetwork():
    "Create a network."
    net = Mininet( controller=Controller, link=TCLink, switch=OVSKernelSwitch )
    
    c0 = net.addController('c0', controller=RemoteController, ip='192.168.1.151', port=6633 )
    
    info('*** Add switches\n')
    s1 = net.addSwitch('s1')
    
    info('*** Add routers\n')
    r1 = net.addHost('r1', ip='192.168.2.1/24')
    
    info('*** Add hosts\n')
    h1 = net.addHost('h1',cls=Host, ip='192.168.2.10/24',defaultRoute='192.168.2.1/24')
    
    info('*** Add links\n')
    net.addLink(h1,s1)
    net.addLink(s1,r1)
    link_r1_s1 = net.addLink(r1,s1)
    
    info('*** Starting network\n')
    net.build()
    info('*** Starting controllers\n')
    for controller in net.controllers:
        controller.start

    info('*** Creating interfaces\n')
    link_r1_s1.intf1.setIP('192.168.2.1/24')
    net.get('s1').start([c0])
    CLI(net)
    net.stop()
    
if __name__ == '__main__':
    setLogLevel( 'info' )
    myNetwork()
    
    
