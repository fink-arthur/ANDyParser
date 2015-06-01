# coding=utf-8

class Variables:
    """
    This class will generate all the text in the correct "snoopy" format to initialize
    all the variables that will be used by the petri net
    """
    
    def creatingEntityVariable(self, entityDefinition, numberOfVariables):
        numberOfEntityLines = entityDefinition.rstrip().lstrip().count("\n") + 1
        lines = entityDefinition.rstrip().lstrip().split("\n")
        startString = "<attribute name=\"VariableList\" type=\"ColList\" id=\"11973\" net=\"1\">\n<colList row_count=\"" + str(numberOfVariables) + "\" col_count=\"3\" active_row=\"0\" active_col=\"0\">\n<colList_head>\n<colList_colLabel>\n<![CDATA[]]>\n</colList_colLabel>\n<colList_colLabel>\n<![CDATA[]]>\n</colList_colLabel>\n<colList_colLabel>\n<![CDATA[]]>\n</colList_colLabel>\n</colList_head>\n<colList_body>\n"
        accumulator = ""
        
        for i in range(numberOfEntityLines):
            splittedLine = lines[i].split(":")
            entityName = splittedLine[0].rstrip().lstrip()
            accumulator += "<colList_row nr=\"" + str(i) + "\">\n"
            accumulator += "<colList_col nr=\"0\">\n"
            accumulator += "<![CDATA[" + "level" + entityName + "]]>\n"
            accumulator += "</colList_col>\n<colList_col nr=\"1\">\n"
            accumulator += "<![CDATA[" + "l" + entityName +  "]]>\n"
            accumulator += "</colList_col>\n<colList_col nr=\"2\">\n\n<![CDATA[]]>\n</colList_col>\n</colList_row>\n"
        
        for i in range(numberOfEntityLines):
            splittedLine = lines[i].split(":")
            entityName = splittedLine[0].rstrip().lstrip()
            accumulator += "<colList_row nr=\"" + str(i + numberOfEntityLines) + "\">\n"
            accumulator += "<colList_col nr=\"0\">\n"
            accumulator += "<![CDATA[" + "timer" + entityName + "]]>\n"
            accumulator += "</colList_col>\n<colList_col nr=\"1\">\n"
            accumulator += "<![CDATA[" + "u" + entityName +  "]]>\n"
            accumulator += "</colList_col>\n<colList_col nr=\"2\">\n\n<![CDATA[]]>\n</colList_col>\n</colList_row>\n"
            
        for i in range(numberOfEntityLines):
            splittedLine = lines[i].split(":")
            entityName = splittedLine[0].rstrip().lstrip()
            accumulator += "<colList_row nr=\"" + str(i + 2* numberOfEntityLines) + "\">\n"
            accumulator += "<colList_col nr=\"0\">\n"
            accumulator += "<![CDATA[" + "lbd" + entityName + "]]>\n"
            accumulator += "</colList_col>\n<colList_col nr=\"1\">\n"
            accumulator += "<![CDATA[" + "lambda" + entityName +  "]]>\n"
            accumulator += "</colList_col>\n<colList_col nr=\"2\">\n\n<![CDATA[]]>\n</colList_col>\n</colList_row>\n"
        
        return startString + accumulator
    
    def creatingActivityVariable(self, potentialDefinition, mandatoryDefinition, numberOfEntities):
        numberOfPotentialLines = potentialDefinition.rstrip().lstrip().count("\n") + 1
        numberOfMandatoryLines = mandatoryDefinition.rstrip().lstrip().count("\n") + 1
        accumulator = ""
        
        for i in range(numberOfPotentialLines):
            accumulator += "<colList_row nr=\"" + str(i + numberOfEntities) + "\">\n"
            accumulator += "<colList_col nr=\"0\">\n"
            accumulator += "<![CDATA[" + "ptalpha" + str(i) + "]]>\n"
            accumulator += "</colList_col>\n<colList_col nr=\"1\">\n"
            accumulator += "<![CDATA[" + "D" + "]]>\n"
            accumulator += "</colList_col>\n<colList_col nr=\"2\">\n\n<![CDATA[]]>\n</colList_col>\n</colList_row>\n"
            
        for i in range(numberOfMandatoryLines):
            accumulator += "<colList_row nr=\"" + str(i + numberOfEntities + numberOfPotentialLines) + "\">\n"
            accumulator += "<colList_col nr=\"0\">\n"
            accumulator += "<![CDATA[" + "ptbeta" + str(i) + "]]>\n"
            accumulator += "</colList_col>\n<colList_col nr=\"1\">\n"
            accumulator += "<![CDATA[" + "D" + "]]>\n"
            accumulator += "</colList_col>\n<colList_col nr=\"2\">\n\n<![CDATA[]]>\n</colList_col>\n</colList_row>\n"
        
        endString =  "</colList_body>\n</colList>\n<graphics count=\"0\"/>\n</attribute>\n<graphics count=\"0\"/>\n</metadata>\n</metadataclass>\n"
        return accumulator + endString
    
    def makeText(self, entityDefinition, potentialDefinition, mandatoryDefinition):
        numberOfVariables = (entityDefinition.rstrip().lstrip().count("\n") + 1) * 3 + (potentialDefinition.rstrip().lstrip().count("\n") + 1) + (mandatoryDefinition.rstrip().lstrip().count("\n") + 1)
        startVariable = "<metadataclass count=\"1\" name=\"Variable Class\">\n<metadata id=\"11969\" net=\"1\">\n<attribute name=\"Name\" id=\"11970\" net=\"1\">\n<![CDATA[NewVariable]]>\n<graphics count=\"0\"/>\n</attribute>\n<attribute name=\"ID\" id=\"11971\" net=\"1\">\n<![CDATA[0]]>\n<graphics count=\"0\"/>\n</attribute>\n<attribute name=\"Comment\" id=\"11972\" net=\"1\">\n<![CDATA[]]>\n<graphics count=\"0\"/>\n</attribute>\n"
        return startVariable + self.creatingEntityVariable(entityDefinition, numberOfVariables) + self.creatingActivityVariable(potentialDefinition, mandatoryDefinition, (entityDefinition.rstrip().lstrip().count("\n") + 1) * 3)