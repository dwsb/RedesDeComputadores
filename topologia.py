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
        s4=self.addSwitch('s4')
        s5=self.addSwitch('s5')
 
        h1=self.addHost('h1', ip='10.0.0.1/24')
        h2=self.addHost('h2', ip='10.0.0.2/24')
        h3=self.addHost('h3', ip='10.0.0.3/24')
        h4=self.addHost('h4', ip='10.0.0.4/24')
        h5=self.addHost('h5', ip='10.0.0.5/24')
        h6=self.addHost('h6', ip='10.0.0.6/24')
	h7=self.addHost('h7', ip='10.0.0.7/24')
	h8=self.addHost('h8', ip='10.0.0.8/24')
	h9=self.addHost('h9', ip='10.0.0.9/24')
	h10=self.addHost('h10', ip='10.0.0.10/24')

	self.addLink(s1, h10, bw=100, delay='1ms', loss=0.5, max_queue_size=100, use_htd=True)         
        self.addLink(s1, s2, bw=100, delay='1ms', loss=0.5, max_queue_size=100, use_htd=True)
	self.addLink(s1, s3, bw=100, delay='1ms', loss=0.5, max_queue_size=100, use_htd=True)
	self.addLink(s1, s4, bw=100, delay='1ms', loss=0.5, max_queue_size=100, use_htd=True)
	self.addLink(s1, s5, bw=100, delay='1ms', loss=0.5, max_queue_size=100, use_htd=True)

        self.addLink(s2, h1, bw=100, delay='1ms', loss=1, max_queue_size=100, use_htb=True) 
        self.addLink(s2, h2, bw=100, delay='1ms', loss=1, max_queue_size=100, use_htb=True)

	self.addLink(s3, h3, bw=100, delay='1ms', loss=1, max_queue_size=100, use_htb=True)        
 	self.addLink(s3, h4, bw=100, delay='1ms', loss=1, max_queue_size=100, use_htb=True)
  	
	self.addLink(s4, h5, bw=100, delay='1ms', loss=1, max_queue_size=100, use_htb=True)
 	self.addLink(s4, h6, bw=100, delay='1ms', loss=1, max_queue_size=100, use_htb=True)
	
	self.addLink(s5, h7, bw=100, delay='1ms', loss=1, max_queue_size=100, use_htb=True)
 	self.addLink(s2, h8, bw=100, delay='1ms', loss=1, max_queue_size=100, use_htb=True)
 	self.addLink(s2, h9, bw=100, delay='1ms', loss=1, max_queue_size=100, use_htb=True)

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
    h4=net.get('h4')
    h5=net.get('h5')
    h6=net.get('h6')
    h7=net.get('h7')
    h8=net.get('h8')
    h9=net.get('h9')
    h10=net.get('h10')
    h1.setMAC("0:0:0:0:0:1")
    h2.setMAC("0:0:0:0:0:2")
    h3.setMAC("0:0:0:0:0:3")
    h4.setMAC("0:0:0:0:0:4")
    h5.setMAC("0:0:0:0:0:5")
    h6.setMAC("0:0:0:0:0:6")
    h7.setMAC("0:0:0:0:0:7")
    h8.setMAC("0:0:0:0:0:8")
    h9.setMAC("0:0:0:0:0:9")
    h10.setMAC("0:0:0:0:0:10")	
    info( '\n' )
    info( "*** Starting iperf Measurement ***\n" )
    info( '\n' )
    info( "*** Stop old iperf server ***" )
    os.system('pkill -f \'iperf -s\'')
    sleep(1)
    info( '\n' )
    info( "*** Running test with iperf ***\n" )


 #   it = IPerfAllTest(net.hosts)
 #   it.start()

    CLI(net)
    net.stop()

    
if __name__ == '__main__':
    setLogLevel('info')
    configureNetwork()
