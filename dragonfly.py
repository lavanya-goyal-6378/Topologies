from mininet.topo import Topo
from mininet.net import Mininet
from mininet.node import Controller
from mininet.cli import CLI
from mininet.log import setLogLevel
import time

class DragonflyTopo(Topo):
    def build(self, a=2, g=3, h=1):
        """
        a: switches per group
        g: number of groups
        h: optical links per switch to other groups
        """
        switches = []
        for i in range(g):
            group_switches = []
            for j in range(a):
                sw = self.addSwitch(f'g{i}s{j}')
                group_switches.append(sw)
                switches.append(sw)

                # Add hosts to each switch
                h1 = self.addHost(f'g{i}s{j}h1')
                self.addLink(h1, sw)
            
            # Internal Group Links (Intra-group) 
            for i_idx in range(len(group_switches)):
                for j_idx in range(i_idx + 1, len(group_switches)):
                    self.addLink(group_switches[i_idx], group_switches[j_idx])

        # Global Links (Inter-group)
        for i in range(g):
            for j in range(i + 1, g):
                # Connect first switch of group i to first switch of group j
                self.addLink(f'g{i}s0', f'g{j}s0')

def run():
    topo = DragonflyTopo()
    net = Mininet(topo=topo, controller=None)
    
    net.start()
    
    print("\n[!] Configuring Dragonfly Switches...")
    for sw in net.switches:
        sw.cmd(f'ovs-vsctl set-fail-mode {sw.name} standalone')
        sw.cmd(f'ovs-vsctl set bridge {sw.name} stp_enable=true')

    time.sleep(30)
    
    print("\n[+] Testing Dragonfly Connectivity...")
    net.pingAll(timeout = 0.5)
    
    CLI(net)
    net.stop()

if __name__ == '__main__':
    setLogLevel('info')
    run()