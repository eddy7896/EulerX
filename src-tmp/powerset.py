# Copyright (c) 2014 University of California, Davis
# 
# 
# Permission is hereby granted, free of charge, to any person obtaining
# a copy of this software and associated documentation files (the
# "Software"), to deal in the Software without restriction, including
# without limitation the rights to use, copy, modify, merge, publish,
# distribute, sublicense, and/or sell copies of the Software, and to
# permit persons to whom the Software is furnished to do so, subject to
# the following conditions:
# 
# The above copyright notice and this permission notice shall be
# included in all copies or substantial portions of the Software.
# 
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
# IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY
# CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT,
# TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE
# SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

import sys

def is_power2(num):
    return num != 0 and ((num & (num - 1)) == 0)

n = int(sys.argv[1])
numOfNodes = 2**n
nodes = []
edges = []

for i in range(numOfNodes):
    nodes.append(i)

for i in nodes:
    for j in nodes:
        if i<j and is_power2(i^j):
            edges.append([i,j])
print edges
            
f = open("powerset.dot","w")
f.write("digraph{\n")
f.write("rankdir = BT\n")
f.write("node [shape=box]\n")
for node in nodes:
    f.write(node.__str__() + "\n")
f.write("edge [style=solid]\n")
for edge in edges:
    f.write(edge[0].__str__() + "->" + edge[1].__str__() + "\n")

f.write("}")
f.close()
