# coding=utf-8

import pickle
import re

class Edges:
    """
    This class will generate all the text in the correct xml format to initialize
    all the edges that will be used by the petri net
    """
    
    def __init__(self, entityDefinition, potentialDefinition, mandatoryDefinition):
        self.iterator = iter(range(40000,50000))
        with open("places.c", 'r') as f:
            self.placesDictionnary = pickle.load(f)
        with open("transitions.c", 'r') as f:
            self.transitionsDictionnary = pickle.load(f)
        self.entityDefinition = entityDefinition
        self.potentialDefinition = potentialDefinition
        self.mandatoryDefinition = mandatoryDefinition
        
    def bothSides(self):
        """
        Returns a dictionnary containing for all the potential definition if an entity is both 
        either an activitor or an inhibitor and a product
        """
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
                potentialActivityDictionnary.setdefault(name, products.count("(" + name + ",") > 0)
            for j in re.findall(rePattern, inhibitors):
                name = j.split(",")[0].rstrip().lstrip()
                potentialActivityDictionnary.setdefault(name, products.count("(" + name + ",") > 0)
            dictionnary.setdefault("alpha" + (str(i)), potentialActivityDictionnary)
        return dictionnary
    
    def countReadEdges(self, dictionnary):
        """
        Returns the number of read edges in the graph by using the dictionnary from the bothSides function
        """
        accumulator = 0
        for i in dictionnary.keys():
            for j in dictionnary[i].keys():
                if (not(dictionnary[i][j])):
                    accumulator += 1
        return accumulator
    
    def countEdges(self):
        """
        Returns the number of edges contained in the petri net
        """
        return 4 * len(self.potentialDefinition.split("\n")) + 2 * len(self.mandatoryDefinition.split("\n")) + 2 * len(self.entityDefinition.split("\n"))
    
    def creatingEntityCompound(self, entityName):
        """
        Returns the color compound that defines an entity
        """
        return "(level" + entityName + ",timer" + entityName + ",lbd" + entityName + ")"
    
    def makeEdge(self, source, target, expression, name):
        """
        Returns a text in the xml format to initialize an edge from source to target with the expression
        """
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
        """
        Returns a text in the xml format to initialize a read edge from source to target with the expression
        """
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
        """
        Returns the text generated in the xml format for all the definitions of the edges
        """
        dictionnary = self.bothSides()
        startEdges = "<nodeclass count=\"0\" name=\"Coarse Place\"/>\n<nodeclass count=\"0\" name=\"Coarse Transition\"/>\n</nodeclasses>\n<edgeclasses count=\"5\">\n<edgeclass count=\"" + str(self.countEdges()) + "\" name=\"Edge\">\n"
        endEdge = "</edgeclass>\n"
        startReadEdge = "<edgeclass count=\"" + str(self.countReadEdges(dictionnary)) + "\" name=\"Read Edge\">\n"
        endReadEdge = "</edgeclass>\n"
        edgeAccumulator = ""
        readEdgeAccumulator = ""
        
        # A loop to create all the read edges from the dictionnary of the function bothSides
        for i in dictionnary.keys():
            for j in dictionnary[i].keys():
                if (not(dictionnary[i][j])):
                    readEdgeAccumulator += self.makeReadEdge(self.placesDictionnary[j], self.transitionsDictionnary["t" + i], self.creatingEntityCompound(j), "")
        
        # A loop to create all the edges going to and from the potential activities places to their transitions
        # but also to and from the potential activities places to the mandatory transition
        loop = 0
        while (loop >= 0):
            try:
                placeID = self.placesDictionnary["palpha" + str(loop)]
                transitionID = self.transitionsDictionnary["talpha" + str(loop)]
                betaTransitionID = self.transitionsDictionnary["tbeta"]
                edgeAccumulator += self.makeEdge(placeID, transitionID, "ptalpha" + str(loop), "")
                edgeAccumulator += self.makeEdge(transitionID, placeID, "0", "")
                edgeAccumulator += self.makeEdge(placeID, betaTransitionID, "ptalpha" + str(loop), "")
                edgeAccumulator += self.makeEdge(betaTransitionID, placeID, "ptalpha" + str(loop) + " + 1", "")
                loop += 1
            except KeyError:
                loop = -1
        
        # A loop to create all the edges going to and from the mandatory activities places to the mandatory activity transition
        loop = 0
        while (loop >= 0):
            try:
                placeID = self.placesDictionnary["pbeta" + str(loop)]
                transitionID = self.transitionsDictionnary["tbeta"]
                edgeAccumulator += self.makeEdge(placeID, transitionID, "ptbeta" + str(loop), "")
                edgeAccumulator += self.makeEdge(transitionID, placeID, "ptbeta" + str(loop), "")
                loop += 1
            except KeyError:
                loop = -1
        
        # A loop to create all the edges going to and from the entities places to the mandatory transition
        for i in (self.entityDefinition.split("\n")):
            name = i.split(":")[0].rstrip().lstrip()
            placeID = self.placesDictionnary[name]
            transitionID = self.transitionsDictionnary["tbeta"]
            edgeAccumulator += self.makeEdge(placeID, transitionID, self.creatingEntityCompound(name), "")
            edgeAccumulator += self.makeEdge(transitionID, placeID, self.creatingEntityCompound(name), "")
        
        # A loop to create all the edges going to and from the entities places to their transition (using the potential definition)
        rePattern = re.compile("[a-zA-Z0-9]+,[+\-][0-9]+")
        splittedPotential = self.potentialDefinition.split("\n")
        for i in range(len(splittedPotential)):
            products = splittedPotential[i].split("->")[1]
            for j in re.findall(rePattern, products):
                name = j.split(",")[0]
                placeID = self.placesDictionnary[name]
                transitionID = self.transitionsDictionnary["talpha" + str(i)]
                edgeAccumulator += self.makeEdge(placeID, transitionID, self.creatingEntityCompound(name), "")
                edgeAccumulator += self.makeEdge(transitionID, placeID, self.creatingEntityCompound(name), "")
        
        return startEdges + edgeAccumulator + endEdge + startReadEdge + readEdgeAccumulator + endReadEdge