"""
 Copyright 2024 Computer Networks Group @ UPB

 Licensed under the Apache License, Version 2.0 (the "License");
 you may not use this file except in compliance with the License.
 You may obtain a copy of the License at

      https://www.apache.org/licenses/LICENSE-2.0

 Unless required by applicable law or agreed to in writing, software
 distributed under the License is distributed on an "AS IS" BASIS,
 WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 See the License for the specific language governing permissions and
 limitations under the License.
 """

#!/usr/bin/python

from mininet.topo import Topo
from mininet.link import TCLink


class StarTopo(Topo):
    def __init__(self):

        Topo.__init__(self)

        # TODO: add nodes and links to construct the topology
        
        # Handles to our network nodes
        s1 = self.addSwitch('s1')
        h1 = self.addHost('h1', ip='10.0.0.1', mac='00:00:00:00:00:01')
        h2 = self.addHost('h2', ip='10.0.0.2', mac='00:00:00:00:00:02')
        h3 = self.addHost('h3', ip='10.0.0.3', mac='00:00:00:00:00:03')

        # Connect the nodes
        #
        # TCLink: veth pair with traffic control: (bw,delay,jitter,loss,max_queue_size)
        #   Link: just a veth pair
        self.addLink(s1, h1, cls=TCLink, bw=10, delay='5ms')
        self.addLink(s1, h2, cls=TCLink, bw=10, delay='5ms')
        self.addLink(s1, h3, cls=TCLink, bw=10, delay='5ms')

topos = {'star': (lambda: StarTopo())}