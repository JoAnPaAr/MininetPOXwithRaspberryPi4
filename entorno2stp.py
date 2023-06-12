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
    
    info('***Create a network...\n')
    #Se indica el tipo de conexion que sera Link y el tipo de conmutador que sera switchOvs
    net = Mininet( controller=Controller, link=TCLink, switch=OVSKernelSwitch )
    
    #Se crea una instancia del controlador con la IP del dispositivo en el que se va a ejecutar
    #el controlador
    c0 = net.addController('c0', controller=RemoteController, ip='192.168.1.151', port=6633 )
    
    info('*** Add switches\n')
    #Se crea una instancia de Switch
    s21 = net.addSwitch('s21')
    s22 = net.addSwitch('s22')
    s23 = net.addSwitch('s23')
    s24 = net.addSwitch('s24')
    s25 = net.addSwitch('s25')

    info('*** Add hosts\n')
    #Se crean los terminales de la topologia
    h21 = net.addHost('h21',cls=Host, ip='10.0.0.75/24')
    h22 = net.addHost('h22',cls=Host, ip='10.0.0.76/24')
    h23 = net.addHost('h23',cls=Host, ip='10.0.0.77/24')
    h24 = net.addHost('h24',cls=Host, ip='10.0.0.78/24')

    info('*** Add links\n')
    #Se vinculan las terminales al switch de la topologia
    net.addLink(s21,h21)
    net.addLink(s22,h22)
    net.addLink(s23,h23)
    net.addLink(s23,h24)
    net.addLink(s21,s22)
    net.addLink(s21,s23)
    net.addLink(s22,s23)
    net.addLink(s21,s24)
    net.addLink(s24,s23)
    net.addLink(s25,s23)
    net.addLink(s24,s25)
    net.addLink(s22,s24)
    
    info('*** Starting controllers\n')
    #Conecta la topologia al controlador
    c0.start()

    info('*** Creating interfaces\n')
    #Se indica al conmutador cual es el controlador al que debe conectarse
    s21.start([c0])
    s22.start([c0])
    s23.start([c0])
    s24.start([c0])
    s25.start([c0])

    #Creando el tunel GRE entre la raspberry actual y raspberry1
    s21.cmd("ip link add s21-tfg1 type gretap local 192.168.1.152 remote 192.168.1.151 ttl 64")
    s21.cmd("ip link set s21-tfg1 up")
    
    #Anyadiendo las interfaces al switch de la topologia
    Intf("s21-tfg1",node=s21)
    net.start()
    CLI(net)
    
    info('***Stopping network')
    #Elimina las interfaces que se han creado para esta topologia
    s21.cmd("ip link del dev s21-tfg1")
    net.stop()
    
if __name__ == '__main__':
    setLogLevel( 'info' )
    myNetwork()
