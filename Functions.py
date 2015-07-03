class Functions:
    """
    This class will generate all the text in the correct xml format to initialize
    all the functions that will be used by the petri net
    """
    
    def __init__(self, entityDefinition, potentialDefinition, mandatoryDefinition):
        self.entityDefinition = entityDefinition
        self.potentialDefinition = potentialDefinition
        self.mandatoryDefinition = mandatoryDefinition
        
    def makeFunction(self, rowNumber, returnType, name, attributes, functionDefinition):
        accumulator = ""
        accumulator += "<colList_row nr=\"" + str(rowNumber) + "\">\n<colList_col nr=\"0\">\n"
        accumulator += "<![CDATA[" + returnType + "]]>\n</colList_col>\n<colList_col nr=\"1\">\n<![CDATA[" + name + "]]>\n"
        accumulator += "</colList_col>\n<colList_col nr=\"2\">\n<![CDATA[" + attributes + "]]>\n</colList_col>\n"
        accumulator += "<colList_col nr=\"3\">\n<![CDATA[" + functionDefinition + "]]>\n"
        accumulator += "</colList_col>\n<colList_col nr=\"4\">\n<![CDATA[]]>\n</colList_col>\n<colList_col nr=\"5\">\n<![CDATA[]]>\n</colList_col>\n</colList_row>\n"
        return accumulator
    
    def makeDecayLevelFunctionDefinition(self, entityDefintion):
        accumulator = ""
        splittedDefinition = entityDefintion.split(":")
        splittedLevel = splittedDefinition[1].rstrip().lstrip()[1:-1].split(",")
        accumulator += "[l=0]0"
        for i in range(1,len(splittedLevel)):
            accumulator += "++[l=" + str(i) + "]([u>=" + str(splittedLevel[i]) + "]" + str(i-1) + "++[u<" + str(splittedLevel[i]) + "]" + str(i) + ")"
        return accumulator
    
    def makeDecayTimerFunctionDefinition(self, entityDefintion):
        accumulator = ""
        splittedDefinition = entityDefintion.split(":")
        splittedLevel = splittedDefinition[1].rstrip().lstrip()[1:-1].split(",")
        accumulator += "[l=0]u+1"
        for i in range(1,len(splittedLevel)):
            accumulator += "++[l=" + str(i) + "]([u>=" + str(splittedLevel[i]) + "]u+1++[u<" + str(splittedLevel[i]) + "]0)"
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
    
    def makeMaxFunctionDefintion(self, D):
        return "[level>=" + str(D) + "]" + str(D) + "++[level<" + str(D) + "]level"
    
    def makeText(self):
        startString = "<metadataclass count=\"1\" name=\"Function Class\">\n<metadata id=\"10156\" net=\"1\">\n<attribute name=\"Name\" id=\"10157\" net=\"1\">\n<![CDATA[NewFunction]]>\n<graphics count=\"0\"/>\n</attribute>\n<attribute name=\"ID\" id=\"10158\" net=\"1\">\n<![CDATA[0]]>\n<graphics count=\"0\"/>\n"
        startString += "</attribute>\n<attribute name=\"Comment\" id=\"10159\" net=\"1\">\n<![CDATA[]]>\n<graphics count=\"0\"/>\n</attribute>\n<attribute name=\"FunctionList\" type=\"ColList\" id=\"10160\" net=\"1\">\n<colList row_count=\"0\" col_count=\"6\" active_row=\"0\" active_col=\"0\">\n<colList_head>\n<colList_colLabel>\n"
        startString += "<![CDATA[]]>\n</colList_colLabel>\n<colList_colLabel>\n<![CDATA[]]>\n</colList_colLabel>\n<colList_colLabel>\n<![CDATA[]]>\n</colList_colLabel>\n<colList_colLabel>\n<![CDATA[]]>\n</colList_colLabel>\n<colList_colLabel>\n<![CDATA[]]>\n</colList_colLabel>\n<colList_colLabel>\n<![CDATA[]]>\n</colList_colLabel>\n</colList_head>\n<colList_body>"
        endString = "</colList_body>\n</colList>\n<graphics count=\"0\"/>\n</attribute>\n<graphics count=\"0\"/>\n</metadata>\n</metadataclass>\n</metadataclasses>\n</Snoopy>"
        
        accumulator = ""
        #accumulator += self.makeFunction(1, "int", "maxD", "int level", self.makeMaxFunctionDefintion(self.figuringDOut()))
        
        return startString + accumulator + endString