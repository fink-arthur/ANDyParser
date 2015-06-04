# coding=utf-8

class Colours:
    """
    This class will generate all the text in the correct xml format to create
    all the colour sets that will need to be used for the petri net (simple and compounded)
    """

    def __init__(self, entityDefinition, potentialDefinition, mandatoryDefinition):
        self.entityDefinition = entityDefinition
        self.potentialDefinition = potentialDefinition
        self.mandatoryDefinition = mandatoryDefinition
        
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
        maximumPotential = 0
        for i in self.potentialDefinition.split("\n"):
            duration = int(i.split("-")[1])
            if (duration > maximumPotential):
                maximumPotential = duration
        maximumMandatory = 0
        for i in self.mandatoryDefinition.split("\n"):
            duration = int(i.split("-")[1])
            if (duration > maximumPotential):
                maximumMandatory = duration
        if (maximumMandatory > maximumPotential):
            return maximumMandatory
        else:
            return maximumPotential
    
    def createSimpleColorSet(self):
        """
        Creates all the simple color set needed for the petri net
        """
        numberOfEntityLines = self.entityDefinition.rstrip().lstrip().count("\n") + 1
        numberOfColours = 2 * numberOfEntityLines + 1
        lines = self.entityDefinition.rstrip().lstrip().split("\n")
        startString =  "<attribute name=\"ColorsetList\" type=\"ColList\" id=\"7039\" net=\"1\">\n<colList row_count=\"" + str(numberOfColours) + "\" col_count=\"5\" active_row=\"0\" active_col=\"0\">\n<colList_head>\n<colList_colLabel>\n<![CDATA[]]>\n</colList_colLabel>\n<colList_colLabel>\n<![CDATA[]]>\n</colList_colLabel>\n<colList_colLabel>\n<![CDATA[]]>\n</colList_colLabel>\n<colList_colLabel>\n<![CDATA[]]>\n</colList_colLabel>\n<colList_colLabel>\n<![CDATA[]]>\n</colList_colLabel>\n</colList_head>\n<colList_body>\n"
        accumulator = ""
        
        for i in range(numberOfEntityLines):
            # A loop to create the colors that will define the current level at which the entity is
            splittedLine = lines[i].split(":")
            accumulator += "<colList_row nr=\"" + str(i) + "\">\n"
            accumulator += "<colList_col nr=\"1\">\n"
            accumulator += "<![CDATA[" + "l" + splittedLine[0].rstrip().lstrip() + "]]>\n" # we take the name of the entity
            accumulator += "</colList_col>\n<colList_col nr=\"1\">\n<![CDATA[int]]>\n</colList_col>\n<colList_col nr=\"2\">\n"
            accumulator += "<![CDATA[0-" + str(len(splittedLine[1].split(",")) - 1) + "]]>\n" # we count how many levels there are
            accumulator += "</colList_col>\n<colList_col nr=\"3\">\n<![CDATA[white]]>\n</colList_col>\n<colList_col nr=\"4\">\n<![CDATA[]]>\n</colList_col>\n</colList_row>\n"
        
        for i in range(numberOfEntityLines):
            # A loop to create the colors that will define the duration spent at the current level since the last update for each entity
            accumulator += "<colList_row nr=\"" + str(i + numberOfEntityLines) + "\">\n"
            accumulator += "<colList_col nr=\"1\">\n"
            accumulator += "<![CDATA[" + "u" + lines[i].split(":")[0].rstrip().lstrip() + "]]>\n" # we take the name of the entity
            accumulator += "</colList_col>\n<colList_col nr=\"1\">\n<![CDATA[int]]>\n</colList_col>\n<colList_col nr=\"2\">\n"
            accumulator += "<![CDATA[0-" + str(self.figuringdOut(lines[i])) + "]]>\n"
            accumulator += "</colList_col>\n<colList_col nr=\"3\">\n<![CDATA[white]]>\n</colList_col>\n<colList_col nr=\"4\">\n<![CDATA[]]>\n</colList_col>\n</colList_row>\n"
        
        # We need a color of size D so that we can create the lambdas for all the entities and the timers for the activities both mandatory and potential
        accumulator += "<colList_row nr=\"" + str(numberOfColours - 1) + "\">\n"
        accumulator += "<colList_col nr=\"1\">\n"
        accumulator += "<![CDATA[D]]>\n"
        accumulator += "</colList_col>\n<colList_col nr=\"1\">\n<![CDATA[int]]>\n</colList_col>\n<colList_col nr=\"2\">\n"
        accumulator += "<![CDATA[0-" + str(self.figuringDOut()) + "]]>\n"
        accumulator += "</colList_col>\n<colList_col nr=\"3\">\n<![CDATA[white]]>\n</colList_col>\n<colList_col nr=\"4\">\n<![CDATA[]]>\n</colList_col>\n</colList_row>\n"
        
        endString = "</colList_body>\n</colList>\n<graphics count=\"0\"/>\n</attribute>\n<graphics count=\"0\"/>\n</metadata>\n</metadataclass>\n"
        return startString + accumulator + endString
    
    def creatingLambda(self, numbersOfLevel):
        """
        Returns the color compound that defines the lambda of an entity
        """
        accumulateur = "D"
        for _ in range(1,numbersOfLevel):
            accumulateur += ",D"
        return accumulateur
    
    def creatingEntityCompound(self, entityName):
        """
        Returns the color compound that defines an entity
        """
        return "l" + entityName + ",u" + entityName + ",lambda" + entityName
    
    def createCompoundColorSet(self):
        """
        Creates all the compound color set using the simple color set for the petri net
        """
        numberOfEntityLines = self.entityDefinition.rstrip().lstrip().count("\n") + 1
        numberOfColours = 2 * numberOfEntityLines
        lines = self.entityDefinition.rstrip().lstrip().split("\n")
        startString = "<attribute name=\"StructuredColorsetList\" type=\"ColList\" id=\"7044\" net=\"1\">\n<colList row_count=\"" + str(numberOfColours) + "\" col_count=\"6\" active_row=\"0\" active_col=\"0\">\n<colList_head>\n<colList_colLabel>\n<![CDATA[]]>\n</colList_colLabel>\n<colList_colLabel>\n<![CDATA[]]>\n</colList_colLabel>\n<colList_colLabel>\n<![CDATA[]]>\n</colList_colLabel>\n<colList_colLabel>\n<![CDATA[]]>\n</colList_colLabel>\n<colList_colLabel>\n<![CDATA[]]>\n</colList_colLabel>\n<colList_colLabel>\n<![CDATA[]]>\n</colList_colLabel>\n</colList_head>\n<colList_body>"
        accumulator = ""
        
        for i in range(numberOfEntityLines):
            # A loop to create the compound colors that will be used to define the lambdas of all the entities
            splittedLine = lines[i].split(":")
            accumulator += "<colList_row nr=\"" + str(i) + "\">\n"
            accumulator += "<colList_col nr=\"0\">\n"
            accumulator += "<![CDATA[" + "lambda" + splittedLine[0].rstrip().lstrip() + "]]>\n" # we take the name of the entity
            accumulator += "</colList_col>\n<colList_col nr=\"1\">\n<![CDATA[product]]>\n</colList_col>\n<colList_col nr=\"2\">\n"
            accumulator += "<![CDATA[" + self.creatingLambda(splittedLine[1].count(",") + 1) + "]]>"
            accumulator += "</colList_col>\n<colList_col nr=\"3\">\n<![CDATA[]]>\n</colList_col>\n<colList_col nr=\"4\">\n<![CDATA[white]]>\n</colList_col>\n<colList_col nr=\"5\">\n<![CDATA[]]>\n</colList_col>\n</colList_row>\n"
        
        for i in range(numberOfEntityLines):
            # A loop to create the compound colors that will be used to define each entities
            splittedLine = lines[i].split(":")
            accumulator += "<colList_row nr=\"" + str(i + numberOfEntityLines) + "\">\n"
            accumulator += "<colList_col nr=\"0\">\n"
            accumulator += "<![CDATA[" + splittedLine[0].rstrip().lstrip() + "]]>\n" # we take the name of the entity
            accumulator += "</colList_col>\n<colList_col nr=\"1\">\n<![CDATA[product]]>\n</colList_col>\n<colList_col nr=\"2\">\n"
            accumulator += "<![CDATA[" + self.creatingEntityCompound(splittedLine[0].rstrip().lstrip()) + "]]>"
            accumulator += "</colList_col>\n<colList_col nr=\"3\">\n<![CDATA[]]>\n</colList_col>\n<colList_col nr=\"4\">\n<![CDATA[white]]>\n</colList_col>\n<colList_col nr=\"5\">\n<![CDATA[]]>\n</colList_col>\n</colList_row>\n"
        
        endString = "</colList_body>\n</colList>\n<graphics count=\"0\"/>\n</attribute>\n<graphics count=\"0\"/>\n</metadata>\n</metadataclass>\n"
        return startString + accumulator + endString
    
    def makeText(self):
        """
        Returns the text generated in the xml format for all the definitions of the colors
        """
        # the string that contains all the unchanging data when creating the simple color sets
        startStringSimpleColor = "<metadataclass count=\"1\" name=\"Basic Colorset Class\">\n<metadata id=\"7035\" net=\"1\">\n<attribute name=\"Name\" id=\"7036\" net=\"1\">\n<![CDATA[NewColorset]]>\n<graphics count=\"0\"/>\n</attribute>\n<attribute name=\"ID\" id=\"7037\" net=\"1\">\n<![CDATA[0]]>\n<graphics count=\"0\"/>\n</attribute>\n<attribute name=\"Comment\" id=\"7038\" net=\"1\">\n<![CDATA[]]>\n<graphics count=\"0\"/>\n</attribute>\n"
        simpleColorSet = startStringSimpleColor + self.createSimpleColorSet()
        # the string that contains all the unchanging data when creating a compound colored set
        startStringCompoundColor =  "<metadataclass count=\"1\" name=\"Structured Colorset Class\">\n<metadata id=\"7040\" net=\"1\">\n<attribute name=\"Name\" id=\"7041\" net=\"1\">\n<![CDATA[NewColorset]]>\n<graphics count=\"0\"/>\n</attribute>\n<attribute name=\"ID\" id=\"7042\" net=\"1\">\n<![CDATA[0]]>\n<graphics count=\"0\"/>\n</attribute>\n<attribute name=\"Comment\" id=\"7043\" net=\"1\">\n<![CDATA[]]>\n<graphics count=\"0\"/>\n</attribute>\n"
        compoundColorSet = startStringCompoundColor + self.createCompoundColorSet()
        # the string that contains all the data for the alias color set which is unused
        StringAliasColor = "<metadataclass count=\"1\" name=\"Alias Colorset Class\">\n<metadata id=\"11959\" net=\"1\">\n<attribute name=\"Name\" id=\"11960\" net=\"1\">\n<![CDATA[NewColorset]]>\n<graphics count=\"0\"/>\n</attribute>\n<attribute name=\"ID\" id=\"11961\" net=\"1\">\n<![CDATA[0]]>\n<graphics count=\"0\"/>\n</attribute>\n<attribute name=\"Comment\" id=\"11962\" net=\"1\">\n<![CDATA[]]>\n<graphics count=\"0\"/>\n</attribute>\n<attribute name=\"AliasColorsetList\" type=\"ColList\" id=\"11963\" net=\"1\">\n<colList row_count=\"0\" col_count=\"3\" active_row=\"0\" active_col=\"0\">\n<colList_head>\n<colList_colLabel>\n<![CDATA[]]>\n</colList_colLabel>\n<colList_colLabel>\n<![CDATA[]]>\n</colList_colLabel>\n<colList_colLabel>\n<![CDATA[]]>\n</colList_colLabel>\n</colList_head>\n<colList_body/>\n</colList>\n<graphics count=\"0\"/>\n</attribute>\n<graphics count=\"0\"/>\n</metadata>\n</metadataclass>\n"
        return simpleColorSet + compoundColorSet + StringAliasColor