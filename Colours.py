# coding=utf-8

class Colours:
    """
    This class will generate all the text in the correct "snoopy" format to initialize
    all the colour sets that will need to be used for the petri net (simple and compounded)
    """
        
    def figuringdOut(self, line):
        """
        Returns d for an entity where d is the highest decay duration for a level
        """
        levels = line.split(":")[1].lstrip().rstrip()[1:-1].split(",")
        accumulator = int(levels[0].lstrip().rstrip())
        for i in range(1, len(levels)):
            if (accumulator < int(levels[i])):
                accumulator = levels[i].lstrip().rstrip()
        return accumulator
    
    def figuringDOut(self, potentialDefinition, mandatoryDefinition):
        """
        Returns D for all the activities where D is the highest duration for an activity
        """
        maximumPotential = 0
        for i in potentialDefinition.split("\n"):
            duration = int(i.split("-")[1])
            if (duration > maximumPotential):
                maximumPotential = duration
        maximumMandatory = 0
        for i in mandatoryDefinition.split("\n"):
            duration = int(i.split("-")[1])
            if (duration > maximumPotential):
                maximumMandatory = duration
        if (maximumMandatory > maximumPotential):
            return maximumMandatory
        else:
            return maximumPotential
    
    def createSimpleColorSet(self, entityDefinition, potentialDefinition, mandatoryDefinition):
        """
        Creates all the simple color set needed for the petri net
        """
        numberOfEntityLines = entityDefinition.rstrip().lstrip().count("\n") + 1
        numberOfPotentialLines = potentialDefinition.rstrip().lstrip().count("\n") + 1
        numberOfMandatoryLines = mandatoryDefinition.rstrip().lstrip().count("\n") + 1
        numberOfColours = 2 * numberOfEntityLines + numberOfPotentialLines + numberOfMandatoryLines + 1
        lines = entityDefinition.rstrip().lstrip().split("\n")
        startString =  "<attribute name=\"ColorsetList\" type=\"ColList\" id=\"7039\" net=\"1\">\n<colList row_count=\"" + str(numberOfColours) + "\" col_count=\"5\" active_row=\"0\" active_col=\"0\">\n<colList_head>\n<colList_colLabel>\n<![CDATA[]]>\n</colList_colLabel>\n<colList_colLabel>\n<![CDATA[]]>\n</colList_colLabel>\n<colList_colLabel>\n<![CDATA[]]>\n</colList_colLabel>\n<colList_colLabel>\n<![CDATA[]]>\n</colList_colLabel>\n<colList_colLabel>\n<![CDATA[]]>\n</colList_colLabel>\n</colList_head>\n<colList_body>\n"
        accumulator = ""
        
        for i in range(numberOfEntityLines):
            # A loop to create the colors that will define the current level at which the entity is
            splittedLine = lines[i].split(":")
            accumulator += "<colList_row nr=\"" + str(i) + "\">\n"
            accumulator += "<colList_col nr=\"1\">\n"
            accumulator += "<![CDATA[" + "l" + splittedLine[0].rstrip().lstrip() + "]]>\n"
            accumulator += "</colList_col>\n<colList_col nr=\"1\">\n<![CDATA[int]]>\n</colList_col>\n<colList_col nr=\"2\">\n"
            accumulator += "<![CDATA[0-" + str(len(splittedLine[1].split(",")) - 1) + "]]>\n"
            accumulator += "</colList_col>\n<colList_col nr=\"3\">\n<![CDATA[white]]>\n</colList_col>\n<colList_col nr=\"4\">\n<![CDATA[]]>\n</colList_col>\n</colList_row>\n"
        
        for i in range(numberOfEntityLines):
            # A loop to create the colors that will define the duration spent at the current level since the last update for each entity
            accumulator += "<colList_row nr=\"" + str(i + numberOfEntityLines) + "\">\n"
            accumulator += "<colList_col nr=\"1\">\n"
            accumulator += "<![CDATA[" + "u" + lines[i].split(":")[0].rstrip().lstrip() + "]]>\n"
            accumulator += "</colList_col>\n<colList_col nr=\"1\">\n<![CDATA[int]]>\n</colList_col>\n<colList_col nr=\"2\">\n"
            accumulator += "<![CDATA[0-" + str(self.figuringdOut(lines[i])) + "]]>\n"
            accumulator += "</colList_col>\n<colList_col nr=\"3\">\n<![CDATA[white]]>\n</colList_col>\n<colList_col nr=\"4\">\n<![CDATA[]]>\n</colList_col>\n</colList_row>\n"
        
        for i in range(numberOfPotentialLines):
            # A loop to create the colors that will define how long since a potential activity was fired
            accumulator += "<colList_row nr=\"" + str(i + 2 * numberOfEntityLines) + "\">\n"
            accumulator += "<colList_col nr=\"1\">\n"
            accumulator += "<![CDATA[" + "alpha" + str(i) + "]]>\n"
            accumulator += "</colList_col>\n<colList_col nr=\"1\">\n<![CDATA[int]]>\n</colList_col>\n<colList_col nr=\"2\">\n"
            accumulator += "<![CDATA[0-" + str(self.figuringDOut(potentialDefinition, mandatoryDefinition)) + "]]>\n"
            accumulator += "</colList_col>\n<colList_col nr=\"3\">\n<![CDATA[white]]>\n</colList_col>\n<colList_col nr=\"4\">\n<![CDATA[]]>\n</colList_col>\n</colList_row>\n"
        
        # index at which the row count will start
        index = 2 * numberOfEntityLines + numberOfPotentialLines
        for i in range(numberOfMandatoryLines):
            # A loop to create the colors that will define how long since a mandatory activity was fired
            accumulator += "<colList_row nr=\"" + str(i + index) + "\">\n"
            accumulator += "<colList_col nr=\"1\">\n"
            accumulator += "<![CDATA[" + "beta" + str(i) + "]]>\n"
            accumulator += "</colList_col>\n<colList_col nr=\"1\">\n<![CDATA[int]]>\n</colList_col>\n<colList_col nr=\"2\">\n"
            accumulator += "<![CDATA[0-" + str(self.figuringDOut(potentialDefinition, mandatoryDefinition)) + "]]>\n"
            accumulator += "</colList_col>\n<colList_col nr=\"3\">\n<![CDATA[white]]>\n</colList_col>\n<colList_col nr=\"4\">\n<![CDATA[]]>\n</colList_col>\n</colList_row>\n"
        
        # We need A color of size D so that we can create the lambda for all the entites
        accumulator += "<colList_row nr=\"" + str(numberOfColours - 1) + "\">\n"
        accumulator += "<colList_col nr=\"1\">\n"
        accumulator += "<![CDATA[D]]>\n"
        accumulator += "</colList_col>\n<colList_col nr=\"1\">\n<![CDATA[int]]>\n</colList_col>\n<colList_col nr=\"2\">\n"
        accumulator += "<![CDATA[0-" + str(self.figuringDOut(potentialDefinition, mandatoryDefinition)) + "]]>\n"
        accumulator += "</colList_col>\n<colList_col nr=\"3\">\n<![CDATA[white]]>\n</colList_col>\n<colList_col nr=\"4\">\n<![CDATA[]]>\n</colList_col>\n</colList_row>\n"
        
        endString = "</colList_body>\n</colList>\n<graphics count=\"0\"/>\n</attribute>\n<graphics count=\"0\"/>\n</metadata>\n</metadataclass>\n"
        return startString + accumulator + endString
    
    def createCompoundCOlorSet(self, entityDefinition):
        """
        Creates all the compound color set using the simple color set for the petri net
        """
        print("Hello World")
        return 1
    
    def makeText(self, entityDefinition, potentialDefinition, mandatoryDefinition):
        # the string that contains all the unchanging data when creating the simple color sets
        startStringSimpleColor = "<metadataclass count=\"1\" name=\"Basic Colorset Class\">\n<metadata id=\"7035\" net=\"1\">\n<attribute name=\"Name\" id=\"7036\" net=\"1\">\n<![CDATA[NewColorset]]>\n<graphics count=\"0\"/>\n</attribute>\n<attribute name=\"ID\" id=\"7037\" net=\"1\">\n<![CDATA[0]]>\n<graphics count=\"0\"/>\n</attribute>\n<attribute name=\"Comment\" id=\"7038\" net=\"1\">\n<![CDATA[]]>\n<graphics count=\"0\"/>\n</attribute>\n"
        return startStringSimpleColor + self.createSimpleColorSet(entityDefinition, potentialDefinition, mandatoryDefinition)