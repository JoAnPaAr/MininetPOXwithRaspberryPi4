#!/usr/bin/env python

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

    net = Mininet( controller=Controller, link=TCLink, switch=OVSKernelSwitch)

    info( '*** Adding controller\n' )
    c0=net.addController(name='c0',
                      controller=RemoteController,
                      ip='192.168.1.151',
                      protocol='tcp',
                      port=6633)

    info( '*** Add switches\n')
    s2 = net.addSwitch('s2')

    info( '*** Add hosts\n')
    h2 = net.addHost('h2', cls=Host, ip='192.168.3.10/24', defaultRoute='192.168.3.1')

    info( '*** Add links\n')
    net.addLink(h2,s2)

    gre_intf = net.addLink(s2,h2,intfName2='gre1', params2={'type':'gretap'})
    gre_intf.intf1.cmd('ip link set dev gre1 up')
    gre_intf.intf1.cmd('ip addr add 10.0.0.2/24 dev gre1')
    
    gre_intf.intf1.cmd('ip addr add 192.168.3.1/24 dev gre1')
    
    s2.cmd('ovs-vsctl add-port s2 gre1 -- set interface gre1 type=gretap options:remote_ip=192.168.3.2')
    s2.cmd('ip link set dev gre1 up')
    s2.cmd('ip laddr add 192.168.3.2/24 dev gre1')
    s2.cmd('ip route add 192.168.3.0/24 dev gre1')

    info( '*** Starting network\n')
    net.build()
    info( '*** Starting controllers\n')
    for controller in net.controllers:
        controller.start
    
    info( '*** Post configure switches and hosts\n')
    info( '*** Starting switches\n')
    for switch in net.switches:
        switch.start([c0])
    CLI(net)
    info( '*** Stopping network\n')
    net.stop()

if __name__ == '__main__':
    setLogLevel( 'info' )
    myNetwork()

