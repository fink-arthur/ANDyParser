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
            self.placesDictionary = pickle.load(f)
        with open("transitions.c", 'r') as f:
            self.transitionsDictionary = pickle.load(f)
        self.entityDefinition = entityDefinition
        self.potentialDefinition = potentialDefinition
        self.mandatoryDefinition = mandatoryDefinition
        self.D = self.figuringDOut()
        self.mandatoryProducts = self.mandatoryProduct()
        
    def bothSides(self):
        """
        Returns a dictionary containing for all the potential definition if an entity is both 
        either an activitor or an inhibitor and a product
        """
        dictionary = dict()
        splittedPotential = self.potentialDefinition.split("\n")
        rePattern = re.compile("[a-zA-Z0-9]+,[0-9]+")
        if not((len(splittedPotential) == 1) & (splittedPotential[0].rstrip().lstrip() == "")):
            for i in range(len(splittedPotential)):
                # A loop to go through each potential activity
                potentialActivitydictionary = dict()
                activatorsAndInhibitors = splittedPotential[i].split("-")[0]
                products = splittedPotential[i].split("->")[1]
                activators = activatorsAndInhibitors.split(";")[0]
                inhibitors = activatorsAndInhibitors.split(";")[1]
                for j in re.findall(rePattern, activators):
                    # A loop to go through each activator
                    name = j.split(",")[0].rstrip().lstrip()
                    potentialActivitydictionary.setdefault(name, products.count("(" + name + ",") > 0)
                for j in re.findall(rePattern, inhibitors):
                    # A loop to go through each inhibitor
                    name = j.split(",")[0].rstrip().lstrip()
                    potentialActivitydictionary.setdefault(name, products.count("(" + name + ",") > 0)
                dictionary.setdefault("alpha" + (str(i)), potentialActivitydictionary)
        return dictionary
    
    def mandatoryProduct(self):
        dictionary = dict()
        splittedMandatory = self.mandatoryDefinition.split("\n")
        rePattern = re.compile("[a-zA-Z0-9]+,[+\-][0-9]+")
        if not((len(splittedMandatory) == 1) & (splittedMandatory[0].rstrip().lstrip() == "")):
            for i in range(len(splittedMandatory)):
                for j in re.findall(rePattern, splittedMandatory[i]):
                    name = j.split(",")[0]
                    try:
                        dictionary.setdefault(name,dictionary[name].append(str(i)))
                    except KeyError:
                        dictionary.setdefault(name,list(str(i)))
        return dictionary
    
    def countReadEdges(self, dictionary):
        """
        Returns the number of read edges in the graph by using the dictionary from the bothSides function
        """
        accumulator = 0
        for i in dictionary.keys():
            for j in dictionary[i].keys():
                if (not(dictionary[i][j])):
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
    
    def numberOfLevel(self, entityName):
        """
        Returns the number of levels of an entity named entityName
        """
        splittedDefinition = self.entityDefinition.split("\n")
        for i in splittedDefinition:
            if (entityName in i):
                return i.count(",") + 1
            
    def figuringdOut(self, line):
        """
        Returns d for an entity where d is the highest decay duration for a level
        """
        levels = line.split(":")[1].lstrip().rstrip()[1:-1].split(",")
        accumulator = int(levels[0].lstrip().rstrip())
        for i in range(1, len(levels)):
            if (accumulator < int(levels[i])):
                accumulator = int(levels[i].lstrip().rstrip())
        return accumulator
    
    def figuringDOut(self):
        """
        Returns D for all the activities where D is the highest duration for an activity
        """
        splittedPotential = self.potentialDefinition.split("\n")
        maximumPotential = 0
        if not((len(splittedPotential) == 1) & (splittedPotential[0].rstrip().lstrip() == "")):
            for i in splittedPotential:
                duration = int(i.split("-")[1])
                if (duration > maximumPotential):
                    maximumPotential = duration
        splittedMandatory = self.mandatoryDefinition.split("\n")
        maximumMandatory = 0
        if not((len(splittedMandatory) == 1) & (splittedMandatory[0].rstrip().lstrip() == "")):
            for i in splittedMandatory:
                duration = int(i.split("-")[1])
                if (duration > maximumPotential):
                    maximumMandatory = duration
        if (maximumMandatory > maximumPotential):
            return maximumMandatory
        else:
            return maximumPotential
    
    def makingMin(self, a, b):
        """
        Returns the mininum between a and b without using a predicate
        """
        return "(" + a + "+" + b + ")/2-abs(" + a + "-(" + b + "))/2"
        #return "( " + a + " + " + b + " ) / 2 - abs( " + a + " - (" + b + ") ) / 2"
        #return "abs(" + b +")"
    
    def makingMaxLambda(self, entityName, zero):
        """
        Returns a lambda where each part is a maxed with the D value
        """
        numberOfLevel = self.numberOfLevel(entityName)
        lambdaAccumulator = "(" + self.makingMin("(lbd" + entityName + ":1)+1", str(self.D))
        for i in range(1,numberOfLevel):
            if zero == i:
                lambdaAccumulator += ",0"
            else:
                lambdaAccumulator += "," + self.makingMin("(lbd" + entityName + ":" + str(i + 1) +")+1", str(self.D))
        lambdaAccumulator += ")"
        return lambdaAccumulator
    
    def makingLambda(self, entityName, entityLevel, levelUpdate, maximum):
        """
        Returns a lambda with the value at 0 after an update at level entityLevel
        """
        accumulator = ""
        lu = int(levelUpdate)
        if lu < 0:
            entityLevel += lu
            lu = abs(lu)
        numberOfLevel = self.numberOfLevel(entityName)
        if not(maximum):
            accumulator += "(lbd" + entityName + ":1"
        else: 
            accumulator += "(" + self.makingMin("(lbd" + entityName + ":1)+1", str(self.D))
        for i in range(1, numberOfLevel):
            if ((entityLevel != 0) & (lu != 0)):
                if not(maximum):
                    accumulator += "," + "lbd" + entityName + ":" + str(i+1)
                else: 
                    accumulator += "," + self.makingMin("(lbd" + entityName + ":" + str(i + 1) +")+1", str(self.D))
                entityLevel -= 1
            #elif ((entityLevel == 0) & (lu == 0)):
            elif lu == 0:
                if not(maximum):
                    accumulator += "," + "lbd" + entityName + ":" + str(i+1)
                else: 
                    accumulator += "," + self.makingMin("(lbd" + entityName + ":" + str(i + 1) +")+1", str(self.D))
            else:
                accumulator += ",0"
                lu -= 1
            
        accumulator += ")"
        return accumulator
    
    def makingList(self,n):
        l = [""]
        while (n>0):
            res1 = ["1" + x for x in l]
            res2 = ["0" + x for x in l]
            res1.extend(res2)
            l = res1
            n -= 1
        return l
    
    def activatorStringToGuard(self, string, delta, opposite):
        """
        Returns a string that is a guard for the activator in string
        """
        name = string.split(",")[0]
        level = string.split(",")[1]
        accumulator = ""
        if not(opposite):
            accumulator += "level" + name + " >= " + level + " & "
            accumulator += "lbd" + name + ":" + str(int(level) + 1) + " >= " + delta
        else:
            accumulator += "(level" + name + " < " + level + " | "
            accumulator += "lbd" + name + ":" + str(int(level) + 1) + " < " + delta + ")"
        return accumulator
    
    def inhibitorStringToGuard(self, string, delta, opposite):
        """
        Returns a string that is a guard for the inhibitor in string
        """
        name = string.split(",")[0]
        level = string.split(",")[1]
        accumulator = ""
        if not(opposite):
            accumulator += "level" + name + " < " + level + " & "
            accumulator += "lbd" + name + ":" + str(int(level) + 1) + " >= " + delta
        else:
            accumulator += "(level" + name + " >= " + level + " | "
            accumulator += "lbd" + name + ":" + str(int(level) + 1) + " < " + delta + ")"
        return accumulator
    
    def stringToCondition(self, string, opposite):
        """
        Returns the guard that will be used by the transitions for the activity contained in the string
        """
        activatorsAndInhibitors = string.split("-")[0]
        delta = string.split("-")[1]
        activators = activatorsAndInhibitors.split(";")[0]
        inhibitors = activatorsAndInhibitors.split(";")[1]
        rePattern = re.compile("[a-zA-Z0-9]+,[0-9]+")
        accumulator = ""
        for i in re.findall(rePattern, activators):
            # A loop to create the conditions for an activator
            accumulator += self.activatorStringToGuard(i, delta, opposite) + "&"
        for i in re.findall(rePattern, inhibitors):
            # A loop to create the conditions for an inhibitor
            accumulator += self.inhibitorStringToGuard(i, delta, opposite) + "&"
        return accumulator[:-1]
    
    def creatingExpression(self, name, mandatory, level, decayTimer):
        splittedMandatory = self.mandatoryDefinition.split("\n")
        conditions = ["timer" + name + ">=" + decayTimer]
        conditions.extend([self.stringToCondition(splittedMandatory[int(x)], False) for x in mandatory])
        notConditions = ["timer" + name + "<" + decayTimer]
        notConditions.extend([self.stringToCondition(splittedMandatory[int(x)], True) for x in mandatory])
        possibilityList = self.makingList(len(mandatory) + 1)
        accumulator = ""
        for i in range(len(possibilityList)):
            
            condition = ""
            for j in range(len(possibilityList[i])):
                if (possibilityList[i][j] == "0"):
                    condition += notConditions[j] + " & "
                else:
                    condition += conditions[j] + " & "
                
            update = 0
            for j in range(1, len(possibilityList[i])):
                if possibilityList[i][j] == "1":
                    rePattern = re.compile(name + ",[+-][0-9]+")
                    for res in re.findall(rePattern, splittedMandatory[int(mandatory[j - 1])]):
                        update += int(res.split(",")[1])
            if possibilityList[i][0] == "1":
                update -= 1
            
            
            if possibilityList[i].count("0") == len(possibilityList[i]):
                if (decayTimer == 0):
                    accumulator += "[" + condition + "level" + name + "=" + level + "](level" + name + ",0," + self.makingLambda(name, 0, 0, True) + ")"
                else:
                    accumulator += "[" + condition + "level" + name + "=" + level + "](level" + name + ",timer" + name + "+1," + self.makingLambda(name, 0, 0, True) + ")"
            else:
                if update >= 0:
                    update = "+" + str(update)
                else:
                    update = str(update)
                accumulator += "[" + condition + "level" + name + "=" + level + "& level" + name + update + ">=0](level" + name + update + ",0," + self.makingLambda(name, int(level), int(update), True)+")"
                accumulator += "++[" + condition + "level" + name + "=" + level + "& level" + name + update + "<0](0,0," + self.makingLambda(name, int(level), int(update), True)+")"
            
            #if(i < len(possibilityList[i])):
            accumulator += "++"
        
        return accumulator
    
    def creatingEntityBetaCompound(self, entityName):
        """
        Returns an entity compound using the formula for the decay of the entity entityName
        """
        accumulator = ""
        splittedDefinition = self.entityDefinition.split("\n")
        for i in splittedDefinition:
            if (entityName in i):
                entityDefinition = i
        splittedDefinition = entityDefinition.split(":")
        splittedLevel = splittedDefinition[1].rstrip().lstrip()[1:-1].split(",")
        #accumulator += "[level" + entityName + "=0](0,0," + self.makingMaxLambda(entityName, None) + ")"
        for i in range(len(splittedLevel)):
            #accumulator += "++[level" + entityName + "=" + str(i) + " & timer" + entityName + ">=" + str(splittedLevel[i]) + "]" + "(level" + entityName + "-1,0," + self.makingMaxLambda(entityName, i) + ")"
            #accumulator += "++[level" + entityName + "=" + str(i) + " & timer" + entityName + "<" + str(splittedLevel[i]) + "]" + "(level" + entityName + "," + "timer" + entityName + "+1," + self.makingMaxLambda(entityName, None) + ")"
            try:
                mandatory = self.mandatoryProducts[entityName]
            except KeyError:
                mandatory = []
            accumulator += self.creatingExpression(entityName, mandatory, str(i), splittedLevel[i])
        
        return accumulator[:-2]
    
    def creatingEntityProductCompound(self, entityName, levelUpdate):
        """
        Returns an entity compound using the formula for an update of the entity entityName
        """
        numberOfLevel = self.numberOfLevel(entityName)
        accumulator = "[level" + entityName + "=0 & 0" + levelUpdate + "<0](0,0," + self.makingLambda(entityName, 0, levelUpdate, False) + ")"
        accumulator += "++[level" + entityName + "=0 & 0" + levelUpdate + ">=0](" + self.makingMin("level" + entityName + levelUpdate, str(numberOfLevel - 1)) + ",0," + self.makingLambda(entityName, 0, levelUpdate, False) + ")"
        for i in range(1,numberOfLevel):
            accumulator += "++[level" + entityName + "=" + str(i) + " & " + str(i) + levelUpdate + "<0](0,0," + self.makingLambda(entityName, i, levelUpdate, False) + ")"
            accumulator += "++[level" + entityName + "=" + str(i) + " & " + str(i) + levelUpdate + ">=0](" + self.makingMin("level" + entityName + levelUpdate, str(numberOfLevel - 1)) + ",0," + self.makingLambda(entityName, i, levelUpdate, False) + ")"
        return accumulator
    
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
        accumulator += "show=\"0\" grparent=\"" + str(identifier) + "\" state=\"1\" pen=\"0,0,0\" brush=\"255,255,255\"/>\n"
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
        accumulator += "show=\"0\" grparent=\"" + str(identifier) + "\" state=\"1\" pen=\"0,0,0\" brush=\"255,255,255\"/>\n"
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
        dictionary = self.bothSides()
        startEdges = "<nodeclass count=\"0\" name=\"Coarse Place\"/>\n<nodeclass count=\"0\" name=\"Coarse Transition\"/>\n</nodeclasses>\n<edgeclasses count=\"5\">\n<edgeclass count=\"" + str(self.countEdges()) + "\" name=\"Edge\">\n"
        endEdge = "</edgeclass>\n"
        startReadEdge = "<edgeclass count=\"" + str(self.countReadEdges(dictionary)) + "\" name=\"Read Edge\">\n"
        endReadEdge = "</edgeclass>\n"
        edgeAccumulator = ""
        readEdgeAccumulator = ""
        
        # A loop to create all the read edges from the dictionary of the function bothSides
        for i in dictionary.keys():
            for j in dictionary[i].keys():
                if (not(dictionary[i][j])):
                    readEdgeAccumulator += self.makeReadEdge(self.placesDictionary[j], self.transitionsDictionary["t" + i], self.creatingEntityCompound(j), "")
        
        # A loop to create all the edges going to and from the potential activities places to their transitions
        # but also to and from the potential activities places to the mandatory transition
        loop = 0
        while (loop >= 0):
            try:
                placeID = self.placesDictionary["palpha" + str(loop)]
                transitionID = self.transitionsDictionary["talpha" + str(loop)]
                betaTransitionID = self.transitionsDictionary["tbeta"]
                edgeAccumulator += self.makeEdge(placeID, transitionID, "ptalpha" + str(loop), "")
                edgeAccumulator += self.makeEdge(transitionID, placeID, "0", "")
                edgeAccumulator += self.makeEdge(placeID, betaTransitionID, "ptalpha" + str(loop), "")
                edgeAccumulator += self.makeEdge(betaTransitionID, placeID, "maxD(ptalpha" + str(loop) + " + 1)", "")
                loop += 1
            except KeyError:
                loop = -1
        
        # A loop to create all the edges going to and from the mandatory activities places to the mandatory activity transition
        loop = 0
        while (loop >= 0):
            try:
                placeID = self.placesDictionary["pbeta" + str(loop)]
                transitionID = self.transitionsDictionary["tbeta"]
                edgeAccumulator += self.makeEdge(placeID, transitionID, "ptbeta" + str(loop), "")
                edgeAccumulator += self.makeEdge(transitionID, placeID, "maxD(ptbeta" + str(loop) + " + 1)", "")
                loop += 1
            except KeyError:
                loop = -1
        
        # A loop to create all the edges going to and from the entities places to the mandatory transition
        for i in (self.entityDefinition.split("\n")):
            name = i.split(":")[0].rstrip().lstrip()
            placeID = self.placesDictionary[name]
            transitionID = self.transitionsDictionary["tbeta"]
            edgeAccumulator += self.makeEdge(placeID, transitionID, self.creatingEntityCompound(name), "")
            edgeAccumulator += self.makeEdge(transitionID, placeID, self.creatingEntityBetaCompound(name), "")
        
        # A loop to create all the edges going to and from the entities places to their transition (using the potential definition)
        rePattern = re.compile("[a-zA-Z0-9]+,[+\-][0-9]+")
        splittedPotential = self.potentialDefinition.split("\n")
        if not((len(splittedPotential) == 1) & (splittedPotential[0].rstrip().lstrip() == "")):
            for i in range(len(splittedPotential)):
                products = splittedPotential[i].split("->")[1]
                for j in re.findall(rePattern, products):
                    name = j.split(",")[0]
                    placeID = self.placesDictionary[name]
                    transitionID = self.transitionsDictionary["talpha" + str(i)]
                    edgeAccumulator += self.makeEdge(placeID, transitionID, self.creatingEntityCompound(name), "")
                    edgeAccumulator += self.makeEdge(transitionID, placeID, self.creatingEntityProductCompound(name, j.split(",")[1]), "")
        
        self.mandatoryProduct()
        
        return startEdges + edgeAccumulator + endEdge + startReadEdge + readEdgeAccumulator + endReadEdge
