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

import re
import copy
import commands
from relations import *
from taxonomy import *

class Articulation:
    
    def __init__(self, initInput="", mapping=None):
        self.string = initInput
        self.numTaxon = 2
        self.confidence = 2
        self.relations = 0
        self.sumLabel = False
        if (initInput == ""):
            self.taxon1 = Taxon()
            self.taxon2 = Taxon()
            self.taxon3 = Taxon()
            self.taxon4 = Taxon()
            self.taxon5 = Taxon()
            return None
        
        # Parsing begins here
        if (initInput.find("confidence=") != -1):
            elements = re.match("(.*) confidence=(.*)", initInput)
            initInput = elements.group(1)
            self.confidence = int(elements.group(2))
        if (initInput.find("lsum ") != -1 or initInput.find("l3sum ") != -1 or\
            initInput.find("l4sum ") != -1 or initInput.find("rsum ") != -1 or\
            initInput.find("r3sum ") != -1 or initInput.find("r4sum ") != -1 or\
            initInput.find("ldiff ") != -1 or initInput.find("rdiff ") != -1 or
            initInput.find("e4sum") != -1 or initInput.find("i4sum") != -1):
            self.sumLabel = True
        if self.sumLabel:
            if (initInput.find("lsum") != -1):
                self.relations = relation["+="]
                elements = re.match("(.*)\.(.*) (.*)\.(.*) lsum (.*)\.(.*)", initInput)
            elif (initInput.find("l3sum") != -1):
                self.relations = relation["+3="]
                elements = re.match("(.*)\.(.*) (.*)\.(.*) (.*)\.(.*) l3sum (.*)\.(.*)", initInput)
            elif (initInput.find("l4sum") != -1):
                self.relations = relation["+4="]
                elements = re.match("(.*)\.(.*) (.*)\.(.*) (.*)\.(.*) (.*)\.(.*) l4sum (.*)\.(.*)", initInput)
            elif (initInput.find("rsum") != -1):
                self.relations = relation["=+"]
                elements = re.match("(.*)\.(.*) rsum (.*)\.(.*) (.*)\.(.*)", initInput)
            elif (initInput.find("r3sum") != -1):
                self.relations = relation["=3+"]
                elements = re.match("(.*)\.(.*) r3sum (.*)\.(.*) (.*)\.(.*) (.*)\.(.*)", initInput)
            elif (initInput.find("r4sum") != -1):
                self.relations = relation["=4+"]
                elements = re.match("(.*)\.(.*) r4sum (.*)\.(.*) (.*)\.(.*) (.*)\.(.*) (.*)\.(.*)", initInput)
            elif (initInput.find("ldiff") != -1):
                self.relations = relation["-="]
                elements = re.match("(.*)\.(.*) (.*)\.(.*) ldiff (.*)\.(.*)", initInput)
            elif (initInput.find("rdiff") != -1):
                self.relations = relation["=-"]
                elements = re.match("(.*)\.(.*) rdiff (.*)\.(.*) (.*)\.(.*)", initInput)
            elif (initInput.find("e4sum") != -1):
                self.relations = 0 #[relationDict["+=+"]]
                elements = re.match("(.*)\.(.*) (.*)\.(.*) e4sum (.*)\.(.*) (.*)\.(.*)", initInput)
            elif (initInput.find("i4sum") != -1):
                self.relations = 0 #[relationDict["+<=+"]]
                elements = re.match("(.*)\.(.*) (.*)\.(.*) i4sum (.*)\.(.*) (.*)\.(.*)", initInput)
            else:
                raise Exception("Syntax error in \""+initInput+"\"!!")
                
            taxon1taxonomy = elements.group(1)
            taxon1taxon = elements.group(2)
            taxon2taxonomy = elements.group(3)
            taxon2taxon = elements.group(4)
            taxon3taxonomy = elements.group(5)
            taxon3taxon = elements.group(6)
            self.taxon1 = mapping.getTaxon(taxon1taxonomy, taxon1taxon)
            self.taxon2 = mapping.getTaxon(taxon2taxonomy, taxon2taxon)
            self.taxon3 = mapping.getTaxon(taxon3taxonomy, taxon3taxon)
            self.numTaxon = 3
            if(initInput.find("e4sum") != -1 or initInput.find("i4sum") != -1 or initInput.find("l3sum") != -1 or initInput.find("r3sum") != -1):
                taxon4taxonomy = elements.group(7)
                taxon4taxon = elements.group(8)
                self.taxon4 = mapping.getTaxon(taxon4taxonomy, taxon4taxon)
                self.numTaxon = 4
            if(initInput.find("l4sum") != -1 or initInput.find("r4sum") != -1):
                taxon4taxonomy = elements.group(7)
                taxon4taxon = elements.group(8)
                self.taxon4 = mapping.getTaxon(taxon4taxonomy, taxon4taxon)
                taxon5taxonomy = elements.group(9)
                taxon5taxon = elements.group(10)
                self.taxon5 = mapping.getTaxon(taxon5taxonomy, taxon5taxon)
                self.numTaxon = 5
        else:
            ## initInput is of form b48.a equals k04.a
            self.relation = 0
            if (initInput.find("{") != -1):
                elements = re.match("(.*)\.(.*) {(.*)} (.*)\.(.*)", initInput)
            else:
                elements = re.match("(.*)\.(.*) (.*) (.*)\.(.*)", initInput)
            if elements is None:
                raise Exception("Syntax error in \""+initInput+"\"!!")
            
            taxon1taxonomy = elements.group(1)
            taxon1taxon = elements.group(2)
            relString = elements.group(3)
            taxon2taxonomy = elements.group(4)
            taxon2taxon = elements.group(5)
            
            if (relString.find(" ") != -1):
                if (relation.has_key(relString)):
                    self.relations = rcc5[relString]
                else:
                    relElements = re.split("\s", relString)
                    
                    for rel in relElements:
                        self.relations |= rcc5[rel]
                        
            else:
                self.relations = rcc5[relString]
                
            self.taxon1 = mapping.getTaxon(taxon1taxonomy, taxon1taxon)
            self.taxon2 = mapping.getTaxon(taxon2taxonomy, taxon2taxon)

    # Generate Gringo aggregation rule
    def getGringoAggrRule(self, firstIsIn, firstName, secondIsIn, secondName, withPW):
        firstIO = "in" if firstIsIn else "out"
        secondIO = "in" if secondIsIn else "out"
        baseFormat = 'X : vrs(X), {}({},X), {}({},X)'
        rule = baseFormat.format(firstIO, firstName, secondIO, secondName)
        rule = ':- #sum {' + rule + '} <= 0'
        if (withPW):
            return rule + ", pw.\n"
        else:
            return rule + ".\n"

    def toASP(self, enc, rnr, align):
        result = ""
        name1 = self.taxon1.dlvName()
        name2 = self.taxon2.dlvName()
        if encode[enc] & encode["vr"] or encode[enc] & encode["dl"] or encode[enc] & encode["mn"]:
            if self.relations == rcc5["equals"]:
                result  = "ir(X, r" + self.ruleNum.__str__() + ") :- out(" + name1 + ",X), in(" + name2 + ",X).\n"
                result += "ir(X, r" + self.ruleNum.__str__() + ") :- in(" + name1 + ",X), out(" + name2 + ",X).\n" 
                result += "ir(X, prod(r" + self.ruleNum.__str__() + ",R)) :- out3(" + name1 + ", X, R), in(" + name2 + ",X), ix.\n"
                result += "ir(X, prod(r" + self.ruleNum.__str__() + ",R)) :- in(" + name1 + ",X), out3(" + name2 + ", X, R), ix.\n" 
                if reasoner[rnr] == reasoner["dlv"]:
                    result += ":- #count{X: vrs(X), in(" + name1 + ",X), in(" + name2 + ",X)} = 0, pw.\n" 
                elif reasoner[rnr] == reasoner["gringo"]:
                    align.basePw += self.getGringoAggrRule(True, name1, True, name2, True)
                    #align.basePw += ":- [vrs(X): in(" + name1 + ",X): in(" + name2 + ",X)]0, pw.\n"
                result += "pie(r" + self.ruleNum.__str__() + ", A, 1) :- ir(X, A), in(" + name1 + ", X), in(" + name2 + ", X), ix.\n"
                result += "c(r" + self.ruleNum.__str__() + ", A, 1) :- vr(X, A), in(" + name1 + ", X), in(" + name2 + ", X), ix.\n\n"
                #result += "in(" + name1 + ",X) :- in(" + name2 + ",X).\n" 
                #result += "in(" + name2 + ",X) :- in(" + name1 + ",X).\n" 
                #result += "out(" + name1 + ",X) :- out(" + name2 + ",X).\n" 
                #result += "out(" + name2 + ",X) :- out(" + name1 + ",X).\n" 
            elif self.relations == rcc5["includes"]:
                result  = "ir(X, r" + self.ruleNum.__str__() + ") :- out(" + name1 + ",X), in(" + name2 + ",X), pw.\n"
                result += "ir(X, prod(r" + self.ruleNum.__str__() + ",R)) :- out3(" + name1 + ", X, R), in(" + name2 + ",X), ix.\n"
                if reasoner[rnr] == reasoner["dlv"]:
                    result += ":- #count{X: vrs(X), in(" + name1 + ",X), in(" + name2 + ",X)} = 0, pw.\n" 
                    result += ":- #count{X: vrs(X), in(" + name1 + ",X), out(" + name2 + ",X)} = 0, pw.\n" 
                elif reasoner[rnr] == reasoner["gringo"]:
                    align.basePw += self.getGringoAggrRule(True, name1, True, name2, True)
                    align.basePw += self.getGringoAggrRule(True, name1, False, name2, True)
                    # align.basePw += ":- [vrs(X): in(" + name1 + ",X): in(" + name2 + ",X)]0, pw.\n"
                    # align.basePw += ":- [vrs(X): in(" + name1 + ",X): out(" + name2 + ",X)]0, pw.\n"
                result += "pie(r" + self.ruleNum.__str__() + ", A, 1) :- ir(X, A), in(" + name1 + ", X), out(" + name2 + ", X), ix.\n"
                result += "c(r" + self.ruleNum.__str__() + ", A, 1) :- vr(X, A), in(" + name1 + ", X), out(" + name2 + ", X), ix.\n\n"
                result += "pie(r" + self.ruleNum.__str__() + ", A, 2) :- ir(X, A), in(" + name1 + ", X), in(" + name2 + ", X), ix.\n"
                result += "c(r" + self.ruleNum.__str__() + ", A, 2) :- vr(X, A), in(" + name1 + ", X), in(" + name2 + ", X), ix.\n\n"
                #result += "in(" + name1 + ",X) :- in(" + name2 + ",X).\n" 
                #result += "out(" + name2 + ",X) :- out(" + name1 + ",X).\n" 
                #result += "in(" + name1 + ",X) v out(" + name1 + ",X) :- out(" + name2 + ",X).\n" 
                #result += "in(" + name2 + ",X) v out(" + name2 + ",X) :- in(" + name1 + ",X).\n" 
            elif self.relations == rcc5["is_included_in"]:
                if reasoner[rnr] == reasoner["dlv"]:
                    result = ":- #count{X: vrs(X), in(" + name1 + ",X), in(" + name2 + ",X)} = 0, pw.\n" 
                    result += ":- #count{X: vrs(X), out(" + name1 + ",X), in(" + name2 + ",X)} = 0, pw.\n" 
                elif reasoner[rnr] == reasoner["gringo"]:
                    align.basePw += self.getGringoAggrRule(True, name1, True, name2, False)
                    align.basePw += self.getGringoAggrRule(False, name1, True, name2, False)
                    # align.basePw += ":- [vrs(X): in(" + name1 + ",X): in(" + name2 + ",X)]0.\n"
                    # align.basePw += ":- [vrs(X): out(" + name1 + ",X): in(" + name2 + ",X)]0.\n"
                result += "ir(X, r" + self.ruleNum.__str__() + ") :- in(" + name1 + ",X), out(" + name2 + ",X), pw.\n" 
                result += "pie(r" + self.ruleNum.__str__() + ", A, 1) :- ir(X, A), out(" + name1 + ", X), in(" + name2 + ", X), ix.\n"
                result += "c(r" + self.ruleNum.__str__() + ", A, 1) :- vr(X, A), out(" + name1 + ", X), in(" + name2 + ", X), ix.\n\n"
                result += "pie(r" + self.ruleNum.__str__() + ", A, 2) :- ir(X, A), in(" + name1 + ", X), in(" + name2 + ", X), ix.\n"
                result += "c(r" + self.ruleNum.__str__() + ", A, 2) :- vr(X, A), in(" + name1 + ", X), in(" + name2 + ", X), ix.\n\n"
                #result += "in(" + name2 + ",X) :- in(" + name1 + ",X).\n" 
                #result += "out(" + name1 + ",X) :- out(" + name2 + ",X).\n" 
                #result += "in(" + name1 + ",X) v out(" + name1 + ",X) :- in(" + name2 + ",X).\n" 
                #result += "in(" + name2 + ",X) v out(" + name2 + ",X) :- out(" + name1 + ",X).\n" 
            elif self.relations == rcc5["disjoint"]:
                if reasoner[rnr] == reasoner["dlv"]:
                    result = ":- #count{X: vrs(X), in(" + name1 + ",X), out(" + name2 + ",X)} = 0, pw.\n" 
                    result += ":- #count{X: vrs(X), out(" + name1 + ",X), in(" + name2 + ",X)} = 0, pw.\n" 
                elif reasoner[rnr] == reasoner["gringo"]:
                    align.basePw += self.getGringoAggrRule(True, name1, False, name2, False)
                    align.basePw += self.getGringoAggrRule(False, name1, True, name2, False)
                    # align.basePw += ":- [vrs(X): in(" + name1 + ",X): out(" + name2 + ",X)]0.\n"
                    # align.basePw += ":- [vrs(X): out(" + name1 + ",X): in(" + name2 + ",X)]0.\n"
                result += "pie(r" + self.ruleNum.__str__() + ", A, 1) :- ir(X, A), out(" + name1 + ", X), in(" + name2 + ", X), ix.\n"
                result += "c(r" + self.ruleNum.__str__() + ", A, 1) :- vr(X, A), out(" + name1 + ", X), in(" + name2 + ", X), ix.\n\n"
                result += "pie(r" + self.ruleNum.__str__() + ", A, 2) :- ir(X, A), in(" + name1 + ", X), out(" + name2 + ", X), ix.\n"
                result += "c(r" + self.ruleNum.__str__() + ", A, 2) :- vr(X, A), in(" + name1 + ", X), out(" + name2 + ", X), ix.\n\n"
                result += "ir(X, r" + self.ruleNum.__str__() + ") :- in(" + name1 + ",X), in(" + name2 + ",X).\n" 
                #result += "out(" + name1 + ",X) :- in(" + name2 + ",X).\n" 
                #result += "out(" + name2 + ",X) :- in(" + name1 + ",X).\n" 
                #result += "in(" + name1 + ",X) v out(" + name1 + ",X) :- out(" + name2 + ",X).\n" 
                #result += "in(" + name2 + ",X) v out(" + name2 + ",X) :- out(" + name1 + ",X).\n" 
            elif self.relations == rcc5["overlaps"]:
                if reasoner[rnr] == reasoner["dlv"]:
                    result = ":- #count{X: vrs(X), in(" + name1 + ",X), in(" + name2 + ",X)} = 0, pw.\n" 
                    result += ":- #count{X: vrs(X), out(" + name1 + ",X), in(" + name2 + ",X)} = 0, pw.\n" 
                    result += ":- #count{X: vrs(X), in(" + name1 + ",X), out(" + name2 + ",X)} = 0, pw.\n" 
                elif reasoner[rnr] == reasoner["gringo"]:
                    align.basePw += self.getGringoAggrRule(True, name1, False, name2, False)
                    align.basePw += self.getGringoAggrRule(True, name1, False, name2, False)
                    align.basePw += self.getGringoAggrRule(False, name1, True, name2, False)
                    # align.basePw += ":- [vrs(X): in(" + name1 + ",X): in(" + name2 + ",X)]0.\n"
                    # align.basePw += ":- [vrs(X): in(" + name1 + ",X): out(" + name2 + ",X)]0.\n"
                    # align.basePw += ":- [vrs(X): out(" + name1 + ",X): in(" + name2 + ",X)]0.\n"
                result += "pie(r" + self.ruleNum.__str__() + ", A, 1) :- ir(X, A), out(" + name1 + ", X), in(" + name2 + ", X), ix.\n"
                result += "c(r" + self.ruleNum.__str__() + ", A, 1) :- vr(X, A), out(" + name1 + ", X), in(" + name2 + ", X), ix.\n\n"
                result += "pie(r" + self.ruleNum.__str__() + ", A, 2) :- ir(X, A), in(" + name1 + ", X), out(" + name2 + ", X), ix.\n"
                result += "c(r" + self.ruleNum.__str__() + ", A, 2) :- vr(X, A), in(" + name1 + ", X), out(" + name2 + ", X), ix.\n\n"
                result += "pie(r" + self.ruleNum.__str__() + ", A, 3) :- ir(X, A), in(" + name1 + ", X), in(" + name2 + ", X), ix.\n"
                result += "c(r" + self.ruleNum.__str__() + ", A, 3) :- vr(X, A), in(" + name1 + ", X), in(" + name2 + ", X), ix.\n\n"
                #result += "in(" + name1 + ",X) v out(" + name1 + ",X) :- in(" + name2 + ",X).\n" 
                #result += "in(" + name2 + ",X) v out(" + name2 + ",X) :- out(" + name1 + ",X).\n" 
                #result += "in(" + name1 + ",X) v out(" + name1 + ",X) :- out(" + name2 + ",X).\n" 
                #result += "in(" + name2 + ",X) v out(" + name2 + ",X) :- in(" + name1 + ",X).\n" 
            elif self.relations == (rcc5["equals"] | rcc5["disjoint"]):
                if reasoner[rnr] == reasoner["dlv"]:
                    result = ":- #count{X: vrs(X), in(" + name1 + ", X), out(" + name2 + ", X)} = 0, #count{Y: vrs(Y), in(" + name1 +", Y), in(" + name2 + ", Y)} = 0, #count{Z: vrs(Z), out(" + name1 + ", Z), in(" + name2 + ", Z)} = 0.\n\n"
                    result += ":- #count{X: vrs(X), in(" + name1 + ", X), out(" + name2 + ", X)} = 0, #count{Y: vrs(Y), in(" + name1 +", Y), in(" + name2 + ", Y)} = 0, #count{Z: vrs(Z), out(" + name1 + ", Z), in(" + name2 + ", Z)} > 0.\n\n"
                    result += ":- #count{X: vrs(X), in(" + name1 + ", X), out(" + name2 + ", X)} = 0, #count{Y: vrs(Y), in(" + name1 +", Y), in(" + name2 + ", Y)} > 0, #count{Z: vrs(Z), out(" + name1 + ", Z), in(" + name2 + ", Z)} > 0.\n\n"
                    result += ":- #count{X: vrs(X), in(" + name1 + ", X), out(" + name2 + ", X)} > 0, #count{Y: vrs(Y), in(" + name1 +", Y), in(" + name2 + ", Y)} = 0, #count{Z: vrs(Z), out(" + name1 + ", Z), in(" + name2 + ", Z)} = 0.\n\n"
                    result += ":- #count{X: vrs(X), in(" + name1 + ", X), out(" + name2 + ", X)} > 0, #count{Y: vrs(Y), in(" + name1 +", Y), in(" + name2 + ", Y)} > 0, #count{Z: vrs(Z), out(" + name1 + ", Z), in(" + name2 + ", Z)} = 0.\n\n"
                    result += ":- #count{X: vrs(X), in(" + name1 + ", X), out(" + name2 + ", X)} > 0, #count{Y: vrs(Y), in(" + name1 +", Y), in(" + name2 + ", Y)} > 0, #count{Z: vrs(Z), out(" + name1 + ", Z), in(" + name2 + ", Z)} > 0.\n\n"
#                    result = "vr(X, r" + self.ruleNum.__str__() + ") v ir(X, r" + self.ruleNum.__str__() + ") :- out(" + name1 + ",X), in(" + name2 + ",X).\n"
#                    result += "vr(X, r" + self.ruleNum.__str__() + ") v ir(X, r" + self.ruleNum.__str__() + ") :- in(" + name1 + ",X), out(" + name2 + ",X).\n"
#                    result += "vr(X, r" + self.ruleNum.__str__() + ") v ir(X, r" + self.ruleNum.__str__() + ") :- in(" + name1 + ",X), in(" + name2 + ",X).\n"  
#                    result  = ":- #count{X : vrs(X), in(" + name1 + ", X), out(" + name2 + ", X)} > 0, #count{Y : vrs(Y), out(" + name1 + ", Y), in(" + name2 + ", Y)} > 0.\n"
#                    result += ":- #count{X : vrs(X), in(" + name1 + ", X), out(" + name2 + ", X)} = 0, #count{Y : vrs(Y), out(" + name1 + ", Y), in(" + name2 + ", Y)} = 0.\n"
#                    result += ":- #count{X : vrs(X), in(" + name1 + ", X), in(" + name2 + ", X)} > 0, #count{Y : vrs(Y), out(" + name1 + ", Y), in(" + name2 + ", Y)} = 0.\n"
#                    result += ":- #count{X : vrs(X), in(" + name1 + ", X), in(" + name2 +", X)} = 0, #count{Y : vrs(Y), out(" + name1 + ", Y), in(" + name2 + ", Y)} > 0.\n"
                elif reasoner[rnr] == reasoner["gringo"]:
                    ## TODO
                    result = ""
            elif self.relations == (rcc5["equals"] | rcc5["is_included_in"]):
                result  = "ir(X, r" + self.ruleNum.__str__() + ") :- in(" + name1 + ",X), out(" + name2 + ",X).\n"
                result += "ir(X, prod(r" + self.ruleNum.__str__() + ",R)) :- in(" + name1 + ",X), out3(" + name2 + ", X, R), ix.\n" 
                if reasoner[rnr] == reasoner["dlv"]:
                    result += "vr(X, r" + self.ruleNum.__str__() + ") v ir(X, r" + self.ruleNum.__str__() + ") :- out(" + name1 + ",X), in(" + name2 + ",X).\n" 
                    result += ":- #count{X: vrs(X), in(" + name1 + ",X), in(" + name2 + ",X)} = 0, pw.\n" 
                elif reasoner[rnr] == reasoner["gringo"]:
                    result += "vr(X, r" + self.ruleNum.__str__() + ") | ir(X, r" + self.ruleNum.__str__() + ") :- out(" + name1 + ",X), in(" + name2 + ",X).\n"
                    align.basePw += self.getGringoAggrRule(True, name1, True, name2, True)
                    #align.basePw += ":- [vrs(X): in(" + name1 + ",X): in(" + name2 + ",X)]0, pw.\n"
                result += "pie(r" + self.ruleNum.__str__() + ", A, 1) :- ir(X, A), in(" + name1 + ", X), in(" + name2 + ", X), ix.\n"
                result += "c(r" + self.ruleNum.__str__() + ", A, 1) :- vr(X, A), in(" + name1 + ", X), in(" + name2 + ", X), ix.\n\n"
                #result += "in(" + name2 + ",X) :- in(" + name1 + ",X).\n" 
                #result += "out(" + name1 + ",X) :- out(" + name2 + ",X).\n" 
                #result += "in(" + name1 + ",X) v out(" + name1 + ",X) :- in(" + name2 + ",X).\n" 
                #result += "in(" + name2 + ",X) v out(" + name2 + ",X) :- out(" + name1 + ",X).\n" 
            elif self.relations == (rcc5["equals"] | rcc5["includes"]):
                result  = "ir(X, r" + self.ruleNum.__str__() + ") :- out(" + name1 + ",X), in(" + name2 + ",X).\n"
                result += "ir(X, prod(r" + self.ruleNum.__str__() + ",R)) :- out3(" + name1 + ", X, R), in(" + name2 + ",X), ix.\n"
                if reasoner[rnr] == reasoner["dlv"]:
                    result += "vr(X, r" + self.ruleNum.__str__() +") v ir(X, r" + self.ruleNum.__str__() + ") :- in(" + name1 + ",X), out(" + name2 + ",X).\n" 
                    result += ":- #count{X: vrs(X), in(" + name1 + ",X), in(" + name2 + ",X)} = 0, pw.\n" 
                elif reasoner[rnr] == reasoner["gringo"]:
                    result += "vr(X, r" + self.ruleNum.__str__() +") | ir(X, r" + self.ruleNum.__str__() + ") :- in(" + name1 + ",X), out(" + name2 + ",X).\n"
                    align.basePw += self.getGringoAggrRule(True, name1, True, name2, False)
                    # align.basePw += ":- [vrs(X): in(" + name1 + ",X): in(" + name2 + ",X)]0.\n"
                result += "pie(r" + self.ruleNum.__str__() + ", A, 1) :- ir(X, A), in(" + name1 + ", X), in(" + name2 + ", X), ix.\n"
                result += "c(r" + self.ruleNum.__str__() + ", A, 1) :- vr(X, A), in(" + name1 + ", X), in(" + name2 + ", X), ix.\n\n"
                #result += "in(" + name1 + ",X) :- in(" + name2 + ",X).\n" 
                #result += "out(" + name2 + ",X) :- out(" + name1 + ",X).\n" 
                #result += "in(" + name2 + ",X) v out(" + name2 + ",X) :- in(" + name1 + ",X).\n" 
                #result += "in(" + name1 + ",X) v out(" + name1 + ",X) :- out(" + name2 + ",X).\n" 
            elif self.relations == (rcc5["is_included_in"] | rcc5["includes"]):
                result  = "ir(X, r" + self.ruleNum.__str__() + ") :- in(" + name1 + ",X), out(" + name2 + ",X), vr(Y, _), in(" + name2 + ",Y), out(" + name1 + ",Y).\n"
                if reasoner[rnr] == reasoner["dlv"]:
                    result += "ir(Y, r" + self.ruleNum.__str__() + ") :- #count{X: vrs(X), in(" + name1 + ",X), out(" + name2 + ",X)} > 0, in(" + name2 + ",Y), out(" + name1 + ",Y).\n"
                elif reasoner[rnr] == reasoner["gringo"]:
                    result += "ir(Y, r" + self.ruleNum.__str__() + ") :- 1[vrs(X): in(" + name1 + ",X): out(" + name2 + ",X)], in(" + name2 + ",Y), out(" + name1 + ",Y).\n"
                #result += "in(" + name2 + ",X) v out(" + name2 + ",X) :- in(" + name1 + ",X).\n" 
                #result += "in(" + name1 + ",X) v out(" + name1 + ",X) :- out(" + name2 + ",X).\n" 
                #result += "in(" + name2 + ",X) v out(" + name2 + ",X) :- out(" + name1 + ",X).\n" 
                #result += "in(" + name1 + ",X) v out(" + name1 + ",X) :- in(" + name2 + ",X).\n" 
            elif self.relations == (rcc5["disjoint"] | rcc5["overlaps"]):
                if reasoner[rnr] == reasoner["dlv"]:
                    result  = "ir(X, r" + self.ruleNum.__str__() + ") v vr(X, r" + self.ruleNum.__str__() +") :- in(" + name1 + ",X), in(" + name2 + ",X).\n"
                    result += ":- #count{X: vrs(X), in(" + name1 + ",X), out(" + name2 + ",X)} = 0, pw.\n" 
                    result += ":- #count{X: vrs(X), in(" + name2 + ",X), out(" + name1 + ",X)} = 0, pw.\n" 
                elif reasoner[rnr] == reasoner["gringo"]:
                    result  = "ir(X, r" + self.ruleNum.__str__() + ") | vr(X, r" + self.ruleNum.__str__() +") :- in(" + name1 + ",X), in(" + name2 + ",X).\n"
                    align.basePw += self.getGringoAggrRule(True, name1, False, name2, False)
                    align.basePw += self.getGringoAggrRule(False, name1, True, name2, False)
                    # align.basePw += ":- [vrs(X): in(" + name1 + ",X): out(" + name2 + ",X)]0.\n"
                    # align.basePw += ":- [vrs(X): out(" + name1 + ",X): in(" + name2 + ",X)]0.\n"
                #result += "in(" + name2 + ",X) v out(" + name2 + ",X) :- in(" + name1 + ",X).\n" 
                #result += "in(" + name1 + ",X) v out(" + name1 + ",X) :- out(" + name2 + ",X).\n" 
                #result += "in(" + name2 + ",X) v out(" + name2 + ",X) :- out(" + name1 + ",X).\n" 
                #result += "in(" + name1 + ",X) v out(" + name1 + ",X) :- in(" + name2 + ",X).\n" 
            elif self.relations == (rcc5["equals"] | rcc5["overlaps"]):
                if reasoner[rnr] == reasoner["dlv"]:
                    result  = ":- #count{X: vrs(X), in(" + name1 + ",X), out(" + name2 + ",X)} > 0, #count{Y: vrs(Y), in(" + name2 + ",Y), out(" + name1 + ",Y)} = 0, pw.\n"
                    result += "pie(r" + self.ruleNum.__str__() + ", A, 1) :- ir(X, A), in(" + name2 + ", X), out(" + name1 + ", X), #count{Y: vr(Y, _), in(" + name1 + ",Y), out(" + name2 + ",Y)} > 0, ix.\n"
                    result += "c(r" + self.ruleNum.__str__() + ", A, 1) :- vr(X, A), in(" + name1 + ", X), out(" + name2 + ", X), #count{Y: vr(Y, _), in(" + name2 + ",Y), out(" + name1 + ",Y)} > 0, ix.\n\n"
                    result += ":- #count{X: vrs(X), in(" + name1 + ",X), out(" + name2 + ",X)} = 0, #count{Y: vrs(Y), in(" + name2 + ",Y), out(" + name1 + ",Y)} > 0, pw.\n"
                    result += "pie(r" + self.ruleNum.__str__() + ", A, 2) :- ir(X, A), in(" + name1 + ", X), out(" + name2 + ", X), #count{Y: vr(Y, _), in(" + name2 + ",Y), out(" + name1 + ",Y)} > 0, ix.\n"
                    result += "c(r" + self.ruleNum.__str__() + ", A, 2) :- vr(X, A), in(" + name1 + ", X), out(" + name2 + ", X), #count{Y: vr(Y, _), in(" + name2 + ",Y), out(" + name1 + ",Y)} > 0, ix.\n\n"
                    result += ":- #count{X: vrs(X), in(" + name1 + ",X), in(" + name2 + ",X)} = 0, pw.\n"
                    result += "pie(r" + self.ruleNum.__str__() + ", A, 3) :- ir(X, A), in(" + name1 + ", X), in(" + name2 + ", X), ix.\n"
                    result += "c(r" + self.ruleNum.__str__() + ", A, 3) :- vr(X, A), in(" + name1 + ", X), in(" + name2 + ", X), ix.\n\n"
                elif reasoner[rnr] == reasoner["gringo"]:

                    firstRule = self.getGringoAggrRule(True, name1, False, name2, False).replace(":- ", ":- 1 <= ").replace(" <= 0.\n", ", ")
                    result = firstRule + self.getGringoAggrRule(False, name2, True, name1, False).replace(":- ", "").replace("vrs(X)", "vr(Y, _)").replace("X", "Y")
                    secodRule = self.getGringoAggrRule(True, name1, False, name2, False).replace(".\n", ", ")
                    result += secodRule + self.getGringoAggrRule(True, name2, False, name1, False).replace(":- ", "1 <= ").replace(" <= 0.", ".").replace("vrs(X)", "vr(Y, _)").replace("X", "Y")
                    result += self.getGringoAggrRule(True, name1, True, name2, False)
                    # result  = ":- 1[vrs(X): in(" + name1 + ",X): out(" + name2 + ",X)], [vr(Y, _): in(" + name2 + ",Y): out(" + name1 + ",Y)]0.\n"
                    # result += ":- [vrs(X): in(" + name1 + ",X): out(" + name2 + ",X)]0, 1[vr(Y, _): in(" + name2 + ",Y): out(" + name1 + ",Y)].\n"
                    # result += ":- [vrs(X): in(" + name1 + ",X): in(" + name2 + ",X)]0.\n"
                #result += "in(" + name2 + ",X) v out(" + name2 + ",X) :- in(" + name1 + ",X).\n" 
                #result += "in(" + name1 + ",X) v out(" + name1 + ",X) :- out(" + name2 + ",X).\n" 
                #result += "in(" + name2 + ",X) v out(" + name2 + ",X) :- out(" + name1 + ",X).\n" 
                #result += "in(" + name1 + ",X) v out(" + name1 + ",X) :- in(" + name2 + ",X).\n" 
            elif self.relations == (rcc5["is_included_in"] | rcc5["overlaps"]):
                if reasoner[rnr] == reasoner["dlv"]:
                    result  = "vr(X, r" + self.ruleNum.__str__() + ") v ir(X, r" + self.ruleNum.__str__() + ") :- in(" + name1 + ",X), out(" + name2 + ",X).\n"
                    result += ":- #count{X: vrs(X), in(" + name1 + ",X), in(" + name2 + ",X)} = 0, pw.\n" 
                    result += ":- #count{X: vrs(X), out(" + name1 + ",X), in(" + name2 + ",X)} = 0, pw.\n" 
                    result += "pie(r" + self.ruleNum.__str__() + ", A, 1) :- ir(X, A), in(" + name1 + ", X), in(" + name2 + ", X), ix.\n"
                    result += "c(r" + self.ruleNum.__str__() + ", A, 1) :- vr(X, A), in(" + name1 + ", X), in(" + name2 + ", X), ix.\n\n"
                    result += "pie(r" + self.ruleNum.__str__() + ", A, 2) :- ir(X, A), out(" + name1 + ", X), in(" + name2 + ", X), ix.\n"
                    result += "c(r" + self.ruleNum.__str__() + ", A, 2) :- vr(X, A), out(" + name1 + ", X), in(" + name2 + ", X), ix.\n\n"
                elif reasoner[rnr] == reasoner["gringo"]:
                    result  = "vr(X, r" + self.ruleNum.__str__() + ") | ir(X, r" + self.ruleNum.__str__() + ") :- in(" + name1 + ",X), out(" + name2 + ",X).\n"
                    align.basePw += self.getGringoAggrRule(True, name1, True, name2, False)
                    align.basePw += self.getGringoAggrRule(False, name1, True, name2, False)
                    # align.basePw += ":- [vrs(X): in(" + name1 + ",X): in(" + name2 + ",X)]0.\n"
                    # align.basePw += ":- [vrs(X): out(" + name1 + ",X): in(" + name2 + ",X)]0.\n"
                #result += "in(" + name2 + ",X) v out(" + name2 + ",X) :- in(" + name1 + ",X).\n" 
                #result += "in(" + name1 + ",X) v out(" + name1 + ",X) :- out(" + name2 + ",X).\n" 
                #result += "in(" + name2 + ",X) v out(" + name2 + ",X) :- out(" + name1 + ",X).\n" 
                #result += "in(" + name1 + ",X) v out(" + name1 + ",X) :- in(" + name2 + ",X).\n" 
            elif self.relations == (rcc5["is_included_in"] | rcc5["disjoint"]):
                if reasoner[rnr] == reasoner["dlv"]:
                    result += ":- #count{X: vrs(X), out(" + name1 + ",X), in(" + name2 + ",X)} = 0, pw.\n"
                    result += ":- #count{X: vrs(X), in(" + name1 + ",X), in(" + name2 + ",X)} > 0, #count{Y: vrs(Y), out(" + name2 + ",Y), in(" + name1 + ",Y)} > 0, pw.\n"
                    result += ":- #count{X: vrs(X), in(" + name1 + ",X), in(" + name2 + ",X)} = 0, #count{Y: vrs(Y), out(" + name2 + ",Y), in(" + name1 + ",Y)} = 0, pw.\n"
                elif reasoner[rnr] == reasoner["gringo"]:
                    align.basePw += self.getGringoAggrRule(False, name1, True, name2, False)
                    # align.basePw += ":- [vrs(X): out(" + name1 + ",X): in(" + name2 + ",X)]0.\n"
                    align.basePw += ":- rel(" + name1 + ", " + name2 + ", \"><\").\n" 
                    align.basePw += "rel(" + name1 + ", " + name2 + ", \"<\") | rel(" + name1 + ", " + name2 + ", \"!\").\n" 
                    result += "pie(r" + self.ruleNum.__str__() + ", A, 1) :- ir(X, A), out(" + name1 + ", X), in(" + name2 + ", X), ix.\n"
                    result += "c(r" + self.ruleNum.__str__() + ", A, 1) :- vr(X, A), out(" + name1 + ", X), in(" + name2 + ", X), ix.\n\n"
                    result += "pie(r" + self.ruleNum.__str__() + ", prod(A, B), 2) :- vr(X, A), in(" + name1 + ", X), in(" + name2 + ", X), vr(Y, B), out("+ name2 + ",Y), in(" + name1 + ",Y), ix.\n"
                    result += "pie(r" + self.ruleNum.__str__() + ", A, 3) :- ir(X, A), in(" + name1 + ", X), in(" + name2 + ", X), ix.\n"
                    result += "c(r" + self.ruleNum.__str__() + ", A, 3) :- vr(X, A), in(" + name1 + ", X), in(" + name2 + ", X), ix.\n\n"
                    result += "c(r" + self.ruleNum.__str__() + ", A, 3) :- vr(X, A), in(" + name1 + ", X), out(" + name2 + ", X), ix.\n\n"
            elif self.relations == (rcc5["includes"] | rcc5["overlaps"]):
                if reasoner[rnr] == reasoner["dlv"]:
                    result += "vrs(X) v irs(X) :- out(" + name1 + ",X), in(" + name2 + ",X), pw.\n" 
                    result += ":- #count{X: vrs(X), in(" + name1 + ",X), in(" + name2 + ",X)} = 0, pw.\n" 
                    result += ":- #count{X: vrs(X), in(" + name1 + ",X), out(" + name2 + ",X)} = 0, pw.\n" 
                elif reasoner[rnr] == reasoner["gringo"]:
                    align.basePw += "vrs(X) | irs(X) :- out(" + name1 + ",X): in(" + name2 + ",X).\n"
                    align.basePw += self.getGringoAggrRule(True, name1, True, name2, False)
                    align.basePw += self.getGringoAggrRule(True, name1, False, name2, False)
                    # align.basePw += ":- [vrs(X): in(" + name1 + ",X): in(" + name2 + ",X)]0.\n"
                    # align.basePw += ":- [vrs(X): in(" + name1 + ",X): out(" + name2 + ",X)]0.\n"
            elif self.relations == (rcc5["includes"] | rcc5["disjoint"]):
                if reasoner[rnr] == reasoner["dlv"]:
                    result += ":- #count{X: vrs(X), in(" + name1 + ",X), out(" + name2 + ",X)} = 0, pw.\n"
                    result += ":- #count{X: vrs(X), in(" + name1 + ",X), in(" + name2 + ",X)} > 0, #count{Y: vrs(Y), in(" + name2 + ",Y), out(" + name1 + ",Y)} > 0, pw.\n"
                    result += ":- #count{X: vrs(X), in(" + name1 + ",X), in(" + name2 + ",X)} = 0, #count{Y: vrs(Y), in(" + name2 + ",Y), out(" + name1 + ",Y)} = 0, pw.\n"
                elif reasoner[rnr] == reasoner["gringo"]:
                    #align.basePw += ":- [vrs(X): in(" + name1 + ",X): out(" + name2 + ",X)]0.\n" 
                    align.basePw += "rel(" + name1 + ", " + name2 + ", \"!\") | rel(" + name1 + ", " + name2 + ", \">\").\n" 
                result += "pie(r" + self.ruleNum.__str__() + ", A, 1) :- ir(X, A), in(" + name1 + ", X), out(" + name2 + ", X), ix.\n"
                result += "c(r" + self.ruleNum.__str__() + ", A, 1) :- vr(X, A), in(" + name1 + ", X), out(" + name2 + ", X), ix.\n\n"
                result += "pie(r" + self.ruleNum.__str__() + ", prod(A, B), 2) :- vr(X, A), in(" + name1 + ", X), in(" + name2 + ", X), vr(Y, B), in("+ name2 + ",Y), out(" + name1 + ",Y), ix.\n"
                result += "pie(r" + self.ruleNum.__str__() + ", A, 3) :- ir(X, A), in(" + name1 + ", X), in(" + name2 + ", X), ix.\n"
                result += "c(r" + self.ruleNum.__str__() + ", A, 3) :- vr(X, A), in(" + name1 + ", X), in(" + name2 + ", X), ix.\n\n"
                result += "c(r" + self.ruleNum.__str__() + ", A, 3) :- vr(X, A), out(" + name1 + ", X), in(" + name2 + ", X), ix.\n\n"
            elif self.relations == (rcc5["includes"] | rcc5["is_included_in"] | rcc5["equals"]):
                if reasoner[rnr] == reasoner["dlv"]:
                    result += "vr(X, r" + self.ruleNum.__str__() + ") v ir(X, r" + self.ruleNum.__str__() + ") :- out(" + name1 + ",X), in(" + name2 + ",X).\n" 
                    result += "vr(X, r" + self.ruleNum.__str__() + ") v ir(X, r" + self.ruleNum.__str__() + ") :- in(" + name1 + ",X), out(" + name2 + ",X).\n" 
                    result += ":- #count{X: vrs(X), in(" + name1 + ",X), out(" + name2 + ", X)} > 0, #count{Y: vrs(Y), out(" + name1 + ",Y), in(" + name2 + ", Y)} > 0.\n"
                    result += ":- #count{X: vrs(X), in(" + name1 + ",X), in(" + name2 + ", X)} = 0.\n\n"
                elif reasoner[rnr] == reasoner["gringo"]:
                    result += "vr(X, r" + self.ruleNum.__str__() + ") | ir(X, r" + self.ruleNum.__str__() + ") :- out(" + name1 + ",X), in(" + name2 + ",X).\n" 
                    result += "vr(X, r" + self.ruleNum.__str__() + ") | ir(X, r" + self.ruleNum.__str__() + ") :- in(" + name1 + ",X), out(" + name2 + ",X).\n"

                    firstRule = self.getGringoAggrRule(True, name1, False, name2, False).replace(":- ", ":- 1 <= ").replace("0.\n", ", ")
                    secodRule = self.getGringoAggrRule(False, name1, True, name2, False).replace(":- ", "1 <= ").replace("0.", ".")
                    thirdRule = self.getGringoAggrRule(True, name1, True, name2, False).replace("0.\n", "0.\n\n")
                    result += firstRule + secodRule + thirdRule
                    # result += ":- 1[vrs(X): in(" + name1 + ",X): out(" + name2 + ", X)], 1[vrs(X): out(" + name1 + ",X): in(" + name2 + ", X)].\n"
                    # result += ":- [vrs(X): in(" + name1 + ",X): in(" + name2 + ", X)]0.\n\n"
            elif self.relations == (rcc5["is_included_in"] | rcc5["equals"] | rcc5["overlaps"]):
                if reasoner[rnr] == reasoner["dlv"]:
                    result += ":- #count{X: vrs(X), in(" + name1 + ",X), out(" + name2 + ", X)} > 0, #count{Y: vrs(Y), out(" + name1 + ",Y), in(" + name2 + ", Y)} = 0.\n"
                    result += ":- #count{X: vrs(X), in(" + name1 + ",X), in(" + name2 + ", X)} = 0.\n\n"
                elif reasoner[rnr] == reasoner["gringo"]:

                    firstRule = self.getGringoAggrRule(True, name1, False, name2, False).replace(":- ", ":- 1 <= ").replace("0.\n", ",")
                    secodRule = self.getGringoAggrRule(False, name1, True, name2, False).replace(":- ", "")
                    thirdRule = self.getGringoAggrRule(True, name1, True, name2, False).replace("0.\n", "0.\n\n")
                    result += firstRule + secodRule + thirdRule
                    # result += ":- 1[vrs(X): in(" + name1 + ",X): out(" + name2 + ", X)], [vrs(X): out(" + name1 + ",X): in(" + name2 + ", X)]0.\n"
                    # result += ":- [vrs(X): in(" + name1 + ",X): in(" + name2 + ", X)]0.\n\n"
            elif self.relations == (rcc5["includes"] | rcc5["equals"] | rcc5["overlaps"]):
                if reasoner[rnr] == reasoner["dlv"]:
                    result += ":- #count{X: vrs(X), in(" + name1 + ",X), out(" + name2 + ", X)} = 0, #count{Y: vrs(Y), out(" + name1 + ",Y), in(" + name2 + ", Y)} > 0.\n"
                    result += ":- #count{X: vrs(X), in(" + name1 + ",X), in(" + name2 + ", X)} = 0.\n\n"
                elif reasoner[rnr] == reasoner["gringo"]:
                    firstRule = self.getGringoAggrRule(True, name1, False, name2, False).replace(".\n", ",")
                    secodRule = self.getGringoAggrRule(False, name1, True, name2, False).replace(":- ", "1 <= ").replace("0.", ".")
                    thirdRule = self.getGringoAggrRule(True, name1, True, name2, False).replace("0.\n", "0.\n\n")
                    result += firstRule + secodRule + thirdRule
                    # result += ":- [vrs(X): in(" + name1 + ",X): out(" + name2 + ", X)]0, 1[vrs(X): out(" + name1 + ",X): in(" + name2 + ", X)].\n"
                    # result += ":- [vrs(X): in(" + name1 + ",X): in(" + name2 + ", X)]0.\n\n"
            elif self.relations == (rcc5["equals"] | rcc5["includes"] | rcc5["disjoint"]):
                if reasoner[rnr] == reasoner["dlv"]:
                    result += ":- #count{X: vrs(X), out(" + name1 + ", X), in(" + name2 + ", X)} = 0, #count{Y: vrs(Y), in(" + name1 +", Y), in(" + name2 + ", Y)} = 0.\n"
                    result += ":- #count{X: vrs(X), out(" + name1 + ", X), in(" + name2 + ", X)} > 0, #count{Y: vrs(Y), in(" + name1 +", Y), in(" + name2 + ", Y)} > 0.\n"
                    result += ":- #count{X: vrs(X), out(" + name1 + ", X), in(" + name2 + ", X)} > 0, #count{Y: vrs(Y), in(" + name1 +", Y), in(" + name2 + ", Y)} = 0, #count{Z: vrs(Z), in(" + name1 + ", Z), out(" + name2 + ", Z)} = 0.\n\n"
                elif reasoner[rnr] == reasoner["gringo"]:
                    # TODO
                    result = ""
            elif self.relations == (rcc5["equals"] | rcc5["is_included_in"] | rcc5["disjoint"]):
                if reasoner[rnr] == reasoner["dlv"]:
                    result += ":- #count{X: vrs(X), in(" + name1 + ", X), out(" + name2 + ", X)} = 0, #count{Y:vrs(Y), in(" + name1 + ", Y), in(" + name2 + ", Y)} = 0.\n"
                    result += ":- #count{X: vrs(X), in(" + name1 + ", X), out(" + name2 + ", X)} > 0, #count{Y:vrs(Y), in(" + name1 + ", Y), in(" + name2 + ", Y)} > 0.\n"
                    result += ":- #count{X: vrs(X), in(" + name1 + ", X), out(" + name2 + ", X)} > 0, #count{Y:vrs(Y), in(" + name1 + ", Y), in(" + name2 + ", Y)} = 0, #count{Z: vrs(Z), out(" + name1 + ", Z), in(" + name2 + ", Z)} = 0.\n\n"
                elif reasoner[rnr] == reasoner["gringo"]:
                    # TODO
                    result = ""
            elif self.relations == (rcc5["includes"] | rcc5["is_included_in"] | rcc5["overlaps"]):
                if reasoner[rnr] == reasoner["dlv"]:
                    result += ":- #count{X: vrs(X), in(" + name1 + ",X), out(" + name2 + ", X)} = 0, #count{Y: vrs(Y), out(" + name1 + ",Y), in(" + name2 + ", Y)} = 0, #count{Z: vrs(Z), in(" + name1 + ",Z), in(" + name2 + ", Z)} > 0.\n"
                    result += ":- #count{X: vrs(X), in(" + name1 + ",X), in(" + name2 + ", X)} = 0.\n\n"
                elif reasoner[rnr] == reasoner["gringo"]:

                    firstRule = self.getGringoAggrRule(True, name1, False, name2, False).replace(".\n", ",")
                    secodRule = self.getGringoAggrRule(False, name1, True, name2, False).replace(":- ", "").replace(".\n", ",")
                    thirdRule = self.getGringoAggrRule(True, name1, True, name2, False).replace(":- ", "").replace("0.\n", ".\n")
                    forthRule = self.getGringoAggrRule(True, name1, True, name2, False).replace(".\n", ".\n\n")
                    result += firstRule + secodRule + thirdRule + forthRule
                    # result += ":- [vrs(X): in(" + name1 + ",X): out(" + name2 + ", X)]0, [vrs(X): out(" + name1 + ",X): in(" + name2 + ", X)]0, 1[vrs(X): in(" + name1 + ",X): in(" + name2 + ", X)].\n"
                    # result += ":- [vrs(X): in(" + name1 + ",X): in(" + name2 + ", X)]0.\n\n"
            elif self.relations == (rcc5["disjoint"] | rcc5["equals"] | rcc5["overlaps"]):
                if reasoner[rnr] == reasoner["dlv"]:
                    result  = ":- #count{X : vrs(X), in(" + name1 + ", X), out(" + name2 + ", X)} > 0, #count{Y : vrs(Y), out(" + name1 + ", Y ), in(" + name2 + ", Y )} = 0.\n"
                    result += ":- #count{X : vrs(X), in(" + name1 + ", X), out(" + name2 + ", X)} = 0, #count{Y : vrs(Y), out(" + name1 + ", Y ), in(" + name2 + ", Y )} > 0.\n"
                    result += ":- #count{X : vrs(X), in(" + name1 + ", X), out(" + name2 + ", X)} = 0, #count{Y : vrs(Y), in(" + name1 + ", Y ), in(" + name2 + ", Y )} = 0, #count{Z : vrs(Z), out(" + name1 + ", Z), in(" + name2 + ", Z)} = 0.\n\n"
                elif reasoner[rnr] == reasoner["gringo"]:
                    # TODO
                    result = ""
            elif self.relations == (rcc5["disjoint"] | rcc5["is_included_in"] | rcc5["overlaps"]):
                if reasoner[rnr] == reasoner["dlv"]:
                    result = ":- #count{X : vrs(X), in(" + name1 + ", X), out(" + name2 + ", X)} = 0, #count{Y: vrs(Y), out(" + name1 + ", Y), in(" + name2 + ", Y)} = 0.\n"\
                           ":- #count{X : vrs(X), in(" + name1 + ", X), out(" + name2 + ", X)} > 0, #count{Y: vrs(Y), in(" + name1 + ", Y), in(" + name2 + ", Y)} > 0, #count{Z: vrs(Z), out(" + name1 + ", Z), in(" + name2 + ", Z)} = 0.\n\n"
                elif reasoner[rnr] == reasoner["gringo"]:
                    # TODO
                    result = ""
            elif self.relations == (rcc5["includes"] | rcc5["disjoint"] | rcc5["overlaps"]):
                if reasoner[rnr] == reasoner["dlv"]:
                    result = ":- #count{X : vrs(X), in(" + name1 + ", X), out(" + name2 + ", X)} = 0, #count{Y : vrs(Y ), out(" + name1 + ", Y), in(" + name2 + ", Y )} = 0.\n"\
                           ":- #count{X : vrs(X), in(" + name1 + ", X), out(" + name2 + ", X)} = 0, #count{Y : vrs(Y), in(" + name1 + ", Y), in(" + name2 + ", Y )} > 0, #count{Z : vrs(Z), out(" + name1 + ", Z), in(" + name2 + ", Z)} > 0.\n"
                elif reasoner[rnr] == reasoner["gringo"]:
                    # TODO
                    result = ""
            elif self.relations == (rcc5["includes"] | rcc5["is_included_in"] | rcc5["disjoint"]):
                if reasoner[rnr] == reasoner["dlv"]:
                    result = ":- #count{X: vrs(X), in(" + name1 + ", X), out(" + name2 + ", X)} = 0, #count{Y: vrs(Y), out(" + name1 + ", Y), in(" + name2 + ", Y)} = 0.\n"\
                           ":- #count{X: vrs(X), in(" + name1 + ", X), out(" + name2 + ", X)} > 0, #count{Y: vrs(Y), in(" + name1 + ", Y), in(" + name2 + ", Y)} > 0, #count{Z : vrs(Z), out(" + name1 + ", Z), in(" + name2 + ", Z)} > 0.\n\n"
                elif reasoner[rnr] == reasoner["gringo"]:
                    # TODO
                    result = ""
            elif self.relations == (rcc5["includes"] | rcc5["is_included_in"] | rcc5["overlaps"] | rcc5["equals"]):
                if reasoner[rnr] == reasoner["dlv"]:
                    result = ":- #count{X: vrs(X), in(" + name1 + ", X), out(" + name2 + ", X)} > 0,"\
                                "#count{Y: vrs(Y), in(" + name1 + ", Y), in(" + name2 + ", Y)} = 0,"\
                                "#count{Z: vrs(Z), out(" + name1 + ", Z), in(" + name2 + ", Z)} > 0.\n"
                elif reasoner[rnr] == reasoner["gringo"]:
                    # TODO
                    result = ""
            elif self.relations == (rcc5["disjoint"] | rcc5["is_included_in"] | rcc5["overlaps"] | rcc5["equals"]):
                if reasoner[rnr] == reasoner["dlv"]:
                    result = ":- #count{X: vrs(X), in(" + name1 + ", X), out(" + name2 + ", X)} > 0,"\
                                "#count{Y: vrs(Y), in(" + name1 + ", Y), in(" + name2 + ", Y)} > 0,"\
                                "#count{Z: vrs(Z), out(" + name1 + ", Z), in(" + name2 + ", Z)} = 0.\n"
                elif reasoner[rnr] == reasoner["gringo"]:
                    # TODO
                    result = ""
            elif self.relations == (rcc5["includes"] | rcc5["disjoint"] | rcc5["overlaps"] | rcc5["equals"]):
                if reasoner[rnr] == reasoner["dlv"]:
                    result = ":- #count{X: vrs(X), in(" + name1 + ", X), out(" + name2 + ", X)} = 0,"\
                                "#count{Y: vrs(Y), in(" + name1 + ", Y), in(" + name2 + ", Y)} > 0,"\
                                "#count{Z: vrs(Z), out(" + name1 + ", Z), in(" + name2 + ", Z)} > 0.\n"
                elif reasoner[rnr] == reasoner["gringo"]:
                    # TODO
                    result = ""
            elif self.relations == (rcc5["includes"] | rcc5["is_included_in"] | rcc5["disjoint"] | rcc5["equals"]):
                if reasoner[rnr] == reasoner["dlv"]:
                    result = ":- #count{X: vrs(X), in(" + name1 + ", X), out(" + name2 + ", X)} > 0,"\
                                "#count{Y: vrs(Y), in(" + name1 + ", Y), in(" + name2 + ", Y)} > 0,"\
                                "#count{Z: vrs(Z), out(" + name1 + ", Z), in(" + name2 + ", Z)} > 0.\n"
                elif reasoner[rnr] == reasoner["gringo"]:
                    # TODO
                    result = ""
            elif self.relations == (rcc5["includes"] | rcc5["is_included_in"] | rcc5["overlaps"] | rcc5["disjoint"]):
                if reasoner[rnr] == reasoner["dlv"]:
                    result = ":- #count{X: vrs(X), in(" + name1 + ", X), out(" + name2 + ", X)} = 0,"\
                                "#count{Y: vrs(Y), out(" + name1 + ", Y), in(" + name2 + ", Y)} = 0.\n"
                elif reasoner[rnr] == reasoner["gringo"]:
                    # TODO
                    result = ""
            elif self.relations == relation["+="]: # lsum
                name3 = self.taxon3.dlvName()
                if reasoner[rnr] == reasoner["dlv"]:
                    result += ":- #count{X: vrs(X), out(" + name1 + ",X), in(" + name3 + ",X)} = 0, pw.\n" 
                    result += ":- #count{X: vrs(X), in(" + name1 + ",X), in(" + name3 + ",X)} = 0, pw.\n" 
                    result += ":- #count{X: vrs(X), out(" + name2 + ",X), in(" + name3 + ",X)} = 0, pw.\n" 
                    result += ":- #count{X: vrs(X), in(" + name2 + ",X), in(" + name3 + ",X)} = 0, pw.\n" 
                elif reasoner[rnr] == reasoner["gringo"]:
                    align.basePw += self.getGringoAggrRule(False, name1, True, name3, False)
                    align.basePw += self.getGringoAggrRule(True, name1, True, name3, False)
                    align.basePw += self.getGringoAggrRule(False, name2, True, name3, False)
                    align.basePw += self.getGringoAggrRule(True, name2, True, name3, False)
                    # align.basePw += ":- [vrs(X): out(" + name1 + ",X): in(" + name3 + ",X)]0.\n"
                    # align.basePw += ":- [vrs(X): in(" + name1 + ",X): in(" + name3 + ",X)]0.\n"
                    # align.basePw += ":- [vrs(X): out(" + name2 + ",X): in(" + name3 + ",X)]0.\n"
                    # align.basePw += ":- [vrs(X): in(" + name2 + ",X): in(" + name3 + ",X)]0.\n"
                result += "pie(r" + self.ruleNum.__str__() + ", A, 1) :- ir(X, A), out(" + name1 + ", X), in(" + name3 + ", X), ix.\n"
                result += "c(r" + self.ruleNum.__str__() + ", A, 1) :- vr(X, A), out(" + name1 + ", X), in(" + name3 + ", X), ix.\n\n"
                result += "pie(r" + self.ruleNum.__str__() + ", A, 2) :- ir(X, A), in(" + name1 + ", X), in(" + name3 + ", X), ix.\n"
                result += "c(r" + self.ruleNum.__str__() + ", A, 2) :- vr(X, A), in(" + name1 + ", X), in(" + name3 + ", X), ix.\n\n"
                result += "pie(r" + self.ruleNum.__str__() + ", A, 3) :- ir(X, A), out(" + name2 + ", X), in(" + name3 + ", X), ix.\n"
                result += "c(r" + self.ruleNum.__str__() + ", A, 3) :- vr(X, A), out(" + name2 + ", X), in(" + name3 + ", X), ix.\n\n"
                result += "pie(r" + self.ruleNum.__str__() + ", A, 4) :- ir(X, A), in(" + name2 + ", X), in(" + name3 + ", X), ix.\n"
                result += "c(r" + self.ruleNum.__str__() + ", A, 4) :- vr(X, A), in(" + name2 + ", X), in(" + name3 + ", X), ix.\n\n"
                result += "ir(X, r" + self.ruleNum.__str__() + ") :- in(" + name1 + ",X), out(" + name3 + ",X), pw.\n" 
                result += "ir(X, r" + self.ruleNum.__str__() + ") :- in(" + name2 + ",X), out(" + name3 + ",X), pw.\n" 
                #result += "in(" + name3 + ",X) :- in(" + name1 + ",X).\n" 
                #result += "in(" + name3 + ",X) :- in(" + name2 + ",X).\n" 
                #result += "out(" + name1 + ",X) :- out(" + name3 + ",X).\n" 
                #result += "out(" + name2 + ",X) :- out(" + name3 + ",X).\n" 
                #result += "in(" + name1 + ",X) v in(" + name2 + ",X) :- in(" + name3 + ",X).\n" 
                #result += "out(" +name3 + ",X) :- out(" + name1 + ",X), out(" + name2 + ",X).\n"
            elif self.relations == relation["=-"]: # rdiff
                name3 = self.taxon3.dlvName()
                if reasoner[rnr] == reasoner["dlv"]:
                    result  = ":- #count{X: vrs(X), out(" + name1 + ",X), in(" + name2 + ",X)} = 0.\n" 
                    result += ":- #count{X: vrs(X), in(" + name1 + ",X), in(" + name2 + ",X)} = 0.\n" 
                    result += ":- #count{X: vrs(X), out(" + name3 + ",X), in(" + name2 + ",X)} = 0.\n" 
                    result += ":- #count{X: vrs(X), in(" + name3 + ",X), in(" + name2 + ",X)} = 0.\n" 
                elif reasoner[rnr] == reasoner["gringo"]:
                    result = self.getGringoAggrRule(False, name1, True, name2, False)
                    result += self.getGringoAggrRule(True, name1, True, name2, False)
                    result += self.getGringoAggrRule(False, name3, True, name2, False)
                    result += self.getGringoAggrRule(True, name3, True, name2, False)
                    # result  = ":- [vrs(X): out(" + name1 + ",X): in(" + name2 + ",X)]0.\n"
                    # result += ":- [vrs(X): in(" + name1 + ",X): in(" + name2 + ",X)]0.\n"
                    # result += ":- [vrs(X): out(" + name3 + ",X): in(" + name2 + ",X)]0.\n"
                    # result += ":- [vrs(X): in(" + name3 + ",X): in(" + name2 + ",X)]0.\n"
                result += "pie(r" + self.ruleNum.__str__() + ", A, 1) :- ir(X, A), out(" + name1 + ", X), in(" + name2 + ", X), ix.\n"
                result += "c(r" + self.ruleNum.__str__() + ", A, 1) :- vr(X, A), out(" + name1 + ", X), in(" + name2 + ", X), ix.\n\n"
                result += "pie(r" + self.ruleNum.__str__() + ", A, 2) :- ir(X, A), in(" + name1 + ", X), in(" + name2 + ", X), ix.\n"
                result += "c(r" + self.ruleNum.__str__() + ", A, 2) :- vr(X, A), in(" + name1 + ", X), in(" + name2 + ", X), ix.\n\n"
                result += "pie(r" + self.ruleNum.__str__() + ", A, 3) :- ir(X, A), out(" + name3 + ", X), in(" + name2 + ", X), ix.\n"
                result += "c(r" + self.ruleNum.__str__() + ", A, 3) :- vr(X, A), out(" + name3 + ", X), in(" + name2 + ", X), ix.\n\n"
                result += "pie(r" + self.ruleNum.__str__() + ", A, 4) :- ir(X, A), in(" + name3 + ", X), in(" + name2 + ", X), ix.\n"
                result += "c(r" + self.ruleNum.__str__() + ", A, 4) :- vr(X, A), in(" + name3 + ", X), in(" + name2 + ", X), ix.\n\n"
                result += "ir(X, r" + self.ruleNum.__str__() + ") :- in(" + name1 + ",X), out(" + name2 + ",X).\n" 
                result += "ir(X, r" + self.ruleNum.__str__() + ") :- in(" + name3 + ",X), out(" + name2 + ",X).\n" 
            elif self.relations == relation["+3="]:
                name3 = self.taxon3.dlvName()
                name4 = self.taxon4.dlvName()
                if reasoner[rnr] == reasoner["dlv"]:
                    result  = ":- #count{X: vrs(X), out(" + name1 + ",X), in(" + name4 + ",X)} = 0.\n" 
                    result += ":- #count{X: vrs(X), in(" + name1 + ",X), in(" + name4 + ",X)} = 0.\n" 
                    result += ":- #count{X: vrs(X), out(" + name2 + ",X), in(" + name4 + ",X)} = 0.\n" 
                    result += ":- #count{X: vrs(X), in(" + name2 + ",X), in(" + name4 + ",X)} = 0.\n"
                    result += ":- #count{X: vrs(X), out(" + name3 + ",X), in(" + name4 + ",X)} = 0.\n" 
                    result += ":- #count{X: vrs(X), in(" + name3 + ",X), in(" + name4 + ",X)} = 0.\n" 
                elif reasoner[rnr] == reasoner["gringo"]:
                    result = self.getGringoAggrRule(False, name1, True, name4, False)
                    result += self.getGringoAggrRule(True, name1, True, name4, False)
                    result += self.getGringoAggrRule(False, name2, True, name4, False)
                    result += self.getGringoAggrRule(True, name2, True, name4, False)
                    result += self.getGringoAggrRule(False, name3, True, name4, False)
                    result += self.getGringoAggrRule(True, name3, True, name4, False)
                    # result  = ":- [vrs(X): out(" + name1 + ",X): in(" + name4 + ",X)]0.\n"
                    # result += ":- [vrs(X): in(" + name1 + ",X): in(" + name4 + ",X)]0.\n"
                    # result += ":- [vrs(X): out(" + name2 + ",X): in(" + name4 + ",X)]0.\n"
                    # result += ":- [vrs(X): in(" + name2 + ",X): in(" + name4 + ",X)]0.\n"
                    # result += ":- [vrs(X): out(" + name3 + ",X): in(" + name4 + ",X)]0.\n"
                    # result += ":- [vrs(X): in(" + name3 + ",X): in(" + name4 + ",X)]0.\n"
                result += "ir(X, r" + self.ruleNum.__str__() + ") :- in(" + name1 + ",X), out(" + name4 + ",X).\n" 
                result += "ir(X, r" + self.ruleNum.__str__() + ") :- in(" + name2 + ",X), out(" + name4 + ",X).\n"
                result += "ir(X, r" + self.ruleNum.__str__() + ") :- in(" + name3 + ",X), out(" + name4 + ",X).\n"
                result += "ir(X, r" + self.ruleNum.__str__() + ") :- out(" +name1 + ",X), out(" + name2 + ",X),\
                            out(" + name3 + ",X), in(" + name4 + ",X).\n"
            elif self.relations == relation["+4="]:
                name3 = self.taxon3.dlvName()
                name4 = self.taxon4.dlvName()
                name5 = self.taxon5.dlvName()
                if reasoner[rnr] == reasoner["dlv"]:
                    result  = ":- #count{X: vrs(X), out(" + name1 + ",X), in(" + name5 + ",X)} = 0.\n" 
                    result += ":- #count{X: vrs(X), in(" + name1 + ",X), in(" + name5 + ",X)} = 0.\n" 
                    result += ":- #count{X: vrs(X), out(" + name2 + ",X), in(" + name5 + ",X)} = 0.\n" 
                    result += ":- #count{X: vrs(X), in(" + name2 + ",X), in(" + name5 + ",X)} = 0.\n"
                    result += ":- #count{X: vrs(X), out(" + name3 + ",X), in(" + name5 + ",X)} = 0.\n" 
                    result += ":- #count{X: vrs(X), in(" + name3 + ",X), in(" + name5 + ",X)} = 0.\n"
                    result += ":- #count{X: vrs(X), out(" + name4 + ",X), in(" + name5 + ",X)} = 0.\n" 
                    result += ":- #count{X: vrs(X), in(" + name4 + ",X), in(" + name5 + ",X)} = 0.\n"
                elif reasoner[rnr] == reasoner["gringo"]:
                    result = self.getGringoAggrRule(False, name1, True, name5, False)
                    result += self.getGringoAggrRule(True, name1, True, name5, False)
                    result += self.getGringoAggrRule(False, name2, True, name5, False)
                    result += self.getGringoAggrRule(True, name2, True, name5, False)
                    result += self.getGringoAggrRule(False, name3, True, name5, False)
                    result += self.getGringoAggrRule(True, name3, True, name5, False)
                    result += self.getGringoAggrRule(False, name4, True, name5, False)
                    result += self.getGringoAggrRule(True, name4, True, name5, False)
                    # result  = ":- [vrs(X): out(" + name1 + ",X): in(" + name5 + ",X)]0.\n"
                    # result += ":- [vrs(X): in(" + name1 + ",X): in(" + name5 + ",X)]0.\n"
                    # result += ":- [vrs(X): out(" + name2 + ",X): in(" + name5 + ",X)]0.\n"
                    # result += ":- [vrs(X): in(" + name2 + ",X): in(" + name5 + ",X)]0.\n"
                    # result += ":- [vrs(X): out(" + name3 + ",X): in(" + name5 + ",X)]0.\n"
                    # result += ":- [vrs(X): in(" + name3 + ",X): in(" + name5 + ",X)]0.\n"
                    # result += ":- [vrs(X): out(" + name4 + ",X): in(" + name5 + ",X)]0.\n"
                    # result += ":- [vrs(X): in(" + name4 + ",X): in(" + name5 + ",X)]0.\n"
                result += "ir(X, r" + self.ruleNum.__str__() + ") :- in(" + name1 + ",X), out(" + name5 + ",X).\n" 
                result += "ir(X, r" + self.ruleNum.__str__() + ") :- in(" + name2 + ",X), out(" + name5 + ",X).\n"
                result += "ir(X, r" + self.ruleNum.__str__() + ") :- in(" + name3 + ",X), out(" + name5 + ",X).\n"
                result += "ir(X, r" + self.ruleNum.__str__() + ") :- in(" + name4 + ",X), out(" + name5 + ",X).\n" 
            elif self.relations == relation["=+"] or self.relations == relation["-="]: # rsum and ldiff
                name3 = self.taxon3.dlvName()
                if reasoner[rnr] == reasoner["dlv"]:
                    result  = ":- #count{X: vrs(X), out(" + name2 + ",X), in(" + name1 + ",X)} = 0.\n" 
                    result += ":- #count{X: vrs(X), in(" + name2 + ",X), in(" + name1 + ",X)} = 0.\n" 
                    result += ":- #count{X: vrs(X), out(" + name3 + ",X), in(" + name1 + ",X)} = 0.\n" 
                    result += ":- #count{X: vrs(X), in(" + name3 + ",X), in(" + name1 + ",X)} = 0.\n" 
                elif reasoner[rnr] == reasoner["gringo"]:
                    result = self.getGringoAggrRule(False, name2, True, name1, False)
                    result += self.getGringoAggrRule(True, name2, True, name1, False)
                    result += self.getGringoAggrRule(False, name3, True, name1, False)
                    result += self.getGringoAggrRule(True, name3, True, name1, False)
                    # result  = ":- [vrs(X): out(" + name2 + ",X): in(" + name1 + ",X)]0.\n"
                    # result += ":- [vrs(X): in(" + name2 + ",X): in(" + name1 + ",X)]0.\n"
                    # result += ":- [vrs(X): out(" + name3 + ",X): in(" + name1 + ",X)]0.\n"
                    # result += ":- [vrs(X): in(" + name3 + ",X): in(" + name1 + ",X)]0.\n"
                result += "ir(X, r" + self.ruleNum.__str__() + ") :- in(" + name2 + ",X), out(" + name1 + ",X).\n" 
                result += "ir(X, r" + self.ruleNum.__str__() + ") :- in(" + name3 + ",X), out(" + name1 + ",X).\n"
            elif self.relations == relation["=3+"]:
                name3 = self.taxon3.dlvName()
                name4 = self.taxon4.dlvName()
                if reasoner[rnr] == reasoner["dlv"]:
                    result  = ":- #count{X: vrs(X), out(" + name2 + ",X), in(" + name1 + ",X)} = 0.\n" 
                    result += ":- #count{X: vrs(X), in(" + name2 + ",X), in(" + name1 + ",X)} = 0.\n" 
                    result += ":- #count{X: vrs(X), out(" + name3 + ",X), in(" + name1 + ",X)} = 0.\n" 
                    result += ":- #count{X: vrs(X), in(" + name3 + ",X), in(" + name1 + ",X)} = 0.\n"
                    result += ":- #count{X: vrs(X), out(" + name4 + ",X), in(" + name1 + ",X)} = 0.\n" 
                    result += ":- #count{X: vrs(X), in(" + name4 + ",X), in(" + name1 + ",X)} = 0.\n" 
                elif reasoner[rnr] == reasoner["gringo"]:
                    result = self.getGringoAggrRule(False, name2, True, name1, False)
                    result += self.getGringoAggrRule(True, name2, True, name1, False)
                    result += self.getGringoAggrRule(False, name3, True, name1, False)
                    result += self.getGringoAggrRule(True, name3, True, name1, False)
                    result += self.getGringoAggrRule(False, name4, True, name1, False)
                    result += self.getGringoAggrRule(True, name4, True, name1, False)
                    # result  = ":- [vrs(X): out(" + name2 + ",X): in(" + name1 + ",X)]0.\n"
                    # result += ":- [vrs(X): in(" + name2 + ",X): in(" + name1 + ",X)]0.\n"
                    # result += ":- [vrs(X): out(" + name3 + ",X): in(" + name1 + ",X)]0.\n"
                    # result += ":- [vrs(X): in(" + name3 + ",X): in(" + name1 + ",X)]0.\n"
                    # result += ":- [vrs(X): out(" + name4 + ",X): in(" + name1 + ",X)]0.\n"
                    # result += ":- [vrs(X): in(" + name4 + ",X): in(" + name1 + ",X)]0.\n"
                result += "ir(X, r" + self.ruleNum.__str__() + ") :- in(" + name2 + ",X), out(" + name1 + ",X).\n" 
                result += "ir(X, r" + self.ruleNum.__str__() + ") :- in(" + name3 + ",X), out(" + name1 + ",X).\n"
                result += "ir(X, r" + self.ruleNum.__str__() + ") :- in(" + name4 + ",X), out(" + name1 + ",X).\n"
            elif self.relations == relation["=4+"]:
                name3 = self.taxon3.dlvName()
                name4 = self.taxon4.dlvName()
                name5 = self.taxon5.dlvName()
                if reasoner[rnr] == reasoner["dlv"]:
                    result  = ":- #count{X: vrs(X), out(" + name2 + ",X), in(" + name1 + ",X)} = 0.\n" 
            	    result += ":- #count{X: vrs(X), in(" + name2 + ",X), in(" + name1 + ",X)} = 0.\n" 
            	    result += ":- #count{X: vrs(X), out(" + name3 + ",X), in(" + name1 + ",X)} = 0.\n" 
            	    result += ":- #count{X: vrs(X), in(" + name3 + ",X), in(" + name1 + ",X)} = 0.\n"
            	    result += ":- #count{X: vrs(X), out(" + name4 + ",X), in(" + name1 + ",X)} = 0.\n" 
            	    result += ":- #count{X: vrs(X), in(" + name4 + ",X), in(" + name1 + ",X)} = 0.\n"
            	    result += ":- #count{X: vrs(X), out(" + name5 + ",X), in(" + name1 + ",X)} = 0.\n" 
            	    result += ":- #count{X: vrs(X), in(" + name5 + ",X), in(" + name1 + ",X)} = 0.\n"
                elif reasoner[rnr] == reasoner["gringo"]:
                    result = self.getGringoAggrRule(False, name2, True, name1, False)
                    result += self.getGringoAggrRule(True, name2, True, name1, False)
                    result += self.getGringoAggrRule(False, name3, True, name1, False)
                    result += self.getGringoAggrRule(True, name3, True, name1, False)
                    result += self.getGringoAggrRule(False, name4, True, name1, False)
                    result += self.getGringoAggrRule(True, name4, True, name1, False)
                    result += self.getGringoAggrRule(False, name5, True, name1, False)
                    result += self.getGringoAggrRule(True, name5, True, name1, False)
                    # result  = ":- [vrs(X): out(" + name2 + ",X): in(" + name1 + ",X)]0.\n"
            	    # result += ":- [vrs(X): in(" + name2 + ",X): in(" + name1 + ",X)]0.\n"
            	    # result += ":- [vrs(X): out(" + name3 + ",X): in(" + name1 + ",X)]0.\n"
            	    # result += ":- [vrs(X): in(" + name3 + ",X): in(" + name1 + ",X)]0.\n"
            	    # result += ":- [vrs(X): out(" + name4 + ",X): in(" + name1 + ",X)]0.\n"
            	    # result += ":- [vrs(X): in(" + name4 + ",X): in(" + name1 + ",X)]0.\n"
            	    # result += ":- [vrs(X): out(" + name5 + ",X): in(" + name1 + ",X)]0.\n"
            	    # result += ":- [vrs(X): in(" + name5 + ",X): in(" + name1 + ",X)]0.\n"
                result += "ir(X, r" + self.ruleNum.__str__() + ") :- in(" + name2 + ",X), out(" + name1 + ",X).\n" 
                result += "ir(X, r" + self.ruleNum.__str__() + ") :- in(" + name3 + ",X), out(" + name1 + ",X).\n"
                result += "ir(X, r" + self.ruleNum.__str__() + ") :- in(" + name4 + ",X), out(" + name1 + ",X).\n"
                result += "ir(X, r" + self.ruleNum.__str__() + ") :- in(" + name5 + ",X), out(" + name1 + ",X).\n" 
                #result += "in(" + name1 + ",X) :- in(" + name2 + ",X).\n" 
                #result += "in(" + name1 + ",X) :- in(" + name3 + ",X).\n" 
                #result += "out(" + name2 + ",X) :- out(" + name1 + ",X).\n" 
                #result += "out(" + name3 + ",X) :- out(" + name1 + ",X).\n" 
                #result += "in(" + name2 + ",X) v in(" + name3 + ",X) :- in(" + name1 + ",X).\n" 
                #result += "out(" +name1 + ",X) :- out(" + name2 + ",X), out(" + name3 + ",X).\n" 
            else:
                print "Relation ",self.relations," is not yet supported!!!!"
                result = "\n"
        elif encode[enc] & encode["direct"]:
            prefix = "label(" + name1 + ", " + name2 +", "
            result = ""
            firstrel = True
            if self.relations < relation["+="]:
                if self.relations & rcc5["includes"] == rcc5["includes"]:
                    result  = prefix + "in) "
                    firstrel = False
                if self.relations & rcc5["is_included_in"] == rcc5["is_included_in"]:
                    if firstrel:
                        result  = prefix + "ls) "
                        firstrel = False
                    else:
                        result += " v " + prefix + "ls) "
                if self.relations & rcc5["overlaps"] == rcc5["overlaps"]:
                    if firstrel:
                        result  = prefix + "ol) "
                        firstrel = False
                    else:
                        result += " v " + prefix + "ol) "
                if self.relations & rcc5["disjoint"] == rcc5["disjoint"]:
                    if firstrel:
                        result  = prefix + "ds) "
                        firstrel = False
                    else:
                        result += " v " + prefix + "ds) "
                if self.relations & rcc5["equals"] == rcc5["equals"]:
                    if firstrel:
                        result  = prefix + "eq) "
                        firstrel = False
                    else:
                        result += " v " + prefix + "eq) "
                if not firstrel:
                    result += "."
            elif self.relations == relation["+="]:
                result = "sum(" + self.taxon3.dlvName() + "," + name1 + "," + name2 + ").\n"
            elif self.relations == relation["=+"]:
                result = "sum(" + name1 + "," + name2 + "," + self.taxon3.dlvName() + ").\n"
        else:
            raise Exception("Encoding:", enc, " is not supported !!")
        return result
