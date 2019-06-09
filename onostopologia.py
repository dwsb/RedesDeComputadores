#!/usr/bin/python
 
from mininet.topo import Topo
from mininet.net import Mininet
from mininet.node import CPULimitedHost
from mininet.link import TCLink
from mininet.util import dumpNodeConnections
from mininet.log import setLogLevel, info
from mininet.node import Controller 
from mininet.cli import CLI
from functools import partial
from mininet.node import RemoteController
import os
from time import sleep
#from iperf import IPerfAllTest

class MyTopo(Topo):
    "Single switch connected to n hosts."
    def __init__(self):
        Topo.__init__(self)

        s1=self.addSwitch('s1')
        s2=self.addSwitch('s2')
        s3=self.addSwitch('s3')
 
        h1=self.addHost('h1', ip='10.0.0.1/24')
        h2=self.addHost('h2', ip='10.0.0.2/24')
        h3=self.addHost('h3', ip='10.0.0.3/24')
        server1=self.addHost('server1', ip='10.0.1.1/24')
        server2=self.addHost('server2', ip='10.0.1.2/24')
        server3=self.addHost('server3', ip='10.0.1.3/24')

	    self.addLink(s1, s2, bw=30, use_htd=True)
        self.addLink(s2, s3, bw=30, use_htd=True)
        self.addLink(s3, s1, bw=30, use_htd=True)

        self.addLink(s1, h1, bw=30, use_htd=True)
        self.addLink(s1, server1, bw=30, use_htd=True)
        
        self.addLink(s2, h2, bw=30, use_htd=True)
        self.addLink(s2, server2, bw=30, use_htd=True)

        self.addLink(s3, h3, bw=30, use_htd=True)
        self.addLink(s2, server3, bw=30, use_htd=True)


def configureNetwork():
    "Create network and run simple performance test"
    topo = MyTopo()
    #net = Mininet(topo=topo, host=CPULimitedHost, link=TCLink, controller=POXcontroller1)
    net = Mininet(topo=topo, host=CPULimitedHost, link=TCLink, controller=partial(RemoteController, ip='127.0.0.1', port=6633))
    net.start()
    print "Dumping host connections"
    dumpNodeConnections(net.hosts)
    h1=net.get('h1')
    h2=net.get('h2')
    h3=net.get('h3')
    server1=net.get('server1')
    server2=net.get('server2')
    server3=net.get('server3')
    h1.setMAC("0:0:0:0:0:1")
    h2.setMAC("0:0:0:0:0:2")
    h3.setMAC("0:0:0:0:0:3")
    server1.setMAC("0:0:0:0:0:4")
    server2.setMAC("0:0:0:0:0:5")
    server3.setMAC("0:0:0:0:0:6")
    info( '\n' )
    info( "*** Starting iperf Measurement ***\n" )
    info( '\n' )
    info( "*** Stop old iperf server ***" )
    os.system('pkill -f \'iperf -s\'')
    sleep(1)
    info( '\n' )
    info( "*** Running test with iperf ***\n" )

    
    #it = IPerfAllTest(net.hosts)
    #it.start()

    CLI(net)
    net.stop()
 
if __name__ == '__main__':
    setLogLevel('info')
    configureNetwork()
