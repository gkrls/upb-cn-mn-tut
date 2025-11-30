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

from ryu.base import app_manager
from ryu.controller import ofp_event
from ryu.controller.handler import CONFIG_DISPATCHER, MAIN_DISPATCHER
from ryu.controller.handler import set_ev_cls
from ryu.ofproto import ofproto_v1_3
from ryu.lib.packet import packet
from ryu.lib.packet import ethernet
from ryu.lib.packet import arp
from ryu.lib.packet import ipv4

class LearningSwitch(app_manager.RyuApp):
    OFP_VERSIONS = [ofproto_v1_3.OFP_VERSION]

    def __init__(self, *args, **kwargs):
        super(LearningSwitch, self).__init__(*args, **kwargs)

        # Initialize mac forwarding table
        self.mac_to_port = {}

    @set_ev_cls(ofp_event.EventOFPSwitchFeatures, CONFIG_DISPATCHER)
    def switch_features_handler(self, ev):
        
        datapath = ev.msg.datapath
        ofproto = datapath.ofproto
        parser = datapath.ofproto_parser

        #
        # 1. Table-miss flow with lowest priority (0) → Send to controller
        #
        match = parser.OFPMatch()
        actions = [parser.OFPActionOutput(ofproto.OFPP_CONTROLLER, ofproto.OFPCML_NO_BUFFER)]
        self.add_flow(datapath, 0, match, actions)

        #
        # 2. Static flows with higher priority (1) → Send to known port (NB: NOT the solution to your assignment)
        # 
        self.add_flow(datapath, 1, parser.OFPMatch(eth_dst="00:00:00:00:00:01"), [parser.OFPActionOutput(1)])
        self.add_flow(datapath, 1, parser.OFPMatch(eth_dst="00:00:00:00:00:02"), [parser.OFPActionOutput(2)])
        self.add_flow(datapath, 1, parser.OFPMatch(eth_dst="00:00:00:00:00:03"), [parser.OFPActionOutput(3)])

        #
        # 3. Flood flows
        #
        self.add_flow(datapath, 1, parser.OFPMatch(eth_dst="ff:ff:ff:ff:ff:ff"), [parser.OFPActionOutput(ofproto.OFPP_FLOOD)])
        self.add_flow(datapath, 1, parser.OFPMatch(eth_dst=("33:33:00:00:00:00", "ff:ff:00:00:00:00")), [parser.OFPActionOutput(ofproto.OFPP_FLOOD)])

    # Add a flow entry to the switch table
    def add_flow(self, datapath, priority, match, actions):
        ofproto = datapath.ofproto
        parser = datapath.ofproto_parser

        # Construct flow_mod message and send it
        inst = [parser.OFPInstructionActions(ofproto.OFPIT_APPLY_ACTIONS, actions)]
        mod = parser.OFPFlowMod(datapath=datapath, priority=priority, match=match, instructions=inst)
        datapath.send_msg(mod)

    # Handle the packet_in event
    @set_ev_cls(ofp_event.EventOFPPacketIn, MAIN_DISPATCHER)
    def _packet_in_handler(self, ev):
        
        msg = ev.msg
        datapath = msg.datapath
        ofproto = datapath.ofproto
        parser = datapath.ofproto_parser
        in_port = msg.match['in_port']

        # Get datapath ID to identify the switch
        dpid = datapath.id
        self.mac_to_port.setdefault(dpid, {})
        

        pkt = packet.Packet(msg.data)
        eth = pkt.get_protocol(ethernet.ethernet)

        # ignore ipv6
        if eth.ethertype == ethernet.ether.ETH_TYPE_IPV6: return

        arp_pkt = pkt.get_protocol(arp.arp)
        if arp_pkt:
            if arp_pkt.opcode == arp.ARP_REQUEST:
                self.logger.info("[DPID %s] ARP REQUEST: who-has %s? tell %s (mac %s, port %s)", dpid, arp_pkt.dst_ip, arp_pkt.src_ip, arp_pkt.src_mac, in_port)
            elif arp_pkt.opcode == arp.ARP_REPLY:
                self.logger.info("[DPID %s] ARP REPLY: %s is-at %s (port %s)", dpid, arp_pkt.src_ip, arp_pkt.src_mac, in_port)
        else:
            self.logger.info("[DPID %s] ETH: %s %s -> %s (port %s)", dpid, eth.ethertype, eth.src, eth.dst, in_port)

        # TODO: learning switch implementation