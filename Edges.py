# coding=utf-8

import pickle
import re

class Edges:
    """
    This class will generate all the text in the correct xml format to initialize
    all the edges that will be used by the petri net
    """
    
    def __init__(self, potentialDefinition, mandatoryDefinition):
        self.iterator = iter(range(22000,23000))
        with open("places.c", 'r') as f:
            self.placesDictionnary = pickle.load(f)
        with open("transitions.c", 'r') as f:
            self.transitionsDictionnary = pickle.load(f)
        self.potentialDefinition = potentialDefinition
        self.mandatoryDefinition = mandatoryDefinition
        print(self.transitionsDictionnary)
        print(self.placesDictionnary)
        
    def bothSides(self):
        dictionnary = dict()
        splittedPotential = self.potentialDefinition.split("\n")
        rePattern = re.compile("[a-zA-Z0-9]+,[0-9]+")
        for i in range(len(splittedPotential)):
            potentialActivityDictionnary = dict()
            activatorsAndInhibitors = splittedPotential[i].split("-")[0]
            products = splittedPotential[i].split("->")[1]
            activators = activatorsAndInhibitors.split(";")[0]
            inhibitors = activatorsAndInhibitors.split(";")[1]
            for j in re.findall(rePattern, activators):
                name = j.split(",")[0].rstrip().lstrip()
                potentialActivityDictionnary.setdefault(name, products.count(name) > 0)
            for j in re.findall(rePattern, inhibitors):
                name = j.split(",")[0].rstrip().lstrip()
                potentialActivityDictionnary.setdefault(name, products.count(name) > 0)
            dictionnary.setdefault("alpha" + (str(i)), potentialActivityDictionnary)
        splittedMandatory = self.mandatoryDefinition.split("\n")
        for i in range(len(splittedMandatory)):
            mandatoryActivityDictionnary = dict()
            activatorsAndInhibitors = splittedMandatory[i].split("-")[0]
            products = splittedMandatory[i].split("->")[1]
            activators = activatorsAndInhibitors.split(";")[0]
            inhibitors = activatorsAndInhibitors.split(";")[1]
            for j in re.findall(rePattern, activators):
                name = j.split(",")[0].rstrip().lstrip()
                mandatoryActivityDictionnary.setdefault(name, products.count(name) > 0)
            for j in re.findall(rePattern, inhibitors):
                name = j.split(",")[0].rstrip().lstrip()
                mandatoryActivityDictionnary.setdefault(name, products.count(name) > 0)
            dictionnary.setdefault("beta" + str(i), mandatoryActivityDictionnary)
        return dictionnary
    
    def countReadEdges(self, dictionnary):
        accumulator = 0
        for i in dictionnary.keys():
            for j in dictionnary[i].keys():
                if (not(dictionnary[i][j])):
                    accumulator += 1
        return accumulator
    
    def creatingEntityCompound(self, entityName):
        """
        Returns the color compound that defines an entity
        """
        return "(level" + entityName + ",timer" + entityName + ",lbd" + entityName + ")"
    
    def makeEdge(self, source, target, expression, name):
        identifier = self.iterator.next()
        accumulator = ""
        accumulator += "<edge source=\""+ str(source) + "\" target=\"" + str(target) + "\" id=\"" + str(self.iterator.next()) + "\" net=\"1\">\n"
        accumulator += "<attribute name=\"Comment\" id=\"" + str(self.iterator.next()) + "\" net=\"1\">\n"
        accumulator += "<![CDATA[]]>\n<graphics count=\"1\">\n"
        accumulator += "<graphic xoff=\"40.00\" x=\"260.00\" y=\"200.00\" id=\"" + str(self.iterator.next()) + "\" net=\"1\" "
        accumulator += "show=\"1\" grparent=\"" + str(identifier) + "\" state=\"1\" pen=\"0,0,0\" brush=\"255,255,255\"/>\n"
        accumulator += "</graphics>\n</attribute>\n<attribute name=\"Multiplicity\" id=\"" + str(self.iterator.next()) + "\" net=\"1\">\n"
        accumulator += "<![CDATA[1]]>\n<graphics count=\"1\">\n"
        accumulator += "<graphic xoff=\"20.00\" x=\"230.00\" y=\"200.00\" id=\"" + str(self.iterator.next()) + "\" net=\"1\" "
        accumulator += "show=\"0\" grparent=\"" + str(identifier) + "\" state=\"1\" pen=\"0,0,0\" brush=\"255,255,255\"/>\n"
        accumulator += "</graphics>\n</attribute>\n<attribute name=\"ExpressionList\" type=\"ColList\" id=\"" + str(self.iterator.next()) + "\" net=\"1\">\n"
        accumulator += "<colList row_count=\"1\" col_count=\"2\" active_row=\"0\" active_col=\"0\">\n<colList_head>\n"
        accumulator += "<colList_colLabel>\n<![CDATA[Expression set]]>\n</colList_colLabel>\n<colList_colLabel>\n"
        accumulator += "<![CDATA[Expression]]>\n</colList_colLabel>\n</colList_head>\n<colList_body>\n<colList_row nr=\"0\">\n"
        accumulator += "<colList_col nr=\"0\">\n<![CDATA[Main]]>\n</colList_col>\n<colList_col nr=\"1\">\n"
        accumulator += "<![CDATA[" + expression + "]]>\n"
        accumulator += "</colList_col>\n</colList_row>\n</colList_body>\n</colList>\n<graphics count=\"1\">\n"
        accumulator += "<graphic xoff=\"25.00\" x=\"245.00\" y=\"200.00\" id=\"" + str(self.iterator.next()) + "\" net=\"1\" "
        accumulator += "show=\"1\" grparent=\"" + str(identifier) + "\" state=\"1\" pen=\"0,0,0\" brush=\"255,255,255\"/>\n"
        accumulator += "</graphics>\n</attribute>\n<graphics count=\"1\">\n"
        accumulator += "<graphic id=\"" + str(identifier) + "\" net=\"1\" source=\""+ str(source-1) + "\" target=\"" + str(target-1) + "\" state=\"1\" "
        accumulator += "show=\"1\" pen=\"0,0,0\" brush=\"0,0,0\" edge_designtype=\"3\">\n"
        accumulator += "<points count=\"2\">\n<point x=\"190.00\" y=\"200.00\"/>\n<point x=\"250.00\" y=\"200.00\"/>\n"
        accumulator += "</points>\n</graphic>\n</graphics>\n</edge>\n"
        return accumulator
    
    def makeReadEdge(self, source, target, expression, name):
        identifier = self.iterator.next()
        accumulator = ""
        accumulator += "<edge source=\""+ str(source) + "\" target=\"" + str(target) + "\" id=\"" + str(self.iterator.next()) + "\" net=\"1\">\n"
        accumulator += "<attribute name=\"Multiplicity\" id=\"" + str(self.iterator.next()) + "\" net=\"1\">\n"
        accumulator += "<![CDATA[1]]>\n<graphics count=\"1\">\n"
        accumulator += "<graphic xoff=\"20.00\" x=\"230.00\" y=\"200.00\" id=\"" + str(self.iterator.next()) + "\" net=\"1\" "
        accumulator += "show=\"0\" grparent=\"" + str(identifier) + "\" state=\"1\" pen=\"0,0,0\" brush=\"255,255,255\"/>\n</graphics>\n</attribute>\n"
        accumulator += "<attribute name=\"Comment\" id=\"" + str(self.iterator.next()) + "\" net=\"1\">\n"
        accumulator += "<![CDATA[]]>\n<graphics count=\"1\">\n"
        accumulator += "<graphic xoff=\"40.00\" x=\"250.00\" y=\"200.00\" id=\"" + str(self.iterator.next()) + "\" net=\"1\" "
        accumulator += "show=\"1\" grparent=\"" + str(identifier) + "\" state=\"1\" pen=\"0,0,0\" brush=\"255,255,255\"/>\n</graphics>\n"
        accumulator += "</attribute>\n<attribute name=\"ExpressionList\" type=\"ColList\" id=\"" + str(self.iterator.next()) + "\" net=\"1\">\n"
        accumulator += "<colList row_count=\"1\" col_count=\"2\" active_row=\"0\" active_col=\"0\">\n<colList_head>\n"
        accumulator += "<colList_colLabel>\n<![CDATA[Inscription set]]>\n</colList_colLabel>\n<colList_colLabel>\n"
        accumulator += "<![CDATA[Inscription]]>\n</colList_colLabel>\n</colList_head>\n<colList_body>\n<colList_row nr=\"0\">\n"
        accumulator += "<colList_col nr=\"0\">\n<![CDATA[Main]]>\n</colList_col>\n<colList_col nr=\"1\">\n"
        accumulator += "<![CDATA[" + expression + "]]>\n"
        accumulator += "</colList_col>\n</colList_row>\n</colList_body>\n</colList>\n<graphics count=\"1\">\n"
        accumulator += "<graphic xoff=\"25.00\" x=\"235.00\" y=\"200.00\" id=\"" + str(self.iterator.next()) + "\" net=\"1\" "
        accumulator += "show=\"1\" grparent=\"" + str(identifier) + "\" state=\"1\" pen=\"0,0,0\" brush=\"255,255,255\"/>\n"
        accumulator += "</graphics>\n</attribute>\n<graphics count=\"1\">\n"
        accumulator += "<graphic id=\"" + str(identifier) + "\" net=\"1\" source=\""+ str(source-1) + "\" target=\"" + str(target-1) + "\" state=\"1\" "
        accumulator += "show=\"1\" pen=\"0,0,0\" brush=\"0,0,0\" edge_designtype=\"2\">\n"
        accumulator += "<points count=\"2\">\n<point x=\"190.00\" y=\"200.00\"/>\n<point x=\"250.00\" y=\"200.00\"/>\n"
        accumulator += "</points>\n</graphic>\n</graphics>\n</edge>\n"
        return accumulator
        
    def makeText(self):
        dictionnary = self.bothSides()
        print(dictionnary)
        startEdges = "<nodeclass count=\"0\" name=\"Coarse Place\"/>\n<nodeclass count=\"0\" name=\"Coarse Transition\"/>\n</nodeclasses>\n<edgeclasses count=\"5\">\n<edgeclass count=\"" + str(0) + "\" name=\"Edge\">\n"
        endEdge = "</edgeclass>\n"
        startReadEdge = "<edgeclass count=\"" + str(self.countReadEdges(dictionnary)) + "\" name=\"Read Edge\">\n"
        endReadEdge = "</edgeclass>\n"
        edgeAccumulator = ""
        readEdgeAccumulator = ""
        for i in dictionnary.keys():
            for j in dictionnary[i].keys():
                if (not(dictionnary[i][j])):
                    readEdgeAccumulator += self.makeReadEdge(self.placesDictionnary[j], self.transitionsDictionnary["t" + (i if (i.count("beta") == 0) else "beta")], self.creatingEntityCompound(j), "")
        return startEdges + edgeAccumulator + endEdge + startReadEdge + readEdgeAccumulator + endReadEdge