# Copyright 2024 Computer Networks Group @ UPB
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

#!/usr/bin/env bash

# sudo mn --topo single,3 --link tc

sudo mn --custom topo.py --topo star --link tc

# NOTES:
#
# The above command _will_ configure S1 to behave like a learning switch, under the hood.
# This is why 'pingall' succeeds. If you run:
#
#   ovs-ofctl dump-flows s1
#
# you will see something like this:
#
#   cookie=0x0, duration=7.378s, table=0, n_packets=18, n_bytes=1548, priority=0 actions=NORMAL
#
# This is a 'flow' installed by mininet. It sends every frame out the "NORMAL" port. This is a
# virtual port that indicates "act like a normal L2 switch when deciding the output port". Another
# option is FLOOD. You can create your own flow rules that select output ports based on your
# conditions. This is the subject of the other 2 tasks.
#
# If you now run:
#
#   sudo mn --custom topo.py --topo bridge --link tc --controller none
# 
# pingall will stop working. That is because there are now no flows installed on the switch, so
# every packet is dropped. You can dump the flows again to verify 