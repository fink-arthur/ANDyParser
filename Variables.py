# coding=utf-8

class Variables:
    """
    This class will generate all the text in the correct "snoopy" format to create
    all the variables that will be used by the petri net
    """

    def __init__(self, entityDefinition, potentialDefinition, mandatoryDefinition):
        self.entityDefinition = entityDefinition
        self.potentialDefinition = potentialDefinition
        self.mandatoryDefinition = mandatoryDefinition
    
    def creatingEntityVariable(self, numberOfVariables):
        """
        Creates all the variables for the entities (i.e. <le,ue,lambdae> where e is an entity)
        """
        numberOfEntityLines = self.entityDefinition.rstrip().lstrip().count("\n") + 1
        lines = self.entityDefinition.rstrip().lstrip().split("\n")
        startString = "<attribute name=\"VariableList\" type=\"ColList\" id=\"11973\" net=\"1\">\n<colList row_count=\"" + str(numberOfVariables) + "\" col_count=\"3\" active_row=\"0\" active_col=\"0\">\n<colList_head>\n<colList_colLabel>\n<![CDATA[]]>\n</colList_colLabel>\n<colList_colLabel>\n<![CDATA[]]>\n</colList_colLabel>\n<colList_colLabel>\n<![CDATA[]]>\n</colList_colLabel>\n</colList_head>\n<colList_body>\n"
        accumulator = ""
        
        for i in range(numberOfEntityLines):
            # A loop to create all the variables that will define at which level the entity is
            splittedLine = lines[i].split(":")
            entityName = splittedLine[0].rstrip().lstrip()
            accumulator += "<colList_row nr=\"" + str(i) + "\">\n"
            accumulator += "<colList_col nr=\"0\">\n"
            accumulator += "<![CDATA[" + "level" + entityName + "]]>\n"
            accumulator += "</colList_col>\n<colList_col nr=\"1\">\n"
            accumulator += "<![CDATA[" + "l" + entityName +  "]]>\n"
            accumulator += "</colList_col>\n<colList_col nr=\"2\">\n<![CDATA[]]>\n</colList_col>\n</colList_row>\n"
        
        for i in range(numberOfEntityLines):
            # A loop to create all the variables that will define the timer that counts how long ago the last update was
            splittedLine = lines[i].split(":")
            entityName = splittedLine[0].rstrip().lstrip()
            accumulator += "<colList_row nr=\"" + str(i + numberOfEntityLines) + "\">\n"
            accumulator += "<colList_col nr=\"0\">\n"
            accumulator += "<![CDATA[" + "timer" + entityName + "]]>\n"
            accumulator += "</colList_col>\n<colList_col nr=\"1\">\n"
            accumulator += "<![CDATA[" + "u" + entityName +  "]]>\n"
            accumulator += "</colList_col>\n<colList_col nr=\"2\">\n<![CDATA[]]>\n</colList_col>\n</colList_row>\n"
            
        startIndex = 2 * numberOfEntityLines
        for i in range(numberOfEntityLines):
            # A loop to create all the variables that will define the vector which will store all the timers
            splittedLine = lines[i].split(":")
            entityName = splittedLine[0].rstrip().lstrip()
            accumulator += "<colList_row nr=\"" + str(i + startIndex) + "\">\n"
            accumulator += "<colList_col nr=\"0\">\n"
            accumulator += "<![CDATA[" + "lbd" + entityName + "]]>\n"
            accumulator += "</colList_col>\n<colList_col nr=\"1\">\n"
            accumulator += "<![CDATA[" + "lambda" + entityName +  "]]>\n"
            accumulator += "</colList_col>\n<colList_col nr=\"2\">\n<![CDATA[]]>\n</colList_col>\n</colList_row>\n"
        
        return startString + accumulator
    
    def creatingActivityVariable(self, numberOfEntities):
        """
        Creates all the variables for the activities (a timer for each potential and mandatory activity)
        """
        numberOfPotentialLines = self.potentialDefinition.rstrip().lstrip().count("\n") + 1
        numberOfMandatoryLines = self.mandatoryDefinition.rstrip().lstrip().count("\n") + 1
        accumulator = ""
        
        for i in range(numberOfPotentialLines):
            # A loop to create all the variables that will store when an update was done on a potential activity
            accumulator += "<colList_row nr=\"" + str(i + numberOfEntities) + "\">\n"
            accumulator += "<colList_col nr=\"0\">\n"
            accumulator += "<![CDATA[" + "ptalpha" + str(i) + "]]>\n"
            accumulator += "</colList_col>\n<colList_col nr=\"1\">\n"
            accumulator += "<![CDATA[" + "D" + "]]>\n"
            accumulator += "</colList_col>\n<colList_col nr=\"2\">\n<![CDATA[]]>\n</colList_col>\n</colList_row>\n"
            
        startIndex = numberOfEntities + numberOfPotentialLines
        for i in range(numberOfMandatoryLines):
            # A loop to create all the variables that will store when an update was done on a mandatory activity
            accumulator += "<colList_row nr=\"" + str(i + startIndex) + "\">\n"
            accumulator += "<colList_col nr=\"0\">\n"
            accumulator += "<![CDATA[" + "ptbeta" + str(i) + "]]>\n"
            accumulator += "</colList_col>\n<colList_col nr=\"1\">\n"
            accumulator += "<![CDATA[" + "D" + "]]>\n"
            accumulator += "</colList_col>\n<colList_col nr=\"2\">\n<![CDATA[]]>\n</colList_col>\n</colList_row>\n"
        
        endString =  "</colList_body>\n</colList>\n<graphics count=\"0\"/>\n</attribute>\n<graphics count=\"0\"/>\n</metadata>\n</metadataclass>\n"
        return accumulator + endString
    
    def makeText(self):
        """
        Returns the text generated in the "snoopy" format for all the definitions of the variables (entities + activities)
        """
        # numberOfVariables = 3 * numberOfEntities + numberOfPotential + numberOfMandatory
        numberOfVariables = (self.entityDefinition.rstrip().lstrip().count("\n") + 1) * 3 + (self.potentialDefinition.rstrip().lstrip().count("\n") + 1) + (self.mandatoryDefinition.rstrip().lstrip().count("\n") + 1)
        startVariable = "<metadataclass count=\"1\" name=\"Variable Class\">\n<metadata id=\"11969\" net=\"1\">\n<attribute name=\"Name\" id=\"11970\" net=\"1\">\n<![CDATA[NewVariable]]>\n<graphics count=\"0\"/>\n</attribute>\n<attribute name=\"ID\" id=\"11971\" net=\"1\">\n<![CDATA[0]]>\n<graphics count=\"0\"/>\n</attribute>\n<attribute name=\"Comment\" id=\"11972\" net=\"1\">\n<![CDATA[]]>\n<graphics count=\"0\"/>\n</attribute>\n"
        return startVariable + self.creatingEntityVariable(numberOfVariables) + self.creatingActivityVariable((self.entityDefinition.rstrip().lstrip().count("\n") + 1) * 3)