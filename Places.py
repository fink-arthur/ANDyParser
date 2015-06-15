# coding=utf-8

import pickle, re

class Places:
    """
    This class will generate all the text in the correct xml format to initialize
    all the places that will be used by the petri net
    """

    def __init__(self, entityDefinition, potentialDefinition, mandatoryDefinition, initialMarking):
        self.entityDefinition = entityDefinition
        self.potentialDefinition = potentialDefinition
        self.mandatoryDefinition = mandatoryDefinition
        # an iterator so that all the id used in a places are controlled and not repeated
        self.iterator = iter(range(20000,30000))
        # numberOfPLaces = numberOfEntities + numberOfPotential + numberOfMandatory
        self.numberOfPlaces = (self.entityDefinition.rstrip().lstrip().count("\n") + 1) + (self.potentialDefinition.rstrip().lstrip().count("\n") + 1) + (self.mandatoryDefinition.rstrip().lstrip().count("\n") + 1)
        self.iteratorNumberOfPlaces = iter(range(self.numberOfPlaces))
        self.placesDictionnary = dict()
        self.initialMarking = dict()
        rePattern = re.compile("[a-zA-Z0-9]+,[0-9]+")
        for i in re.findall(rePattern, initialMarking):
            self.initialMarking.setdefault(i.split(",")[0],i.split(",")[1])

    def createGraphicPreferences(self, identifier, name):
        """
        Returns the text in xml format to initialize all the graphic preference of a place
        (this is used both by the activity and the entity functions)
        """
        nodeID = self.iterator.next()
        self.placesDictionnary.setdefault(name, nodeID)
        accumulator = ""
        accumulator += "<node id=\"" + str(nodeID) + "\" net=\"1\">\n"
        accumulator +="<attribute name=\"Name\" id=\"" + str(self.iterator.next()) + "\" net=\"1\">\n<![CDATA[" + name + "]]>\n" # Setting the name of the place
        accumulator += "<graphics count=\"1\">\n"
        accumulator += "<graphic xoff=\"25.00\" yoff=\"20.00\" x=\"205.00\" y=\"220.00\" id=\"" + str(self.iterator.next()) + "\" net=\"1\" "
        accumulator += "show=\"1\" grparent=\"" + str(identifier) + "\" state=\"1\" pen=\"0,0,0\" brush=\"255,255,255\"/>\n" # graphic preferences for the name
        accumulator += "</graphics>\n</attribute>\n<attribute name=\"ID\" id=\"" + str(self.iterator.next()) + "\" net=\"1\">\n"
        accumulator += "<![CDATA[" + str(self.iteratorNumberOfPlaces.next()) + "]]>\n<graphics count=\"1\">\n" # Setting the id of the place
        accumulator += "<graphic xoff=\"25.00\" yoff=\"20.00\" x=\"205.00\" y=\"220.00\" id=\"" + str(self.iterator.next()) + "\" net=\"1\" "
        accumulator += "show=\"0\" grparent=\"" + str(identifier) + "\" state=\"1\" pen=\"0,0,0\" brush=\"255,255,255\"/>\n" # graphic preferences for the id
        accumulator += "</graphics>\n</attribute>\n<attribute name=\"Marking\" id=\"" + str(self.iterator.next()) + "\" net=\"1\">\n" # Setting the marking for the place
        accumulator += "<![CDATA[1]]>\n<graphics count=\"1\">\n"
        accumulator += "<graphic x=\"180.00\" y=\"200.00\" id=\"" + str(self.iterator.next()) + "\" net=\"1\" "
        accumulator += "show=\"1\" grparent=\"" + str(identifier) + "\" state=\"1\" pen=\"0,0,0\" brush=\"255,255,255\"/>\n" # graphic preferences for the marking
        accumulator += "</graphics>\n</attribute>\n<attribute name=\"Logic\" id=\"" + str(self.iterator.next()) + "\" net=\"1\">\n" # Setting the logic identifier (not used)
        accumulator += "<![CDATA[0]]>\n<graphics count=\"0\"/>\n</attribute>\n<attribute name=\"Comment\" id=\"" + str(self.iterator.next()) + "\" net=\"1\">\n" # Setting the comment for the place
        accumulator += "<![CDATA[]]>\n<graphics count=\"1\">\n"
        accumulator += "<graphic yoff=\"40.00\" x=\"180.00\" y=\"240.00\" id=\"" + str(self.iterator.next()) + "\" net=\"1\" "
        accumulator += "show=\"1\" grparent=\"" + str(identifier) + "\" state=\"1\" pen=\"0,0,0\" brush=\"255,255,255\"/>\n" # graphical preferences for the comment
        accumulator += "</graphics>\n</attribute>\n"
        return accumulator
    
    def creatingLambda(self, numberOfLevel):
        """
        Returns a string with numberOfLevel * D,
        """
        accumulator = "0"
        for _ in range(1,numberOfLevel):
            accumulator += ",0"
        return accumulator
    
    def creatingInitialMarking(self, name):
        try:
            return self.initialMarking[name]
        except KeyError:
            return "0"

    def createMarkingPreferenceEntity(self, name, identifier, numberOfLevel):
        """
        Returns the text in xml format to initialize a place for an entity with the correct marking
        """
        accumulator = ""
        accumulator += "<attribute name=\"MarkingList\" type=\"ColList\" id=\"" + str(self.iterator.next()) + "\" net=\"1\">\n<colList row_count=\"1\" col_count=\"2\" active_row=\"0\" active_col=\"0\">\n"
        accumulator += "<colList_head>\n<colList_colLabel>\n<![CDATA[Color/Predicate/Function]]>\n</colList_colLabel>\n"
        accumulator += "<colList_colLabel>\n<![CDATA[Marking]]>\n</colList_colLabel>\n</colList_head>\n<colList_body>\n"
        # the next 2 lines initialize the marking with everything at 0 and a single token
        accumulator += "<colList_row nr=\"0\">\n<colList_col nr=\"0\">\n<![CDATA[" + "(" + self.creatingInitialMarking(name) + ",0,(" + self.creatingLambda(numberOfLevel) + "))" + "]]>\n</colList_col>\n<colList_col nr=\"1\">\n"
        accumulator += "<![CDATA[1]]>\n</colList_col>\n</colList_row>\n</colList_body>\n</colList>\n<graphics count=\"1\">\n"
        accumulator += "<graphic xoff=\"34.00\" yoff=\"-19.00\" x=\"214.00\" y=\"181.00\" id=\"" + str(self.iterator.next()) + "\" net=\"1\" "
        accumulator += "show=\"1\" grparent=\"" + str(identifier) + "\" state=\"1\" pen=\"0,0,0\" brush=\"255,255,255\"/>\n"# graphic preferences for the current marking of the place
        accumulator += "</graphics>\n</attribute>\n<attribute name=\"Colorset\" id=\"" + str(self.iterator.next()) + "\" net=\"1\">\n<![CDATA[" + str(name) + "]]>\n<graphics count=\"1\">\n" # Setting the color set of the place
        accumulator += "<graphic yoff=\"-20.00\" x=\"180.00\" y=\"180.00\" id=\"" + str(self.iterator.next()) + "\" net=\"1\" "
        accumulator += "show=\"0\" grparent=\"" + str(identifier) + "\" state=\"1\" pen=\"0,0,0\" brush=\"0,0,255\"/>\n" # graphical preferences for the color set
        accumulator += "</graphics>\n</attribute>\n<graphics count=\"1\">\n"
        accumulator += "<graphic x=\"180.00\" y=\"200.00\" id=\"" + str(identifier) + "\" net=\"1\" "
        accumulator += "show=\"1\" w=\"20.00\" h=\"20.00\" state=\"1\" pen=\"0,0,0\" brush=\"255,255,255\"/>\n" # graphic preferences for the place itself
        accumulator += "</graphics>\n</node>\n"
        return accumulator

    def makeEntityPlace(self, identifier, name, numberOfLevel):
        """
        Returns the text in xml format to initialize the place for the entity
        """
        return self.createGraphicPreferences(identifier, name) + self.createMarkingPreferenceEntity(name, identifier, numberOfLevel)

    def createMarkingPreferenceActivity(self, identifier, name):
        """
        Returns the text in xml format to initialize a place for an activity with the correct marking
        """
        accumulator = ""
        accumulator += "<attribute name=\"MarkingList\" type=\"ColList\" id=\"" + str(self.iterator.next()) + "\" net=\"1\">\n<colList row_count=\"1\" col_count=\"2\" active_row=\"0\" active_col=\"0\">\n"
        accumulator += "<colList_head>\n<colList_colLabel>\n<![CDATA[Color/Predicate/Function]]>\n</colList_colLabel>\n"
        accumulator += "<colList_colLabel>\n<![CDATA[Marking]]>\n</colList_colLabel>\n</colList_head>\n<colList_body>\n"
        # the next 2 lines initialize the marking at 0 and a single token
        accumulator += "<colList_row nr=\"0\">\n<colList_col nr=\"0\">\n<![CDATA[0]]>\n</colList_col>\n<colList_col nr=\"1\">\n"
        accumulator += "<![CDATA[1]]>\n</colList_col>\n</colList_row>\n</colList_body>\n</colList>\n<graphics count=\"1\">\n"
        accumulator += "<graphic xoff=\"34.00\" yoff=\"-19.00\" x=\"214.00\" y=\"181.00\" id=\"" + str(self.iterator.next()) + "\" net=\"1\" "
        accumulator += "show=\"1\" grparent=\"" + str(identifier) + "\" state=\"1\" pen=\"0,0,0\" brush=\"255,255,255\"/>\n" # graphic preferences for the current marking of the place
        accumulator += "</graphics>\n</attribute>\n<attribute name=\"Colorset\" id=\"13666\" net=\"1\">\n<![CDATA[D]]>\n<graphics count=\"1\">\n" # Setting the color set of the place
        accumulator += "<graphic yoff=\"-20.00\" x=\"180.00\" y=\"180.00\" id=\"" + str(self.iterator.next()) + "\" net=\"1\" "
        accumulator += "show=\"0\" grparent=\"" + str(identifier) + "\" state=\"1\" pen=\"0,0,0\" brush=\"0,0,255\"/>\n" # graphical preferences for the color set
        accumulator += "</graphics>\n</attribute>\n<graphics count=\"1\">\n"
        accumulator += "<graphic x=\"180.00\" y=\"200.00\" id=\"" + str(identifier) + "\" net=\"1\" "
        accumulator += "show=\"1\" w=\"20.00\" h=\"20.00\" state=\"1\" pen=\"0,0,0\" brush=\"255,255,255\"/>\n" # graphic preferences for the place itself
        accumulator += "</graphics>\n</node>\n"
        return accumulator
    
    def makeActivityPlace(self, identifier, name):
        """
        Returns the text in xml format to initialize the place for the activity
        """
        return self.createGraphicPreferences(identifier, name) + self.createMarkingPreferenceActivity(identifier, name)

    def makeText(self):
        """
        Returns the text generated in the xml format for all the definitions of the places (entities + activities)
        """
        startPlaces = "<?xml version=\"1.0\" encoding=\"utf-8\"?>\n<?xml-stylesheet type=\"text/xsl\" href=\"/xsl/spped2svg.xsl\"?>\n<Snoopy version=\"2\" revision=\"1.13\">\n<netclass name=\"Colored Extended Petri Net\"/>\n<nodeclasses count=\"4\">\n<nodeclass count=\"" + str(self.numberOfPlaces) + "\" name=\"Place\">\n"
        endPlaces = "</nodeclass>\n"
        accumulator = ""
        for i in (self.entityDefinition.split("\n")):
            # A loop to create all the places for each entity
            numberOfLevel = i.split(":")[1].count(",") + 1
            name = i.split(":")[0].rstrip().lstrip()
            accumulator += self.makeEntityPlace(self.iterator.next(), name, numberOfLevel)
        splittedPotential = self.potentialDefinition.split("\n")
        if not((len(splittedPotential) == 1) & (splittedPotential[0].rstrip().lstrip() == "")):
            for i in range(len(splittedPotential)):
                # A loop to create all the places for each potential activity
                accumulator += self.makeActivityPlace(self.iterator.next(), "palpha" + str(i))
        splittedMandatory = self.mandatoryDefinition.split("\n")
        if not((len(splittedMandatory) == 1) & (splittedMandatory[0].rstrip().lstrip() == "")):
            for i in range(len(splittedMandatory)):
                # A loop to create all the places for each mandatory activity
                accumulator += self.makeActivityPlace(self.iterator.next(), "pbeta" + str(i))
        with open("places.c", 'w') as f:
            pickle.dump(self.placesDictionnary, f)
        return startPlaces + accumulator + endPlaces