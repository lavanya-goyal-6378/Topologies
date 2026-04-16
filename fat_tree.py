from mininet.topo import Topo
from mininet.net import Mininet
from mininet.node import Controller, OVSKernelSwitch
from mininet.log import setLogLevel
from mininet.cli import CLI

class FatTree4(Topo):
	def build(self):
		k=4
		num_pods=k
		num_core_switches = (k//2) ** 2
		cores=[]
		for i in range(num_core_switches):
            		cores.append(self.addSwitch(f'c{i+1}'))
		for p in range(num_pods):
			aggs=[]
			edges=[]
			for i in range (k//2):
				aggs.append(self.addSwitch(f'p{p}_a{i+1}'))
				edges.append(self.addSwitch(f'p{p}_e{i+1}'))
			for a in aggs:
                		for c in cores:
                    			self.addLink(a, c)
			for e in edges:
				for a in aggs:
					self.addLink(e,a)
			for i,e in enumerate(edges):
				for h_idx in range(k//2):
					h= self.addHost(f'p{p}_e{i+1}_h{h_idx+1}')
					self.addLink(h,e)

def run ():
	topo = FatTree4()
	net= Mininet(topo = topo, autoStaticArp=True)
	net.start()
	for sw in net.switches:
		sw.cmd(f'ovs-vsctl set-fail-mode {sw.name} standalone')
		sw.cmd(f'ovs-vsctl set bridge {sw.name} stp_enable=true')
	import time
	time.sleep(30)
	
	CLI(net)
	net.stop()
if __name__ == '__main__':
	setLogLevel('info')
	run()
