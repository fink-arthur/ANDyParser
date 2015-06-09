# coding=utf-8

import re
import pickle

class Transitions:
    """
    This class will generate all the text in the correct xml format to initialize
    all the transitions that will be used by the petri net
    """
    
    def __init__(self, potentialDefinition):
        self.potentialDefinition = potentialDefinition
        # an iterator so that all the id used in a places are controlled and not repeated
        self.iterator = iter(range(21000,22000))
        # numberOfTransitions = numberOfPotential + 1 (only one transition for the mandatory activities)
        self.numberOfTransitions = (self.potentialDefinition.rstrip().lstrip().count("\n") + 1) + 1
        self.iteratorNumberOfTransitions = iter(range(self.numberOfTransitions))
        self.transitionsDictionnary = dict()
        
    def activatorStringToGuard(self, string, delta):
        """
        Returns a string that is a guard for the activator in string
        """
        name = string.split(",")[0]
        level = string.split(",")[1]
        accumulator = ""
        accumulator += "level" + name + " >= " + level + " & "
        accumulator += "lbd" + name + ":" + str(int(level) + 1) + " >= " + delta + " & "
        return accumulator
    
    def inhibitorStringToGuard(self, string, delta):
        """
        Returns a string that is a guard for the inhibitor in string
        """
        name = string.split(",")[0]
        level = string.split(",")[1]
        accumulator = ""
        accumulator += "level" + name + " < " + level + " & "
        accumulator += "lbd" + name + ":" + str(int(level) + 1) + " >= " + delta + " & "
        return accumulator
    
    def stringToGuard(self, string, definitionNumber):
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
            accumulator += self.activatorStringToGuard(i, delta)
        for i in re.findall(rePattern, inhibitors):
            accumulator += self.inhibitorStringToGuard(i, delta)
        return accumulator + "ptalpha" + str(definitionNumber) + ">=" + string.split("-")[1]
    
    def createGraphicPreferences(self, identifier, definitionNumber):
        """
        Returns the text in xml format to initialize all the graphic preference of a transition
        (this is used both by the potential and mandatory activities function)
        """
        if (definitionNumber >= 0):
            name = "talpha" + str(definitionNumber)
        else:
            name = "tbeta"
        nodeID = self.iterator.next()
        self.transitionsDictionnary.setdefault(name, nodeID)
        accumulator = ""
        accumulator += "<node id=\"" + str(nodeID) + "\" net=\"1\">\n"
        accumulator +="<attribute name=\"Name\" id=\"" + str(self.iterator.next()) + "\" net=\"1\">\n<![CDATA[" + name + "]]>\n" # Setting the name of the transition
        accumulator += "<graphics count=\"1\">\n"
        accumulator += "<graphic xoff=\"25.00\" yoff=\"20.00\" x=\"275.00\" y=\"220.00\" id=\"" + str(self.iterator.next()) + "\" net=\"1\" "
        accumulator += "show=\"1\" grparent=\"" + str(identifier) + "\" state=\"1\" pen=\"0,0,0\" brush=\"255,255,255\"/>\n" # graphic preferences for the name
        accumulator += "</graphics>\n</attribute>\n<attribute name=\"ID\" id=\"" + str(self.iterator.next()) + "\" net=\"1\">\n"
        accumulator += "<![CDATA[" + str(self.iteratorNumberOfTransitions.next()) + "]]>\n<graphics count=\"1\">\n" # Setting the id of the transition
        accumulator += "<graphic xoff=\"25.00\" yoff=\"20.00\" x=\"205.00\" y=\"220.00\" id=\"" + str(self.iterator.next()) + "\" net=\"1\" "
        accumulator += "show=\"0\" grparent=\"" + str(identifier) + "\" state=\"1\" pen=\"0,0,0\" brush=\"255,255,255\"/>\n" # graphic preferences for the id
        accumulator += "</graphics>\n</attribute>\n"
        accumulator += "<attribute name=\"Logic\" id=\"" + str(self.iterator.next()) + "\" net=\"1\">\n" # Setting the logic identifier (not used)
        accumulator += "<![CDATA[0]]>\n<graphics count=\"0\"/>\n</attribute>\n<attribute name=\"Comment\" id=\"" + str(self.iterator.next()) + "\" net=\"1\">\n" # Setting the comment of the transition
        accumulator += "<![CDATA[]]>\n<graphics count=\"1\">\n"
        accumulator += "<graphic yoff=\"40.00\" x=\"180.00\" y=\"240.00\" id=\"" + str(self.iterator.next()) + "\" net=\"1\" "
        accumulator += "show=\"1\" grparent=\"" + str(identifier) + "\" state=\"1\" pen=\"0,0,0\" brush=\"255,255,255\"/>\n" # graphic preferences for the comment
        accumulator += "</graphics>\n</attribute>\n"
        return accumulator
    
    def createPotentialGuard(self, identifier, string, definitionNumber):
        """
        Returns a text in the xml format for the correct guard of a potential activity
        """
        accumulator = ""
        accumulator += "<attribute name=\"GuardList\" type=\"ColList\" id=\"" + str(self.iterator.next()) + "\" net=\"1\">\n"
        accumulator += "<colList row_count=\"1\" col_count=\"2\" active_row=\"0\" active_col=\"0\">\n"
        accumulator += "<colList_head>\n<colList_colLabel>\n<![CDATA[Guard set]]>\n</colList_colLabel>\n"
        accumulator += "<colList_colLabel>\n<![CDATA[Guard]]>\n</colList_colLabel>\n</colList_head>\n"
        accumulator += "<colList_body>\n<colList_row nr=\"0\">\n<colList_col nr=\"0\">\n<![CDATA[Main]]>\n</colList_col>"
        accumulator += "<colList_col nr=\"1\">\n<![CDATA[" + self.stringToGuard(string, definitionNumber) + "]]>\n" # Setting the guard for the transition
        accumulator += "</colList_col>\n</colList_row>\n</colList_body>\n</colList>\n<graphics count=\"1\">\n"
        accumulator += "<graphic xoff=\"45.00\" yoff=\"-25.00\" x=\"305.00\" y=\"175.00\" id=\"" + str(self.iterator.next()) + "\" net=\"1\" "
        accumulator += "show=\"1\" grparent=\"" + str(identifier) + "\" state=\"1\" pen=\"0,0,0\" brush=\"255,255,255\"/>\n" # graphical preferences for the guard
        accumulator += "</graphics>\n</attribute>\n<graphics count=\"1\">\n"
        accumulator += "<graphic x=\"260.00\" y=\"200.00\" id=\"" + str(identifier) + "\" net=\"1\" "
        accumulator += "show=\"1\" w=\"20.00\" h=\"20.00\" state=\"1\" pen=\"0,0,0\" brush=\"255,255,255\"/>\n" # graphical preferences for the transition itself
        accumulator += "</graphics>\n</node>\n"
        return accumulator
    
    def makePotentialTransition(self, potentialDef, definitionNumber):
        """
        Returns the text in xml format to initialize a transition for a potential activity
        """
        identifier = self.iterator.next()
        return self.createGraphicPreferences(identifier, definitionNumber) + self.createPotentialGuard(identifier, potentialDef, definitionNumber)
    
    def createMandatoryGuard(self, identifier):
        """
        Returns a text in the xml format for the correct guard of a mandatory activity
        """
        accumulator = ""
        accumulator += "<attribute name=\"GuardList\" type=\"ColList\" id=\"" + str(self.iterator.next()) + "\" net=\"1\">\n"
        accumulator += "<colList row_count=\"1\" col_count=\"2\" active_row=\"0\" active_col=\"0\">\n"
        accumulator += "<colList_head>\n<colList_colLabel>\n<![CDATA[Guard set]]>\n</colList_colLabel>\n"
        accumulator += "<colList_colLabel>\n<![CDATA[Guard]]>\n</colList_colLabel>\n</colList_head>\n"
        accumulator += "<colList_body>\n<colList_row nr=\"0\">\n<colList_col nr=\"0\">\n<![CDATA[Main]]>\n</colList_col>"
        accumulator += "<colList_col nr=\"1\">\n<![CDATA[]]>\n" # Setting the guard to True for the transition
        accumulator += "</colList_col>\n</colList_row>\n</colList_body>\n</colList>\n<graphics count=\"1\">\n"
        accumulator += "<graphic xoff=\"45.00\" yoff=\"-25.00\" x=\"305.00\" y=\"175.00\" id=\"" + str(self.iterator.next()) + "\" net=\"1\" "
        accumulator += "show=\"1\" grparent=\"" + str(identifier) + "\" state=\"1\" pen=\"0,0,0\" brush=\"255,255,255\"/>\n" # graphical preferences for the guard
        accumulator += "</graphics>\n</attribute>\n<graphics count=\"1\">\n"
        accumulator += "<graphic x=\"260.00\" y=\"200.00\" id=\"" + str(identifier) + "\" net=\"1\" "
        accumulator += "show=\"1\" w=\"20.00\" h=\"20.00\" state=\"1\" pen=\"0,0,0\" brush=\"255,255,255\"/>\n" # graphical preferences for the transition itself
        accumulator += "</graphics>\n</node>\n"
        return accumulator
    
    def makeMandatoryTransition(self):
        """
        Returns the text in xml format to initialize a transition for a mandatory activity
        """
        identifier = self.iterator.next()
        return self.createGraphicPreferences(identifier, -1) + self.createMandatoryGuard(identifier)
    
    def makeText(self):
        """
        Returns the text generated in the xml format for all the definitions of the transitions (potential + mandatory)
        """
        startTransitions = "<nodeclass count=\"" + str(self.numberOfTransitions) + "\" name=\"Transition\">\n"
        endTransitions = "</nodeclass>\n"
        accumulator = ""
        splittedDefinition = self.potentialDefinition.split("\n")
        for i in range(len(splittedDefinition)):
            # A loop to create the transitions for each potential definition
            accumulator += self.makePotentialTransition(splittedDefinition[i], i)
        accumulator += self.makeMandatoryTransition() # creates the unique transition for all the mandatory activities
        with open("transitions.c", 'w') as f:
            pickle.dump(self.transitionsDictionnary, f)
        return startTransitions + accumulator + endTransitions