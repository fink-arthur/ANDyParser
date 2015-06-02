# coding=utf-8

class Places:
    """
    This class will generate all the text in the correct "snoopy" format to initialize
    all the places that will be used by the petri net
    """

    def __init__(self, entityDefinition, potentialDefinition, mandatoryDefinition):
        self.entityDefinition = entityDefinition
        self.potentialDefinition = potentialDefinition
        self.mandatoryDefinition = mandatoryDefinition
        # an iterator so that all the id used in a places are controlled and not repeated
        self.iterator = iter(range(20000,30000))
        # numberOfPLaces = numberOfEntities + numberOfPotential + numberOfMandatory
        self.numberOfPlaces = (self.entityDefinition.rstrip().lstrip().count("\n") + 1) + (self.potentialDefinition.rstrip().lstrip().count("\n") + 1) + (self.mandatoryDefinition.rstrip().lstrip().count("\n") + 1)
        self.iteratorNumberOfPlaces = iter(range(self.numberOfPlaces))

    def createGraphicPreferences(self, identifier, name):
        accumulator = ""
        accumulator += "<node identifier=\"" + str(self.iterator.next()) + "\" net=\"1\">\n"
        accumulator +="<attribute name=\"Name\" identifier=\"" + str(self.iterator.next()) + "\" net=\"1\">\n<![CDATA[" + name + "]]>\n"
        accumulator += "<graphics count=\"1\">\n"
        accumulator += "<graphic xoff=\"25.00\" yoff=\"20.00\" x=\"205.00\" y=\"220.00\" identifier=\"" + str(self.iterator.next()) + "\" net=\"1\" "
        accumulator += "show=\"1\" grparent=\"" + str(identifier) + "\" state=\"1\" pen=\"0,0,0\" brush=\"255,255,255\"/>\n"
        accumulator += "</graphics>\n</attribute>\n<attribute name=\"ID\" identifier=\"" + str(self.iterator.next()) + "\" net=\"1\">\n"
        accumulator += "<![CDATA[" + str(self.iteratorNumberOfPlaces.next()) + "]]>\n\n<graphics count=\"1\">\n"
        accumulator += "<graphic xoff=\"25.00\" yoff=\"20.00\" x=\"205.00\" y=\"220.00\" identifier=\"" + str(self.iterator.next()) + "\" net=\"1\" "
        accumulator += "show=\"0\" grparent=\"" + str(identifier) + "\" state=\"1\" pen=\"0,0,0\" brush=\"255,255,255\"/>\n"
        accumulator += "</graphics>\n</attribute>\n<attribute name=\"Marking\" identifier=\"" + str(self.iterator.next()) + "\" net=\"1\">\n"
        accumulator += "<![CDATA[1]]>\n\n<graphics count=\"1\">\n"
        accumulator += "<graphic x=\"180.00\" y=\"200.00\" identifier=\"" + str(self.iterator.next()) + "\" net=\"1\" "
        accumulator += "show=\"1\" grparent=\"" + str(identifier) + "\" state=\"1\" pen=\"0,0,0\" brush=\"255,255,255\"/>\n"
        accumulator += "</graphics>\n</attribute>\n<attribute name=\"Logic\" identifier=\"" + str(self.iterator.next()) + "\" net=\"1\">\n"
        accumulator += "<![CDATA[0]]>\n<graphics count=\"0\"/>\n</attribute>\n<attribute name=\"Comment\" identifier=\"" + str(self.iterator.next()) + "\" net=\"1\">\n"
        accumulator += "<![CDATA[]]>\n<graphics count=\"1\">\n"
        accumulator += "<graphic yoff=\"40.00\" x=\"180.00\" y=\"240.00\" identifier=\"" + str(self.iterator.next()) + "\" net=\"1\" "
        accumulator += "show=\"1\" grparent=\"" + str(identifier) + "\" state=\"1\" pen=\"0,0,0\" brush=\"255,255,255\"/>\n"
        accumulator += "</graphics>\n</attribute>\n"
        return accumulator
    
    def creatingLambda(self, numberOfLevel):
        accumulator = "0"
        for _ in range(1,numberOfLevel):
            accumulator += ",0"
        return accumulator

    def createMarkingPreferenceEntity(self, identifier, name, numberOfLevel):
        accumulator = ""
        accumulator += "<attribute name=\"MarkingList\" type=\"ColList\" identifier=\"" + str(self.iterator.next()) + "\" net=\"1\">\n<colList row_count=\"1\" col_count=\"2\" active_row=\"0\" active_col=\"0\">\n"
        accumulator += "<colList_head>\n<colList_colLabel>\n<![CDATA[Color/Predicate/Function]]>\n</colList_colLabel>\n"
        accumulator += "<colList_colLabel>\n<![CDATA[Marking]]>\n</colList_colLabel>\n</colList_head>\n<colList_body>\n"
        accumulator += "<colList_row nr=\"0\">\n<colList_col nr=\"0\">\n<![CDATA[" + "(0,0,(" + self.creatingLambda(numberOfLevel) + "))" + "]]>\n</colList_col>\n<colList_col nr=\"1\">\n"
        accumulator += "<![CDATA[1]]>\n</colList_col>\n</colList_row>\n</colList_body>\n</colList>\n<graphics count=\"1\">\n"
        accumulator += "<graphic xoff=\"34.00\" yoff=\"-19.00\" x=\"214.00\" y=\"181.00\" identifier=\"" + str(self.iterator.next()) + "\" net=\"1\" "
        accumulator += "show=\"1\" grparent=\"" + str(identifier) + "\" state=\"1\" pen=\"0,0,0\" brush=\"255,255,255\"/>\n"
        accumulator += "</graphics>\n</attribute>\n<attribute name=\"Colorset\" identifier=\"13666\" net=\"1\">\n<![CDATA[" + str(name) + "]]>\n<graphics count=\"1\">\n"
        accumulator += "<graphic yoff=\"-20.00\" x=\"180.00\" y=\"180.00\" identifier=\"" + str(self.iterator.next()) + "\" net=\"1\" "
        accumulator += "show=\"1\" grparent=\"" + str(identifier) + "\" state=\"1\" pen=\"0,0,0\" brush=\"0,0,255\"/>\n"
        accumulator += "</graphics>\n</attribute>\n<graphics count=\"1\">\n"
        accumulator += "<graphic x=\"180.00\" y=\"200.00\" identifier=\"" + str(identifier) + "\" net=\"1\" "
        accumulator += "show=\"1\" w=\"20.00\" h=\"20.00\" state=\"1\" pen=\"0,0,0\" brush=\"255,255,255\"/>"
        accumulator += "</graphics>\n</node>\n"
        return accumulator

    def makeEntityPlace(self, identifier, name, numberOfLevel):
        return self.createGraphicPreferences(identifier, name) + self.createMarkingPreferenceEntity(name, identifier, numberOfLevel)

    def makeText(self):
        startPlaces = "<?xml version=\"1.0\" encoding=\"utf-8\"?>\n<?xml-stylesheet type=\"text/xsl\" href=\"/xsl/spped2svg.xsl\"?>\n<Snoopy version=\"2\" revision=\"1.13\">\n<netclass name=\"Colored Extended Petri Net\"/>\n<nodeclasses count=\"4\">\n<nodeclass count=\"" + str(self.numberOfPlaces) + "\" name=\"Place\">\n"
        endPlaces = "</nodeclass>\n"
        accumulator = ""
        for i in (self.entityDefinition.split("\n")):
            numberOfLevel = i.split(":")[1].count(",") + 1
            name = i.split(":")[0]
            accumulator += self.makeEntityPlace(self.iterator.next(), name, numberOfLevel)
        return startPlaces + accumulator + endPlaces