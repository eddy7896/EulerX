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

# =========
# lattice.py
# Author: Shizhuo Yu
# <fill me with good Python best practice stuff> 

import subprocess
from subprocess import call
import sys
import os
import re
from arts2NumPW import artD

def removeRed(originList,removeList):
    delNodes = []
    for e in removeList:
        if e in originList:
            originList.remove(e)

def remove_duplicate_string(li):
    if li:
        li.sort()
        last = li[-1]
        for i in range(len(li)-2, -1, -1):
            if last == li[i]:
                del li[i]
            else:
                last = li[i]

def removeBracPri(s):
    return s.replace("[","").replace("]","").replace("'","")

# Green -> Blue
# Red -> Pink
def findGreenNumPW(t):
    s = ""
    if t in artD:
        s = "\n(" + artD[tuple(anyGreen[1:])].__str__() + ")"
    else:
        s = "\n(?)"
    return s

def findRedNumPW(t):
    s = ""
    if t in artD:
        s = "\n(" + artD[tuple(anyRed[1:])].__str__() + ")"
    else:
        s = "\n(?)"
    return s

fileName = os.path.splitext(os.path.basename(sys.argv[1]))[0]
fileFullDot = sys.argv[2]+"/"+fileName+"_fulllat.dot"
fileDot = sys.argv[2]+"/"+fileName+"_lat.dot"
fileName = sys.argv[1]
misArts = []
arts = []
f = open("output.txt","r")
lines = f.readlines()
for line in lines:
    if line.split(" ")[0] == "Min":
        index1 = line.index("[")
        index2 = line.index("]")
        line = line[index1+1:index2-1]
        mises = line.split(" , ")
        tmpmis = ""
        for mis in mises:
            tmpmis = tmpmis + mis[mis.index(":")+2:] + ","
        misArts.append(tmpmis[:-1])
f.close()
f = open(fileName, "r")
lines = f.readlines()
for line in lines:
    if (re.match("\[.*?\]", line)):
        arts.append(re.match("\[(.*)\]", line).group(1))
f.close()

misArtIds = []
misList = []
for mis in misArts:
    tmpindex = 0
    tmpindexes = []
    tmpindexesList = []
    tmpAs = mis.split(",")
    for tmpA in tmpAs:
        tmpindex = arts.index(tmpA)+1
        tmpindexes.append(tmpindex)
        tmpindexesList.append(str(tmpindex))
#    for tmpA in tmpAs:
#        for a in arts:
#            if tmpA == a:
#                tmpindex = arts.index(a)+1
#                tmpindexes.append(tmpindex)
#                tmpindexesList.append(str(tmpindex))
    misArtIds.append(tmpindexes)
    misList.append(tmpindexesList)

i = 0
solidRedWs = []
allRedWs = []
for misArtId in misArtIds:
    s = ""
    ssR = ""
    for e in misArtId:
        s = s + "i(W," + str(e) + "),"
    for e in range(1,len(arts)+1):
        if e not in misArtId:
            ssR = ssR + "o(W," + e.__str__() + "),"
    ssR = s + ssR
    f = open("query.asp","w")
    f.write(s[:-1]+"?")
    f.close()
    allRedW = subprocess.check_output("dlv -silent -brave expWorlds_aw.asp query.asp", shell=True)
    for e in allRedW.split("\n")[:-1]:
        allRedWs.append(e)
    f = open("query.asp","w")
    f.write(ssR[:-1]+"?")
    f.close()
    solidRedW = subprocess.check_output("dlv -silent -brave expWorlds_aw.asp query.asp", shell=True)
    solidRedWs.append(solidRedW[:-1])
    i = i + 1

allNodes = []
for i in range(2**len(arts)):
    allNodes.append(str(i))

remove_duplicate_string(allRedWs)

f = open("resultRed.txt","w")
i = 0
for node in allRedWs:
    f = open("query.asp","w")
    f.write("ai(A) :- i(" + node +",A).\n")
    f.write("ai(A)?")
    f.close()
    com = "echo \"" + node + "\" >> resultRed.txt"
    call(com, shell=True)
    com ="dlv -silent expWorlds_aw.asp query.asp -brave >> resultRed.txt" 
    call(com, shell=True)
    com = "echo \"\n\" >> \"resultRed.txt\""
    call(com, shell=True)
    print "done",i,"/",len(allRedWs)-1
    i = i+1
f.close()

with open("resultRed_tmp.txt", "wt") as fout:
    with open("resultRed.txt","rt") as fin:
        for line in fin:
            s = line.replace("\n",",")
            fout.write(s)
with open("resultRed_new.txt", "wt") as fout:
    with open("resultRed_tmp.txt","rt") as fin:
        for line in fin:
            s = line.replace(",,,","\n")
            fout.write(s)
call("rm resultRed_tmp.txt", shell=True)

allReds = []
f = open("resultRed_new.txt","r")
lines = f.readlines()
for line in lines:
    if line != "\n":
        oneRed = line[:-1].split(",")
        allReds.append(oneRed)
f.close()

removeRed(allNodes,allRedWs)

f = open("result.txt","w")
i = 0
for node in allNodes:
    f = open("query.asp","w")
    f.write("ai(A) :- i(" + node +",A).\n")
    f.write("ai(A)?")
    f.close()
    com = "echo \"" + node + "\" >> result.txt"
    call(com, shell=True)
    com ="dlv -silent expWorlds_aw.asp query.asp -brave >> result.txt" 
    call(com, shell=True)
    com = "echo \"\n\" >> \"result.txt\""
    call(com, shell=True)
    print "done",i,"/",len(allNodes)-1
    i = i+1
f.close()


with open("result_tmp.txt", "wt") as fout:
    with open("result.txt","rt") as fin:
        for line in fin:
            s = line.replace("\n",",")
            fout.write(s)
with open("result_new.txt", "wt") as fout:
    with open("result_tmp.txt","rt") as fin:
        for line in fin:
            s = line.replace(",,,","\n")
            fout.write(s)
call("rm result_tmp.txt", shell=True)

allGreens = []
f = open("result_new.txt","r")
lines = f.readlines()
for line in lines:
    if line != "\n":
        oneGreen = line[:-1].split(",")
        allGreens.append(oneGreen)
f.close()

macList = []
for e in allGreens:
    macList.append(e) 

delNodes = []
for e1 in macList:
    for e2 in macList:
        if (set(e1[1:]).issubset(set(e2[1:])) and set(e1[1:]) != set(e2[1:])) or e1[1:] == [""]:
            delNodes.append(e1)
remove_duplicate_string(delNodes)

for delNode in delNodes:
    if macList.index(delNode) != -1:
        macList.remove(delNode)

solidGreenWs = []
for mac in macList:
    s = ""
    ssG= ""
    f = open("query.asp","w")
    for e in mac[1:]:
        if e:
            s = s + "i(W," + str(e) + "),"
    for e in range(1,len(arts)+1):
        if e.__str__() not in mac[1:]:
            ssG = ssG + "o(W," + e.__str__() + "),"
    ssG = s + ssG
    f = open("query.asp","w")
    f.write(ssG[:-1]+"?")
    f.close()
    solidGreenW = subprocess.check_output("dlv -silent -brave expWorlds_aw.asp query.asp", shell=True)
    solidGreenWs.append(solidGreenW[:-1])

# get full lattice
fIn = open("up.dlv","r")
line = fIn.readline()
ups = line[1:-1].split(", ")
fOut = open(fileFullDot,"w")
fOut.write("digraph{\n")
fOut.write('node[fontname="Helvetica-Narrow"]\n')
fOut.write("rankdir=TB\n")
anyGreenW = []
anyRedW = []
for anyGreen in allGreens:
    anyGreenW.append(anyGreen[0])
    if anyGreen[0] in solidGreenWs:
        fOut.write(anyGreen[0] + ' [shape=box color="#134d9c" fillcolor="#68b5e3" style="rounded,filled" label="' \
                   + removeBracPri(anyGreen[1:].__str__()) + findGreenNumPW(tuple(anyGreen[1:])) + '"];\n')
    else:
        fOut.write(anyGreen[0] + ' [shape=box color="#134d9c" style=dashed label="' \
                   + removeBracPri(anyGreen[1:].__str__()) + findGreenNumPW(tuple(anyGreen[1:])) + '"];\n')
for anyRed in allReds:
    anyRedW.append(anyRed[0])
    if anyRed[0] in solidRedWs:
        fOut.write(anyRed[0] + ' [shape=octagon color="#9f1684" fillcolor="#df77cb" style=filled label="' \
                   + removeBracPri(anyRed[1:].__str__()) + findRedNumPW(tuple(anyRed[1:])) + '"];\n')
    else:
        fOut.write(anyRed[0] + ' [shape=octagon color="#9f1684" fillcolor="#df77cb" style=dashed label="' \
                   + removeBracPri(anyRed[1:].__str__()) + findRedNumPW(tuple(anyRed[1:])) + '"];\n')    
for up in ups:
    if up.split(",")[0][3:] in anyGreenW and up.split(",")[1][:-1] in anyGreenW:
        fOut.write(up.split(",")[1][:-1] + '->' + up.split(",")[0][3:] + '[color="#134d9c" style=dashed];\n')
    if up.split(",")[0][3:] in anyRedW and up.split(",")[1][:-1] in anyRedW:
        fOut.write(up.split(",")[1][:-1] + '->' + up.split(",")[0][3:] + '[dir=back color="#9c1382" style=dashed];\n')
    if up.split(",")[0][3:] in anyGreenW and up.split(",")[1][:-1] in anyRedW:
        fOut.write(up.split(",")[1][:-1] + '->' + up.split(",")[0][3:] + '[arrowhead=none color="#0000FF" style=filled];\n')

# Add legend
artsLabels = ""
for art in arts:
    artsLabels += "<TR> \n <TD>" + str(arts.index(art)+1) + "</TD> \n <TD>" + art + "</TD> \n </TR> \n"
fOut.write("node[shape=box] \n")
fOut.write('{rank=sink Legend [fillcolor= white margin=0 label=< \n <TABLE BORDER="0" CELLBORDER="1" CELLSPACING="0" CELLPADDING="4"> \n' )
fOut.write(artsLabels)
fOut.write("</TABLE> \n >] } \n")


fOut.write("}")
fIn.close()
fOut.close()

#com = "dot -Tpdf " + fileDot + " -o " + filePdf
#call(com, shell=True)

# get reduced lattice
f = open(fileDot,"w")
f.write("digraph{\n")
f.write('node[fontname="Helvetica-Narrow"]\n')
f.write("rankdir=TB\n")
if len(misList) != 1:
    f.write('"AllOtherRed" [shape=octagon color="#df77cb" style=dashed]\n')
if len(macList) != 1:
    f.write('"AllOtherGreen" [shape=box color="#134d9c" style="rounded,dashed"]\n')
for mcs in macList:
    f.write('"' + removeBracPri(str(mcs[1:])) + '" [shape=box color="#134d9c" fillcolor="#68b5e3" style="rounded,filled"];\n')
for mis in misList:
    f.write('"' + removeBracPri(str(mis)) + '" [shape=octagon color="#9f1684" fillcolor="#df77cb" style="filled"];\n')
for mcs in macList:
    if len(misList) != 1:
        f.write('"AllOtherRed" -> "' + removeBracPri(str(mcs[1:])) + '" [color=blue, arrowhead=none, label='+ str(len(arts)-len(mcs[1:])) +'];\n')
    if len(macList) != 1:
        f.write('"' + removeBracPri(str(mcs[1:])) + '" -> "AllOtherGreen" [color="#134d9c" style=dashed, label='+ str(len(mcs[1:])) +'];\n')
for mis in misList:
    if len(misList) != 1:
        f.write('"AllOtherRed" -> "' + removeBracPri(str(mis)) + '" [color=red, style=dashed, dir=back, label='+ str(len(arts)-len(mis)) +'];\n')
    if len(macList) != 1:
        f.write('"' + removeBracPri(str(mis)) + '" -> "AllOtherGreen" [color=blue, arrowhead=none, label='+ str(len(mis)) +'];\n')
for mcs in macList:
    for mis in misList:
        if set(mcs[1:]).issubset(set(mis)):
            f.write('"' + removeBracPri(str(mis)) + '" -> "' + removeBracPri(str(mcs[1:])) + '" [color=blue, arrowhead=none, label=1];\n')
        elif set(mis).issubset(set(mcs[1:])):
            f.write('"' + removeBracPri(str(mcs[1:])) + '" -> "' + removeBracPri(str(mis)) + '" [color=blue, arrowhead=none, label=1];\n')

# Add legend
f.write("node[shape=box] \n")
f.write('{rank=sink Legend [fillcolor= white margin=0 label=< \n <TABLE BORDER="0" CELLBORDER="1" CELLSPACING="0" CELLPADDING="4"> \n' )
f.write(artsLabels)
f.write("</TABLE> \n >] } \n")
f.write("}")
f.close()

#com = "dot -Tpdf " + fileDot + " -o " + filePdf
#call(com, shell=True)

# delete unused file
if os.path.isfile("arts2NumPW.py"):
    call("rm " +  "arts2NumPW.py", shell=True)
if os.path.isfile("arts2NumPW.pyc"):
    call("rm " +  "arts2NumPW.pyc", shell=True)
