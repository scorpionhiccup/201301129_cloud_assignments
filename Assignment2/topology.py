#!/usr/bin/python

from mininet.topo import Topo
from mininet.net import Mininet
from mininet.util import dumpNodeConnections
from mininet.log import setLogLevel
from mininet.cli import CLI
from mininet.node import RemoteController, Controller, OVSSwitch

class CustomTopo(Topo):
    '''Custom Topology'''
    def build(self, no_switches=3):
        switches = []
        for switch_count in range(1, no_switches+1):
            switches.append(self.addSwitch('S' + str(switch_count)))
            
            host = self.addHost('H%s' % (2*switch_count))
            self.addLink(host, switches[switch_count-1])            
            host = self.addHost('H%s' % (2*switch_count - 1))
            self.addLink(host, switches[switch_count-1])
        

        for i in range(no_switches-1):
            for j in range(i+1, no_switches):
                self.addLink(switches[i], switches[j])                
                #self.addLink(switches[j], switches[i])

        '''
        for switch_count in range(no_switches):
            for j in range(switch_count+1, no_switches):
                print j
            print switch_count, j
        '''
            

def main():
    #no_hosts = raw_input("No. of hosts: ")
    no_switches = int(raw_input("No. of switches: "))
    #topo = CustomTopo(no_hosts, no_switches)
    topo = CustomTopo(no_switches)
    net = Mininet(topo, switch=OVSSwitch )
    net.start()    
    print "Dumping host connections"
    dumpNodeConnections(net.hosts)
    print "Testing network connectivity"
    net.pingAll()
    #CLI( net )
    net.stop()

if __name__ == '__main__':
    # Tell mininet to print useful information
    setLogLevel('info')
    main()
