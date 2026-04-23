from mininet.topo import Topo
from mininet.net import Mininet
from mininet.node import Controller
from mininet.cli import CLI
from mininet.log import setLogLevel
import time

def topology():
        
    net = Mininet(controller=None)
    s1=net.addSwitch('s1')
    s2=net.addSwitch('s2')
    s3=net.addSwitch('s3')
    s4=net.addSwitch('s4')
    s5=net.addSwitch('s5')
    s6=net.addSwitch('s6')
    h1 = net.addHost('h1')
    h2 = net.addHost('h2')
    h3 = net.addHost('h3')
    h4 = net.addHost('h4')
    h5 = net.addHost('h5')
    h6 = net.addHost('h6')
    net.addLink(h1,s1)
    net.addLink(h2,s2)
    net.addLink(h3,s3)
    net.addLink(h4,s4)
    net.addLink(h5,s5)
    net.addLink(h6,s6)
    net.addLink(s1,s3)
    net.addLink(s2,s3)
    net.addLink(s3,s4)
    net.addLink(s1,s2)
    net.addLink(s5,s6)
    net.addLink(s3,s5)

    net.start()
    
    print("\n[!] Configuring Dragonfly Switches...")

    s1.cmd(f'ovs-vsctl set-fail-mode s1 standalone')
    s2.cmd(f'ovs-vsctl set-fail-mode s2 standalone')
    s3.cmd(f'ovs-vsctl set-fail-mode s3 standalone')
    s4.cmd(f'ovs-vsctl set-fail-mode s4 standalone')
    s5.cmd(f'ovs-vsctl set-fail-mode s5 standalone')
    s6.cmd(f'ovs-vsctl set-fail-mode s6 standalone')

    s1.cmd(f'ovs-vsctl set Bridge s1 stp_enable=true')
    s2.cmd(f'ovs-vsctl set Bridge s2 stp_enable=true')
    s3.cmd(f'ovs-vsctl set Bridge s3 stp_enable=true')
    s4.cmd(f'ovs-vsctl set Bridge s4 stp_enable=true')
    s5.cmd(f'ovs-vsctl set Bridge s5 stp_enable=true')
    s6.cmd(f'ovs-vsctl set Bridge s6 stp_enable=true')
	
    time.sleep(30)
    print("\n[+] Testing Dragonfly Connectivity...")
    net.pingAll(timeout = 0.5)
    CLI(net)
    net.stop()
if __name__ == '__main__':
    setLogLevel('info')
    topology()