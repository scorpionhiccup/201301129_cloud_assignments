#!/usr/bin/python
from mininet.net import Mininet
from mininet.util import dumpNodeConnections, irange
from mininet.log import setLogLevel
from mininet.cli import CLI
from mininet.link import TCLink
from mininet.node import Controller, CPULimitedHost

class CustomTopology():
    '''Custom Topology'''
    def __init__(self, no_hosts ,no_switches):
        self.no_hosts = no_hosts
        self.no_switches = no_switches
        self.mininet_obj = Mininet(controller=Controller, link=TCLink)

    def build(self):
        self.mininet_obj.addController( 'c0' )
        switches = []
        hosts = []

        #self.addController( 'c0' )
        odd_ip='11.0.0.'
        even_ip='11.0.1.'

        #Add All Hosts
        count, count2 = 1, 1
        for host_count in range(self.no_hosts*self.no_switches):
            if host_count%2:
                hosts.append(self.mininet_obj.addHost('h%s' % (host_count+1), ip=odd_ip + str(count) + '/24'))
                count+=1
            else:
                hosts.append(self.mininet_obj.addHost('h%s' % (host_count+1), ip=even_ip + str(count2)+ '/24'))
                count2+=1
            #count+=1

        #Add All Switches
        for switch_count in range(self.no_hosts):
            switches.append(self.mininet_obj.addSwitch('s%s' % (switch_count+1)))

        for switch_no in range(self.no_switches):
            for host_no in range(self.no_hosts):
                self.mininet_obj.addLink( hosts[self.no_hosts*switch_no+host_no], switches[switch_no], bw=2-host_no%2)

        #Connect the Switches in a ring-like topology.
        for switch_no in range(self.no_hosts-1):
            print switch_no
            self.mininet_obj.addLink(switches[switch_no], switches[switch_no+1], bw=2) 

    def run(self):
        self.mininet_obj.start()
        print "Dumping host connections"
        dumpNodeConnections(self.mininet_obj.hosts)
        print "Testing network connectivity"
        self.mininet_obj.pingAll()
        CLI( self.mininet_obj )
        self.mininet_obj.stop()

            
def main():
    no_hosts = int(raw_input("No. of hosts: "))
    no_switches = int(raw_input("No. of switches: "))
    topo_obj = CustomTopology(no_hosts, no_switches)
    topo_obj.build()
    topo_obj.run()

if __name__ == '__main__':
    # Tell mininet to print useful information
    setLogLevel( 'info' )
    main()
