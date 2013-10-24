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
        if (initInput == ""):
            self.taxon1 = Taxon()
            self.taxon2 = Taxon()
            self.taxon3 = Taxon()
            self.taxon4 = Taxon()
	    return None

        # Parsing begins here
	if (initInput.find("confidence=") != -1):
	    elements = re.match("(.*) confidence=(.*)", initInput)
            initInput = elements.group(1)
            self.confidence = int(elements.group(2))
	if (initInput.find("sum") != -1 or initInput.find("diff") != -1):
	    if (initInput.find("lsum") != -1):
	        self.relations = relation["+="]
	        elements = re.match("(.*)\.(.*) (.*)\.(.*) lsum (.*)\.(.*)", initInput)
	    elif (initInput.find("rsum") != -1):
	        self.relations = relation["=+"]
	        elements = re.match("(.*)\.(.*) rsum (.*)\.(.*) (.*)\.(.*)", initInput)
	    elif (initInput.find("ldiff") != -1):
	        self.relations = 0 #[relationDict["-="]]
	        elements = re.match("(.*)\.(.*) (.*)\.(.*) ldiff (.*)\.(.*)", initInput)
	    elif (initInput.find("rdiff") != -1):
	        self.relations = 0 #[relationDict["=-"]]
	        elements = re.match("(.*)\.(.*) rdiff (.*)\.(.*) (.*)\.(.*)", initInput)
	    elif (initInput.find("e4sum") != -1):
	        self.relations = 0 #[relationDict["+=+"]]
	        elements = re.match("(.*)\.(.*) (.*)\.(.*) e4sum (.*)\.(.*) (.*)\.(.*)", initInput)
	    elif (initInput.find("i4sum") != -1):
	        self.relations = 0 #[relationDict["+<=+"]]
	        elements = re.match("(.*)\.(.*) (.*)\.(.*) i4sum (.*)\.(.*) (.*)\.(.*)", initInput)
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
            if(initInput.find("4sum") != -1):
                taxon4taxonomy = elements.group(7)
                taxon4taxon = elements.group(8)
                self.taxon4 = mapping.getTaxon(taxon4taxonomy, taxon4taxon)
	        self.numTaxon = 4
        else:
            ## initInput is of form b48.a equals k04.a
            self.relation = 0
            if (initInput.find("{") != -1):
                elements = re.match("(.*)\.(.*) {(.*)} (.*)\.(.*)", initInput)
            else:
                elements = re.match("(.*)\.(.*) (.*) (.*)\.(.*)", initInput)
            
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
 
    def toASP(self, enc, rnr):
        name1 = self.taxon1.dlvName()
        name2 = self.taxon2.dlvName()
        if encode[enc] & encode["vr"] or encode[enc] & encode["dl"] or encode[enc] & encode["mn"]:
	    if self.relations == rcc5["equals"]:
		result  = "ir(X, r" + self.ruleNum.__str__() + ") :- out(" + name1 + ",X), in(" + name2 + ",X).\n"
		result += "ir(X, r" + self.ruleNum.__str__() + ") :- in(" + name1 + ",X), out(" + name2 + ",X).\n" 
                if reasoner[rnr] == reasoner["dlv"]:
		    result += ":- #count{X: vrs(X), in(" + name1 + ",X), in(" + name2 + ",X)} = 0, pw.\n" 
                elif reasoner[rnr] == reasoner["gringo"]:
		    result += ":- [vrs(X): in(" + name1 + ",X): in(" + name2 + ",X)]0, pw.\n" 
	        result += "pie(r" + self.ruleNum.__str__() + ", A, 1) :- ir(X, A), in(" + name1 + ", X), in(" + name2 + ", X), ix.\n"
	        result += "c(r" + self.ruleNum.__str__() + ", A, 1) :- vr(X, A), in(" + name1 + ", X), in(" + name2 + ", X), ix.\n\n"
		#result += "in(" + name1 + ",X) :- in(" + name2 + ",X).\n" 
		#result += "in(" + name2 + ",X) :- in(" + name1 + ",X).\n" 
		#result += "out(" + name1 + ",X) :- out(" + name2 + ",X).\n" 
		#result += "out(" + name2 + ",X) :- out(" + name1 + ",X).\n" 
	    elif self.relations == rcc5["includes"]:
		result  = "ir(X, r" + self.ruleNum.__str__() + ") :- out(" + name1 + ",X), in(" + name2 + ",X).\n"
                if reasoner[rnr] == reasoner["dlv"]:
		    result += ":- #count{X: vrs(X), in(" + name1 + ",X), in(" + name2 + ",X)} = 0, pw.\n" 
		    result += ":- #count{X: vrs(X), in(" + name1 + ",X), out(" + name2 + ",X)} = 0, pw.\n" 
                elif reasoner[rnr] == reasoner["gringo"]:
		    result += ":- [vrs(X): in(" + name1 + ",X): in(" + name2 + ",X)]0, pw.\n" 
		    result += ":- [vrs(X): in(" + name1 + ",X): out(" + name2 + ",X)]0, pw.\n" 
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
		    result = ":- [vrs(X): in(" + name1 + ",X): in(" + name2 + ",X)]0, pw.\n" 
		    result += ":- [vrs(X): out(" + name1 + ",X): in(" + name2 + ",X)]0, pw.\n" 
		result += "ir(X, r" + self.ruleNum.__str__() + ") :- in(" + name1 + ",X), out(" + name2 + ",X).\n" 
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
		    result = ":- [vrs(X): in(" + name1 + ",X): out(" + name2 + ",X)]0, pw.\n" 
		    result += ":- [vrs(X): out(" + name1 + ",X): in(" + name2 + ",X)]0, pw.\n" 
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
		    result = ":- [vrs(X): in(" + name1 + ",X): in(" + name2 + ",X)]0, pw.\n" 
		    result += ":- [vrs(X): out(" + name1 + ",X): in(" + name2 + ",X)]0, pw.\n" 
		    result += ":- [vrs(X): in(" + name1 + ",X): out(" + name2 + ",X)]0, pw.\n" 
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
	    elif self.relations == (rcc5["equals"] | rcc5["is_included_in"]):
		result  = "ir(X, r" + self.ruleNum.__str__() + ") :- in(" + name1 + ",X), out(" + name2 + ",X).\n"
                if reasoner[rnr] == reasoner["dlv"]:
		    result += "vr(X, r" + self.ruleNum.__str__() + ") v ir(X, r" + self.ruleNum.__str__() + ") :- out(" + name1 + ",X), in(" + name2 + ",X).\n" 
		    result += ":- #count{X: vrs(X), in(" + name1 + ",X), in(" + name2 + ",X)} = 0, pw.\n" 
                elif reasoner[rnr] == reasoner["gringo"]:
		    result += "vr(X, r" + self.ruleNum.__str__() + ") | ir(X, r" + self.ruleNum.__str__() + ") :- out(" + name1 + ",X), in(" + name2 + ",X).\n" 
		    result += ":- [vrs(X): in(" + name1 + ",X): in(" + name2 + ",X)]0, pw.\n" 
	        result += "pie(r" + self.ruleNum.__str__() + ", A, 1) :- ir(X, A), in(" + name1 + ", X), in(" + name2 + ", X), ix.\n"
	        result += "c(r" + self.ruleNum.__str__() + ", A, 1) :- vr(X, A), in(" + name1 + ", X), in(" + name2 + ", X), ix.\n\n"
		#result += "in(" + name2 + ",X) :- in(" + name1 + ",X).\n" 
		#result += "out(" + name1 + ",X) :- out(" + name2 + ",X).\n" 
		#result += "in(" + name1 + ",X) v out(" + name1 + ",X) :- in(" + name2 + ",X).\n" 
		#result += "in(" + name2 + ",X) v out(" + name2 + ",X) :- out(" + name1 + ",X).\n" 
	    elif self.relations == (rcc5["equals"] | rcc5["includes"]):
		result  = "ir(X, r" + self.ruleNum.__str__() + ") :- out(" + name1 + ",X), in(" + name2 + ",X).\n"
                if reasoner[rnr] == reasoner["dlv"]:
		    result += "vr(X, r" + self.ruleNum.__str__() +") v ir(X, r" + self.ruleNum.__str__() + ") :- in(" + name1 + ",X), out(" + name2 + ",X).\n" 
		    result += ":- #count{X: vrs(X), in(" + name1 + ",X), in(" + name2 + ",X)} = 0, pw.\n" 
                elif reasoner[rnr] == reasoner["gringo"]:
		    result += "vr(X, r" + self.ruleNum.__str__() +") | ir(X, r" + self.ruleNum.__str__() + ") :- in(" + name1 + ",X), out(" + name2 + ",X).\n" 
		    result += ":- [vrs(X): in(" + name1 + ",X): in(" + name2 + ",X)]0, pw.\n" 
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
                elif reasoner[rnr] == reasoner["gringo"]:
		    result  = "ir(X, r" + self.ruleNum.__str__() + ") | vr(X, r" + self.ruleNum.__str__() +") :- in(" + name1 + ",X), in(" + name2 + ",X).\n"
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
		    result  = ":- 1[vrs(X): in(" + name1 + ",X): out(" + name2 + ",X)], [vr(Y, _): in(" + name2 + ",Y): out(" + name1 + ",Y)]0.\n"
		    result += ":- [vrs(X): in(" + name1 + ",X): out(" + name2 + ",X)]0, 1[vr(Y, _): in(" + name2 + ",Y): out(" + name1 + ",Y)].\n"
		    result += ":- [vrs(X): in(" + name1 + ",X): in(" + name2 + ",X)]0.\n"
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
		    result += "1[vrs(X): in(" + name1 + ",X): in(" + name2 + ",X)] :- pw.\n" 
		    result += "1[vrs(X): out(" + name1 + ",X): in(" + name2 + ",X)] :- pw.\n" 
		#result += "in(" + name2 + ",X) v out(" + name2 + ",X) :- in(" + name1 + ",X).\n" 
		#result += "in(" + name1 + ",X) v out(" + name1 + ",X) :- out(" + name2 + ",X).\n" 
		#result += "in(" + name2 + ",X) v out(" + name2 + ",X) :- out(" + name1 + ",X).\n" 
		#result += "in(" + name1 + ",X) v out(" + name1 + ",X) :- in(" + name2 + ",X).\n" 
	    elif self.relations == (rcc5["includes"] | rcc5["disjoint"]):
                if reasoner[rnr] == reasoner["dlv"]:
		    result  = ":- #count{X: vrs(X), in(" + name1 + ",X), out(" + name2 + ",X)} = 0, pw.\n"
		    result += ":- #count{X: vrs(X), in(" + name1 + ",X), in(" + name2 + ",X)} > 0, #count{Y: vrs(Y), in(" + name2 + ",Y), out(" + name1 + ",Y)} > 0, pw.\n"
		    result += ":- #count{X: vrs(X), in(" + name1 + ",X), in(" + name2 + ",X)} = 0, #count{Y: vrs(Y), in(" + name2 + ",Y), out(" + name1 + ",Y)} = 0, pw.\n"
                elif reasoner[rnr] == reasoner["gringo"]:
		    result  = ":- [vrs(X), in(" + name1 + ",X), out(" + name2 + ",X)]0, pw.\n"
		    result += ":- 1[vrs(X): in(" + name1 + ",X): in(" + name2 + ",X)], 1[vrs(X): out(" + name1 + ",X): in(" + name2 + ",X)], pw.\n" 
		    result += ":- [vrs(X): in(" + name1 + ",X): in(" + name2 + ",X)]0, [vrs(X): out(" + name1 + ",X): in(" + name2 + ",X)]0, pw.\n" 
            elif self.relations == relation["+="]:
                name3 = self.taxon3.dlvName()
                if reasoner[rnr] == reasoner["dlv"]:
		    result  = ":- #count{X: vrs(X), out(" + name1 + ",X), in(" + name3 + ",X)} = 0.\n" 
		    result += ":- #count{X: vrs(X), in(" + name1 + ",X), in(" + name3 + ",X)} = 0.\n" 
		    result += ":- #count{X: vrs(X), out(" + name2 + ",X), in(" + name3 + ",X)} = 0.\n" 
		    result += ":- #count{X: vrs(X), in(" + name2 + ",X), in(" + name3 + ",X)} = 0.\n" 
                elif reasoner[rnr] == reasoner["gringo"]:
		    result  = ":- [vrs(X): out(" + name1 + ",X): in(" + name3 + ",X)]0.\n" 
		    result += ":- [vrs(X): in(" + name1 + ",X): in(" + name3 + ",X)]0.\n" 
		    result += ":- [vrs(X): out(" + name2 + ",X): in(" + name3 + ",X)]0.\n" 
		    result += ":- [vrs(X): in(" + name2 + ",X): in(" + name3 + ",X)]0.\n" 
		result += "ir(X, r" + self.ruleNum.__str__() + ") :- in(" + name1 + ",X), out(" + name3 + ",X).\n" 
		result += "ir(X, r" + self.ruleNum.__str__() + ") :- in(" + name2 + ",X), out(" + name3 + ",X).\n" 
		#result += "in(" + name3 + ",X) :- in(" + name1 + ",X).\n" 
		#result += "in(" + name3 + ",X) :- in(" + name2 + ",X).\n" 
		#result += "out(" + name1 + ",X) :- out(" + name3 + ",X).\n" 
		#result += "out(" + name2 + ",X) :- out(" + name3 + ",X).\n" 
		#result += "in(" + name1 + ",X) v in(" + name2 + ",X) :- in(" + name3 + ",X).\n" 
		#result += "out(" +name3 + ",X) :- out(" + name1 + ",X), out(" + name2 + ",X).\n" 
            elif self.relations == relation["=+"]:
                name3 = self.taxon3.dlvName()
                if reasoner[rnr] == reasoner["dlv"]:
		    result  = ":- #count{X: vrs(X), out(" + name2 + ",X), in(" + name1 + ",X)} = 0.\n" 
		    result += ":- #count{X: vrs(X), in(" + name2 + ",X), in(" + name1 + ",X)} = 0.\n" 
		    result += ":- #count{X: vrs(X), out(" + name3 + ",X), in(" + name1 + ",X)} = 0.\n" 
		    result += ":- #count{X: vrs(X), in(" + name3 + ",X), in(" + name1 + ",X)} = 0.\n" 
                elif reasoner[rnr] == reasoner["gringo"]:
                    result  = ":- [vrs(X): out(" + name2 + ",X): in(" + name1 + ",X)]0.\n"            
                    result += ":- [vrs(X): in(" + name2 + ",X): in(" + name1 + ",X)]0.\n"            
                    result += ":- [vrs(X): out(" + name3 + ",X): in(" + name1 + ",X)]0.\n"            
                    result += ":- [vrs(X): in(" + name3 + ",X): in(" + name1 + ",X)]0.\n"
		result += "ir(X, r" + self.ruleNum.__str__() + ") :- in(" + name2 + ",X), out(" + name1 + ",X).\n" 
		result += "ir(X, r" + self.ruleNum.__str__() + ") :- in(" + name3 + ",X), out(" + name1 + ",X).\n" 
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

