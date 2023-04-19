import argparse
import xml.etree.ElementTree as xml
import sys
noArg = ["POPFRAME","PUSHFRAME","RETURN","CREATEFRAME"]  # todo
oneArg = ["DEFVAR", "CALL", "PUSHS", "POPS", "WRITE","LABEL","JUMP","EXIT","CALL","DPRINT","BREAK"]
twoArg = ["MOVE","READ","INT2CHAR","TYPE","NOT","STRLEN"]
threeArg = ["JUMPIFEQ","JUMPIFNEQ","ADD","SUB","MUL","IDIV","STRI2INT","LT","GT","EQ","AND","OR","CONCAT","GETCHAR","SETCHAR"]
symbols = ["STRING","INT","BOOL","NIL"]
validTags = ["instruction","arg1","arg2","arg3"]
validTags1 = ["instruction","arg1"]
validTags2 = ["instruction","arg1","arg2"]
knownInstructions = ["SETCHAR","GETCHAR","STRLEN","CONCAT","AND","OR","NOT","LT","GT","EQ","TYPE","CREATEFRAME","POPFRAME","PUSHFRAME","RETURN","DEFVAR", "CALL", "PUSHS", "POPS", "WRITE","LABEL","JUMP","EXIT","CALL","DPRINT","BREAK","MOVE","READ","INT2CHAR","JUMPIFEQ","JUMPIFNEQ","ADD","SUB","MUL","IDIV","STRI2INT"]

class dataStack():
    def __init__(self):
        self.vars = []
    def pushVal(self,type,value):
        self.vars.append(stackValue(value,type))
    def popVal(self):
        try:
            return self.vars.pop()
        except:
            exit(56)

class stackValue():
    def __init__(self,value,type):
        self.value = value
        self.type = type
    def getType(self):
        return self.type
    def getValue(self):
        return self.value

class labelList():
    def __init__(self):
        self.labels = []
    def addLabel(self,name,instruction,position):
        defined = False
        for labela in self.labels:
            if labela.getName() == name and labela.getInstruction() == instruction:
                defined = True
            elif labela.getName() == name and labela.getInstruction() != instruction:
                exit(52)
        if defined == False:
            self.labels.append(label(name,instruction,position))

    def getLabel(self,name):
        for label in self.labels:
            if label.getName() == name:
                return label.getPosition()
        exit(52)

class label():
    def __init__(self,name,instruction,position):
        self.name = name
        self.instruction = instruction
        self.position = int(position)
        self.called = 0
    def getName(self):
        return self.name
    def getInstruction(self):
        return self.instruction
    def getPosition(self):
        if self.called >250:
            exit(99)  #TODO obmedzenie call error
        self.called = self.called+1
        return self.position

class frameStack:
    def __init__(self):
        self.stack = []

    def pushFrame(self, frameToPush):
        self.stack.append(frameToPush)

    def popFrame(self):
        try:
            return self.stack.pop()
        except:
            exit(55)

    def getLF(self):
        try:
            return self.stack[-1]
        except:
            exit(56)

class frame:
    def __init__(self):
        self.LF = varList()

    def addVariable(self, name, value):
        self.LF.addVariable(name, value)

    def getVariable(self, name):
        return self.LF.getVariable(name)

    def setValueAndType(self, name, value, type):
        self.LF.setValueAndType(name, value, type)

class callStack:
    def __init__(self):
        self.stack = []
    def addPosition(self,position):
        self.stack.append(position)
    def popPosition(self):
        try:

            return self.stack.pop()

        except:
            exit(56)

class varList:
    accesable = True

    def __init__(self):
        self.vars = []

    def addVariable(self, name, value):
        for var in self.vars:
            if var.getName() == name:
                exit(52)
        self.vars.append(variable(name, value))

    def getVariable(self, name):
        if self.accesable:
            for tmp in self.vars:
                if tmp.name == name:
                    return tmp
            exit(54)
        else:
            exit(54)

    def getAllVariables(self):
        for variable in self.vars:
            print(variable.getName(), "= ", variable.getValue())

    def setAccesibility(self, accesable):
        self.accesable = accesable

    def setValueAndType(self, name, value, type):
        for var in self.vars:
            if var.getName() == name:
                var.setValueAndType(value, type)
                return
        exit(54)


class variable:
    def __init__(self, name, value):
        self.name = name
        self.value = ""
        self.type = ""

    def getName(self):
        return self.name

    def getValue(self):
        return self.value

    def getType(self):
        return self.type
    def setValueAndType(self, value, type):
        self.value = value
        self.type = type


class Instruction:
    def __init__(self, order, name, arguments, type):
        if arguments == "0":
            self.args = []
            self.order = order
            self.name = name
        else:
            self.order = order
            self.name = name
            self.args.append(argument(arguments, type))

    def addArg(self, type, name):
        self.args.append(argument(type, name))

    def getName(self):
        return self.name

    def getOrder(self):
        return self.order

    def getArg(self):
        return self.args
    def getArgNumber(self):
       return len(self.args)

    def printInstruction(self):
        print(self.order, self.name)

    def printArguments(self):
        for i in self.args:
            print(i.getType(), i.getValue())


class argument:
    def __init__(self, type, value):
        self.type = type
        self.value = value

    def getType(self):
        return self.type

    def getValue(self):
        return self.value


class InstructionsList:
    def __init__(self):
        self.instructions = []

    def addNewInsruction(self, instruct):
        if self.getInstructionAtOrd(order) == None:
            self.instructions.append(instruct)
        else:
            exit(32)

    def addInstriction(self, order, name, argument, type):
        if self.getInstructionAtOrd(order) == None:
            self.instructions.append(Instruction(order, name, arguments, type))
        else:
            exit(32)

    def printInstructions(self):
        for i in self.instructions:
            arg = i.getArg()
            print(i.getName(), ":")
            for a in arg:
                print(a.getType(), a.getValue())

    def getInstructionList(self):
        return self.instructions

    def getInstructionAtPosition(self,pos):
        return self.instructions[pos]
    def getInstructionAtOrd(self,ord):
        for instruction in self.instructions:
            if instruction.getOrder() == ord:
                return instruction
        return None
    def getInstructionMaxOrd(self):
        maxOrd = 0
        for instruction in self.instructions:
            newOrd = instruction.getOrder()
            if newOrd > maxOrd:
                maxOrd =newOrd
        return maxOrd
    def getInstructionsNumer(self):
        return len(self.instructions)

def getVarReference(type,name,GF,tmpFrame,frame_Stack,tmpArgumentReference):
    if type == "VAR":
        if "GF@" in name.upper():
            SerchedVarReference = GF.getVariable(name.replace('GF@', ''))
        elif "TF@" in name.upper():
            SerchedVarReference = tmpFrame.getVariable(tmpArgumentReference[0].getValue().replace('TF@', ''))
        elif "LF@" in name.upper():
            frameReference = frame_Stack.getLF()
            SerchedVarReference = frameReference.getVariable(name.replace('LF@', ''))
        else:
            SerchedVarReference = None
        return SerchedVarReference

def operations(operation,GF,tmpFrame,frame_Stack,tmpArgumentReference):
    firstValue = 0
    secondValue = 0
    if tmpArgumentReference[0].getType().upper() == "VAR":

        if tmpArgumentReference[1].getType().upper() == "INT" and tmpArgumentReference[2].getType().upper() == "INT":
            firstValue = tmpArgumentReference[1].getValue()
            secondValue = tmpArgumentReference[2].getValue()
        elif tmpArgumentReference[1].getType().upper() == "VAR" and tmpArgumentReference[2].getType().upper() == "VAR":
            firstVar = getVarReference(tmpArgumentReference[1].getType().upper(),tmpArgumentReference[1].getValue(), GF, tmpFrame, frame_Stack,tmpArgumentReference)
            secondVar = getVarReference(tmpArgumentReference[2].getType().upper(),tmpArgumentReference[2].getValue(), GF, tmpFrame, frame_Stack,tmpArgumentReference)

            if firstVar.getType().upper() == "INT" and secondVar.getType().upper() == "INT":
                firstValue = firstVar.getValue()
                secondValue = secondVar.getValue()
            else:
                exit(53)


        elif tmpArgumentReference[1].getType().upper() == "INT" and tmpArgumentReference[2].getType().upper() == "VAR":
            firstValue = tmpArgumentReference[1].getValue()
            secondVar = getVarReference(tmpArgumentReference[2].getType().upper(),
                                        tmpArgumentReference[2].getValue(), GF, tmpFrame, frame_Stack,tmpArgumentReference)
            if secondVar.getType().upper() == "INT":
                secondValue = secondVar.getValue()
            else:
                exit(53)

        elif tmpArgumentReference[1].getType().upper() == "VAR" and tmpArgumentReference[2].getType().upper() == "INT":
            secondValue = tmpArgumentReference[2].getValue()
            firstVar = getVarReference(tmpArgumentReference[1].getType().upper(),tmpArgumentReference[1].getValue(), GF, tmpFrame, frame_Stack,tmpArgumentReference)
            if firstVar.getType().upper() == "INT":
                firstValue = firstVar.getValue()
            else:
                exit(53)
        else:
            exit(53)
        try:
            firstValue = int(firstValue)
            secondValue = int(secondValue)
        except:
            exit(32)
        if secondValue != "" and firstValue != "":
            if operation == "ADD":
                return int(firstValue) + int(secondValue)
            if operation == "SUB":
                return int(firstValue) - int(secondValue)
            if operation == "MUL":
                return int(firstValue) * int(secondValue)
            if operation == "IDIV":
                if int(secondValue) != 0:
                    return int(int(firstValue) / int(secondValue))
                else:
                    exit(57)
        else:
            exit(56)

def sizeOperations(operation,GF,tmpFrame,frame_Stack,tmpArgumentReference):
    returnValue = False
    type1 = ""
    type2 = ""
    val1 = ""
    val2 = ""
    if tmpArgumentReference[1].getType().upper() == "VAR":
        tmpVarReference = getVarReference(tmpArgumentReference[1].getType().upper(),tmpArgumentReference[1].getValue(),GF,tmpFrame,frame_Stack,tmpArgumentReference)
        type1 = tmpVarReference.getType()
        val1 = tmpVarReference.getValue()

    if tmpArgumentReference[1].getType().upper() in symbols:
        type1 = tmpArgumentReference[1].getType()
        val1 = tmpArgumentReference[1].getValue()

    if tmpArgumentReference[1].getType().upper() in symbols:
        type2 = tmpArgumentReference[1].getType()
        val2 = tmpArgumentReference[1].getValue()

    if tmpArgumentReference[2].getType().upper() == "VAR":
        tmpVarReference = getVarReference(tmpArgumentReference[2].getType().upper(),tmpArgumentReference[2].getValue(),GF,tmpFrame,frame_Stack,tmpArgumentReference)
        type2 = tmpVarReference.getType()
        val2 = tmpVarReference.getValue()



    if type1 == type2:
        if type1.upper() == "INT":
            try:
                val1 = int(val1)
                val2 = int(val2)
            except:
                exit(32)
            if operation == "LT":
                if val1 < val2:
                    returnValue="true"
                else:
                    returnValue = "false"
            if operation == "GT":
                if val1 > val2:
                    returnValue="true"
                else:
                    returnValue = "false"
            if operation == "EQ":
                if val1 == val2:
                    returnValue= "true"
                else:
                    returnValue = "false"

        if type1.upper() == "STRING":
            if operation == "LT":
                if str(val1) < str(val2):
                    returnValue= "true"
                else:
                    returnValue = "false"
            if operation == "GT":
                if str(val1) > str(val2):
                    returnValue= "true"
                else:
                    returnValue = "false"
            if operation == "EQ":
                if str(val1) == str(val2):
                    returnValue= "true"
                else:
                    returnValue = "false"

        if type1.upper() == "BOOL":
            if str(val1).upper() == "TRUE":
                val1 = 1
            else:
                val1 = 0
            if str(val1).upper() == "TRUE":
                val2 = 1
            else:
                val2 = 0
            if operation == "LT":
                if int(val1) < int(val2):
                    returnValue = "true"
                else:
                    returnValue = "false"
            if operation == "GT":
                if int(val1) > int(val2):
                    returnValue = "true"
                else:
                    returnValue = "false"
            if operation == "EQ":
                if int(val1) == int(val2):
                    returnValue = "true"
                else:
                    returnValue = "false"

        if type1.upper() == "NIL":

            if operation == "EQ":
                if val1 == val2:
                    returnValue= "true"
                else:
                    returnValue = "false"
            else:
                exit(53)
        return returnValue
    else:
        exit(53)

def subStringConverter(string):
    toConvert = []
    startToConvert=0
    if isinstance(string,str):
        for char in string:
            if char == "\\":
                toConvert.append(string[startToConvert:startToConvert+4])
            startToConvert=startToConvert+1
        for replacingString in toConvert:
            stringToConvert = replacingString[1:]
            string=string.replace(replacingString,chr(int(stringToConvert)))
        return string
    else:
        return string

def getSymbolValue(pos,GF,tmpFrame,frame_Stack,tmpArgumentReference):
    returnValue = ""
    if tmpArgumentReference[pos].getType().upper() == "VAR":
        varRef = getVarReference(tmpArgumentReference[pos].getType().upper(),tmpArgumentReference[pos].getValue(),GF,tmpFrame,frame_Stack,tmpArgumentReference)
        returnValue = varRef.getValue()
    elif tmpArgumentReference[pos].getType().upper() in symbols:
        returnValue = tmpArgumentReference[pos].getValue()
    else:
        exit(53)
    return returnValue

def getSymbolType(pos,GF,tmpFrame,frame_Stack,tmpArgumentReference):
    returnValue = ""
    if tmpArgumentReference[pos].getType().upper() == "VAR":
        varRef = getVarReference(tmpArgumentReference[pos].getType().upper(),tmpArgumentReference[pos].getValue(),GF,tmpFrame,frame_Stack,tmpArgumentReference)
        returnValue = varRef.getType().upper()
    elif tmpArgumentReference[pos].getType().upper() in symbols:
        returnValue = tmpArgumentReference[pos].getType().upper()
    else:
        exit(53)
    return returnValue






# //////////////////////////////////////////////////////////////////

ap = argparse.ArgumentParser()
ap.add_argument('--source', nargs=1, help="vstupný súbor s XML reprezentáciou zdrojového kódu ")
ap.add_argument('--input', nargs=1, help="súbor so vstupmy pre samostatnú interpretáciu zadaného zdrojového kódu")
args = ap.parse_args()
root = None
labelList = labelList()
callStack = callStack()
dataStack = dataStack()
inputFile = None
if args.input is None and args.source is None:
    exit(10)
if args.input is not None:
    try:
        inputFile = open(args.input[0])
    except:
        exit(11)
if args.source is not None:
    try:
        tree = xml.parse(args.source[0])
        root = tree.getroot()
        if root.tag != "program":
            exit(32)
        if (root.attrib.get('language') != "IPPcode22"):
            exit(32)
    except xml.ParseError:
        exit(31)
else:
    loaded = []
    while True:
        line = (input())
        if not line:
            break
        loaded.append(line)
    root = xml.fromstringlist(loaded)
    if (root.attrib.get('language') != "IPPcode22"):
        print("NOIPP22")
GF = varList()
totalInstructionsDone = 0
tmpFrame = None
frame_Stack = frameStack()
instructions = InstructionsList()
for instruction in root:
    name = instruction.attrib.get('opcode')
    order = instruction.attrib.get('order')
    if name == None or order ==None:
        exit(32)
    if name.upper() not in knownInstructions:
        exit(32)
    try:
        order = int(order)
    except:
        exit(32)
    if order <= 0:
        exit(32)
    for arg in instruction.iter():
        if arg.tag in validTags:
            pass
        else:
            exit(32)
    if name.upper() in oneArg:
        instructionTmp = Instruction(order, name, "0", "0")
        controlValue = 0
        for tag in instruction.iter():
            if tag.tag not in validTags1:
                exit(32)
        for arg in instruction.iter('arg1'):
            if controlValue <=0:
                type = arg.attrib.get('type')
                arguments = arg.text
                instructionTmp.addArg(type, arguments)
                controlValue = controlValue + 1
            else:
                exit(32)
        if instructionTmp.getArgNumber() == 1 :
            instructions.addNewInsruction(instructionTmp)
        else:
            exit(32)

    elif name.upper() in twoArg:
        for tag in instruction.iter():
            if tag.tag not in validTags2:
                exit(32)
        instructionTmp = Instruction(order, name, "0", "0")
        controlValue = 0
        for arg in instruction.iter('arg1'):
            if controlValue <=0:
                type = arg.attrib.get('type')
                arguments = arg.text
                instructionTmp.addArg(type, arguments)
                controlValue= controlValue + 1
            else:
                exit(32)

        controlValue = 0
        for arg in instruction.iter('arg2'):
            if controlValue <= 0:
                type = arg.attrib.get('type')
                arguments = arg.text
                instructionTmp.addArg(type, arguments)
                controlValue = controlValue + 1
            else:
                exit(32)
        if instructionTmp.getArgNumber() == 2 :
            instructions.addNewInsruction(instructionTmp)
        else:
            exit(32)

    elif name.upper() in threeArg:
        controlValue = 0
        instructionTmp = Instruction(order, name, "0", "0")
        for arg in instruction.iter('arg1'):
            if controlValue <= 0:
                type = arg.attrib.get('type')
                arguments = arg.text
                instructionTmp.addArg(type, arguments)
                controlValue = controlValue + 1
                if type is None or arguments is None:
                    exit(32)
            else:
                exit(32)
        controlValue = 0
        for arg in instruction.iter('arg2'):
            if controlValue <= 0:
                type = arg.attrib.get('type')
                arguments = arg.text
                instructionTmp.addArg(type, arguments)
                controlValue = controlValue + 1
                if type is None or arguments is None:
                    exit(32)
            else:
                exit(32)
        controlValue = 0
        for arg in instruction.iter('arg3'):
            if controlValue <=0:
                type = arg.attrib.get('type')
                arguments = arg.text
                instructionTmp.addArg(type, arguments)
                controlValue = controlValue + 1
                if type is None or arguments is None:
                    exit(32)
            else:
                exit(32)
        if instructionTmp.getArgNumber() == 3 :
            instructions.addNewInsruction(instructionTmp)
        else:
            exit(32)
    elif name.upper() in noArg:
        instructionTmp = Instruction(order, name, "0", "0")
        instructions.addNewInsruction(instructionTmp)

# interpreting
instructionOrder=0
while instructionOrder <= instructions.getInstructionMaxOrd():
    loadedInstruction = instructions.getInstructionAtOrd(instructionOrder)
    if loadedInstruction != None:
        if loadedInstruction.getName().upper() == "LABEL":
            tmpArgumentReference = loadedInstruction.getArg()
            if tmpArgumentReference[0].getType().upper() == "LABEL":
                labelList.addLabel(tmpArgumentReference[0].getValue(), loadedInstruction, instructionOrder)
            totalInstructionsDone = totalInstructionsDone + 1
    instructionOrder= instructionOrder + 1
instructionOrder=0

while instructionOrder <= instructions.getInstructionMaxOrd():
    loadedInstruction=instructions.getInstructionAtOrd(instructionOrder)
    if loadedInstruction != None:
        if loadedInstruction.getName().upper() == "DEFVAR":
            tmpArgumentReference = loadedInstruction.getArg()
            if tmpArgumentReference[0].getType().upper() == "VAR" and "GF@" in tmpArgumentReference[0].getValue().upper():
                GF.addVariable(tmpArgumentReference[0].getValue().replace('GF@', ''), "")
                # to do pre lf a tf
            elif tmpArgumentReference[0].getType().upper() == "VAR" and "LF@" in tmpArgumentReference[0].getValue().upper():
                LF = frame_Stack.getLF()
                LF.addVariable(tmpArgumentReference[0].getValue().replace('LF@', ''), "")

            elif tmpArgumentReference[0].getType().upper() == "VAR" and "TF@" in tmpArgumentReference[0].getValue().upper():
                if tmpFrame is not None:
                    tmpFrame.addVariable(tmpArgumentReference[0].getValue().replace('TF@', ''), "")
                else:
                    exit(55)
            else:
                exit(52)
            totalInstructionsDone = totalInstructionsDone + 1



        if loadedInstruction.getName().upper() == "MOVE":
            tmpArgumentReference = loadedInstruction.getArg()
            if tmpArgumentReference[0].getType().upper() == "VAR" and tmpArgumentReference[1].getType().upper != "VAR":
                if "GF@" in tmpArgumentReference[0].getValue().upper():
                    GF.setValueAndType(tmpArgumentReference[0].getValue().replace('GF@', ''),
                                       tmpArgumentReference[1].getValue(), tmpArgumentReference[1].getType())
                # to do for lf tf use framelist
                if "LF@" in tmpArgumentReference[0].getValue().upper():
                    LF = frame_Stack.getLF()
                    LF.setValueAndType(tmpArgumentReference[0].getValue().replace('LF@', ''),
                                       tmpArgumentReference[1].getValue(), tmpArgumentReference[1].getType())

                if "TF@" in tmpArgumentReference[0].getValue().upper():
                    tmpFrame.setValueAndType(tmpArgumentReference[0].getValue().replace('TF@', ''),
                                             tmpArgumentReference[1].getValue(), tmpArgumentReference[1].getType())
            totalInstructionsDone = totalInstructionsDone + 1

        if loadedInstruction.getName().upper() == "WRITE":
            tmpArgumentReference = loadedInstruction.getArg()
            tmpVarReference=None
            printValue = None
            if tmpArgumentReference == None :
                exit(32)
            if tmpArgumentReference[0].getType().upper() == "VAR" :
                if "GF@" in tmpArgumentReference[0].getValue().upper():
                    tmpVarReference = GF.getVariable(tmpArgumentReference[0].getValue().replace('GF@', ''))
                    printValue = tmpVarReference.getValue()
                elif "TF@" in tmpArgumentReference[0].getValue().upper():
                    if tmpFrame != None:
                        tmpVarReference = tmpFrame.getVariable(tmpArgumentReference[0].getValue().replace('TF@', ''))
                        printValue = tmpVarReference.getValue()
                    else:
                        exit(55)
                elif "LF@" in tmpArgumentReference[0].getValue().upper():
                    tmpFrameReference = frame_Stack.getLF()
                    tmpVarReference = tmpFrameReference.getVariable(tmpArgumentReference[0].getValue().replace('LF@', ''))
                    printValue = tmpVarReference.getValue()
                else:
                    printValue = None
            elif tmpArgumentReference[0].getType().upper() in symbols:
                printValue = tmpArgumentReference[0].getValue()
            else:
                exit(32)
            if printValue is not None:
               printValue=subStringConverter(printValue)
               print(printValue,end='')
            else:
                exit(32)
            totalInstructionsDone = totalInstructionsDone + 1


        if loadedInstruction.getName().upper() == "CREATEFRAME":
            tmpFrame = frame()
            totalInstructionsDone = totalInstructionsDone + 1


        if loadedInstruction.getName().upper() == "PUSHFRAME":
            if tmpFrame is not None:
                frame_Stack.pushFrame(tmpFrame)
                tmpFrame = None
            else:
                exit(55)
            totalInstructionsDone = totalInstructionsDone + 1

        if loadedInstruction.getName().upper() == "POPFRAME":
            if frame_Stack is not None:
                tmpFrame = frame_Stack.popFrame()
            else:
                exit(55)
            totalInstructionsDone = totalInstructionsDone + 1

        if loadedInstruction.getName().upper() == "READ":
            inputValue = None
            inputType = None
            tmpArgumentReference = loadedInstruction.getArg()
            if tmpArgumentReference[0].getType().upper() == "VAR" :
                tmpVarReference=getVarReference(tmpArgumentReference[0].getType().upper(),tmpArgumentReference[0].getValue(),GF,tmpFrame,frame_Stack,tmpArgumentReference)
                if tmpVarReference is not None:
                    if inputFile == None:
                        inputValue = input()
                    else:
                        inputValue = inputFile.readline()
                    if tmpArgumentReference[1].getType().upper() == "TYPE":
                        if inputValue == "" or inputValue is None:
                            inputValue=""
                            inputType="NIL"
                        elif tmpArgumentReference[1].getValue().upper() == "INT":
                            try:
                                inputValue = int(inputValue)
                                inputType = "int"
                            except:
                                try:
                                    inputValue = int(inputValue,16)
                                    inputType = "int"
                                except:
                                    try:
                                        inputValue = int(inputValue, 8)
                                        inputType = "int"
                                    except:
                                        inputValue = ""
                                        inputType = "NIL"
                        elif tmpArgumentReference[1].getValue().upper() == "BOOL":
                            inputType = "bool"
                            if inputValue.upper() == "TRUE":
                                inputValue = "true"
                            else:
                                inputValue= "false"
                        elif tmpArgumentReference[1].getValue().upper() == "STRING":
                            inputValue=str(inputValue).replace("\n","")
                        else:
                            inputType="NIL"
                            inputValue="nil@nil"
                tmpVarReference.setValueAndType(inputValue,inputType)
            else:
                exit(53)  # nedefinovana var
            totalInstructionsDone = totalInstructionsDone + 1



        if loadedInstruction.getName().upper() == "JUMP":
            tmpArgumentReference = loadedInstruction.getArg()
            if tmpArgumentReference[0].getType().upper() == "LABEL":
                instructionOrder=labelList.getLabel(tmpArgumentReference[0].getValue())
            totalInstructionsDone = totalInstructionsDone + 1

        if loadedInstruction.getName().upper() == "JUMPIFEQ" or loadedInstruction.getName().upper() == "JUMPIFNEQ":
            if loadedInstruction.getName().upper() == "JUMPIFNEQ":
                neq = True
            else:
                neq = False
            tmpArgumentReference = loadedInstruction.getArg()
            arg1Value = ""
            arg2Value = ""
            arg1Type = ""
            arg2Type = ""
            if tmpArgumentReference[0].getType().upper() == "LABEL":
                if tmpArgumentReference[1].getType().upper() == "VAR":
                    arg1Var= getVarReference(tmpArgumentReference[1].getType().upper(),tmpArgumentReference[1].getValue(),GF,tmpFrame,frame_Stack,tmpArgumentReference)
                    arg1Value = arg1Var.getValue()
                    arg1Type = arg1Var.getType().upper()
                elif tmpArgumentReference[1].getType().upper() in symbols:
                    arg1Value = tmpArgumentReference[1].getValue()
                    arg1Type = tmpArgumentReference[1].getType().upper()
                else:
                    exit(52)
                if tmpArgumentReference[2].getType().upper() == "VAR":
                    arg2Var= getVarReference(tmpArgumentReference[2].getType().upper(),tmpArgumentReference[2].getValue(),GF,tmpFrame,frame_Stack,tmpArgumentReference)
                    arg2Value = arg2Var.getValue()
                    arg2Type = arg2Var.getType().upper()
                elif tmpArgumentReference[2].getType().upper() in symbols:
                    arg2Value = tmpArgumentReference[2].getValue()
                    arg2Type = tmpArgumentReference[2].getType().upper()
                else:
                    exit(52)
            else:
                exit(52)
            if not neq:
                if str(arg1Value) == str(arg2Value) or arg1Type == "NIL" or arg2Type == "NIL":
                    if arg1Type == arg2Type or arg1Type == "NIL" or arg2Type == "NIL":
                        instructionOrder = labelList.getLabel(tmpArgumentReference[0].getValue()) - 1
                    else:
                        exit(53)
            else:
                if str(arg1Value) != str(arg2Value) or arg1Type == "NIL" or arg2Type == "NIL":
                    if arg1Type == arg2Type or arg1Type == "NIL" or arg2Type == "NIL":
                        instructionOrder = labelList.getLabel(tmpArgumentReference[0].getValue()) - 1
                    else:
                        exit(53)
            totalInstructionsDone = totalInstructionsDone + 1

        if loadedInstruction.getName().upper() == "EXIT":
            tmpArgumentReference = loadedInstruction.getArg()
            if tmpArgumentReference[0].getType().upper() == "INT":
                    if 0 <= int(tmpArgumentReference[0].getValue()) <= 49:
                        exit(int(tmpArgumentReference[0].getValue()))
                    else:
                        exit(57)
            elif tmpArgumentReference[0].getType().upper() == "VAR":
                serchedVar = getVarReference(tmpArgumentReference[0].getType().upper(),tmpArgumentReference[0].getValue(),GF,tmpFrame,frame_Stack,tmpArgumentReference)
                typeOfVar = serchedVar.getType()
                exitCode = serchedVar.getValue()
                if exitCode == "":
                    exit(56)
                exitCode=int(exitCode)
                if 0 <= exitCode <= 49 and typeOfVar.upper() == "INT":
                    exit(exitCode)
                else:
                    exit(57)
            else:
                exit(57)
            totalInstructionsDone = totalInstructionsDone + 1


        if loadedInstruction.getName().upper() == "ADD" or \
                loadedInstruction.getName().upper() == "SUB" or \
                loadedInstruction.getName().upper() == "MUL"or \
                loadedInstruction.getName().upper() == "IDIV":

            tmpArgumentReference = loadedInstruction.getArg()
            finalVarReference = getVarReference(tmpArgumentReference[0].getType().upper(),tmpArgumentReference[0].getValue(),GF,tmpFrame,frame_Stack,tmpArgumentReference)

            if loadedInstruction.getName().upper() == "ADD":
                returnValue = operations("ADD",GF,tmpFrame,frame_Stack,tmpArgumentReference)
            elif loadedInstruction.getName().upper() == "SUB":
                returnValue = operations("SUB",GF,tmpFrame,frame_Stack,tmpArgumentReference)
            elif loadedInstruction.getName().upper() == "MUL":
                returnValue = operations("MUL",GF,tmpFrame,frame_Stack,tmpArgumentReference)
            else:
                returnValue = operations("IDIV",GF,tmpFrame,frame_Stack,tmpArgumentReference)
            finalVarReference.setValueAndType(returnValue,"INT")
            totalInstructionsDone = totalInstructionsDone + 1

        if loadedInstruction.getName().upper() == "CALL":
            tmpArgumentReference = loadedInstruction.getArg()
            if tmpArgumentReference[0].getType().upper() == "LABEL":
                callStack.addPosition(instructionOrder)
                instructionOrder = labelList.getLabel(tmpArgumentReference[0].getValue()) - 1
            totalInstructionsDone = totalInstructionsDone + 1

        if loadedInstruction.getName().upper() == "RETURN":
            instructionOrder = callStack.popPosition()
            totalInstructionsDone = totalInstructionsDone + 1

        if loadedInstruction.getName().upper() == "INT2CHAR":
            returnValue=""
            tmpArgumentReference = loadedInstruction.getArg()
            if tmpArgumentReference[0].getType().upper() == "VAR":
                finalVar = getVarReference(tmpArgumentReference[0].getType().upper(),tmpArgumentReference[0].getValue(),GF,tmpFrame,frame_Stack,tmpArgumentReference)
                tmpArgumentReference = loadedInstruction.getArg()
                if tmpArgumentReference[1].getType().upper() == "INT":
                    try:
                        returnValue = chr(int(tmpArgumentReference[1].getValue()))
                    except:
                        exit(58)
                elif tmpArgumentReference[1].getType().upper() == "VAR":
                    tmpVarReference=getVarReference(tmpArgumentReference[1].getType().upper(),tmpArgumentReference[1].getValue(),GF,tmpFrame,frame_Stack,tmpArgumentReference)
                    if tmpVarReference.getType().upper() == "INT":
                        try:
                            returnValue = chr(int(tmpVarReference.getValue()))
                        except:
                            exit(58)
                    else:
                        exit(53)
                else:
                    exit(53)
                finalVar.setValueAndType(returnValue,"STRING")
                totalInstructionsDone = totalInstructionsDone + 1

        if loadedInstruction.getName().upper() == "DPRINT":
            tmpArgumentReference = loadedInstruction.getArg()
            dprintValue = ""
            if tmpArgumentReference[0].getType().upper() == "VAR":
                varRef = getVarReference(tmpArgumentReference[0].getType().upper(),tmpArgumentReference[0].getValue(),GF,tmpFrame,frame_Stack,tmpArgumentReference)
                dprintValue = str(varRef.getValue())
            elif tmpArgumentReference[0].getType().upper() in symbols:
                dprintValue = str(tmpArgumentReference[0].getValue())
            else:
                exit(53)
            sys.stderr.write(dprintValue+"\n")
            totalInstructionsDone = totalInstructionsDone + 1

        if loadedInstruction.getName().upper() == "BREAK":

            sys.stderr.write("Pocet vykonaných instrukcii: "+str(totalInstructionsDone)+"\n")
            totalInstructionsDone = totalInstructionsDone + 1

        if loadedInstruction.getName().upper() == "STRI2INT":
            returnValue = ""
            position = ""
            tmpArgumentReference = loadedInstruction.getArg()
            if tmpArgumentReference[0].getType().upper() == "VAR":
                finalVar = getVarReference(tmpArgumentReference[0].getType().upper(), tmpArgumentReference[0].getValue(),GF, tmpFrame, frame_Stack,tmpArgumentReference)
                tmpArgumentReference = loadedInstruction.getArg()
                if tmpArgumentReference[2].getType().upper() == "INT":
                    position = tmpArgumentReference[2].getValue()
                elif tmpArgumentReference[2].getType().upper() == "VAR":
                    tmpVarReferencePos = getVarReference(tmpArgumentReference[2].getType().upper(),tmpArgumentReference[2].getValue(),GF,tmpFrame,frame_Stack,tmpArgumentReference)
                    if tmpVarReferencePos.getType().upper() == "INT":
                        position = int(tmpVarReferencePos.getValue())
                else :
                    exit(52)
                if tmpArgumentReference[1].getType().upper() == "STRING":
                    try:
                        j=0
                        convertingValue = tmpArgumentReference[1].getValue()
                        if len(convertingValue)-1 >= int(position):
                            for character in convertingValue:
                                if j == int(position):
                                    returnValue = ord(character)
                                    break
                                j=j+1
                        else:
                            exit(58)
                    except:
                        exit(58)
                elif tmpArgumentReference[1].getType().upper() == "VAR":
                    tmpVarReference = getVarReference(tmpArgumentReference[1].getType().upper(),tmpArgumentReference[1].getValue(), GF, tmpFrame, frame_Stack,tmpArgumentReference)
                    if tmpVarReference.getType().upper() == "STRING":
                        try:
                            j=0
                            convertingValue = tmpVarReference.getValue()
                            if len(convertingValue)-1 >= position:
                                for character in convertingValue:
                                    if j == int(position):
                                        returnValue = ord(character)
                                        break
                                    j = j + 1
                            else:
                                exit(58)

                        except:
                            exit(58)
                    else:
                        exit(53)
                else:
                    exit(53)
                finalVar.setValueAndType(returnValue, "INT")
                totalInstructionsDone = totalInstructionsDone + 1

        if loadedInstruction.getName().upper() == "LT" or loadedInstruction.getName().upper() == "GT" or loadedInstruction.getName().upper() == "EQ":
            tmpArgumentReference = loadedInstruction.getArg()
            if tmpArgumentReference[0].getType().upper() == "VAR":
                returnValue = sizeOperations(loadedInstruction.getName().upper(),GF,tmpFrame,frame_Stack,tmpArgumentReference)
                varRef = getVarReference(tmpArgumentReference[0].getType().upper(), tmpArgumentReference[0].getValue(), GF,tmpFrame, frame_Stack, tmpArgumentReference)
                varRef.setValueAndType(returnValue,"BOOL")
            else:
                exit(53)
            totalInstructionsDone = totalInstructionsDone + 1

        if loadedInstruction.getName().upper() == "AND" or loadedInstruction.getName().upper() == "OR":
            operation = loadedInstruction.getName().upper()
            returnValue = ""
            val1 = ""
            val2 = ""
            type1 = ""
            type2 = ""
            tmpArgumentReference = loadedInstruction.getArg()

            if tmpArgumentReference[0].getType().upper() == "VAR":
                if tmpArgumentReference[1].getType().upper() == "VAR":
                    firstVarRef = getVarReference(tmpArgumentReference[1].getType().upper(),tmpArgumentReference[1].getValue(), GF, tmpFrame, frame_Stack,tmpArgumentReference)
                    type1 = firstVarRef.getType().upper()
                    val1 = firstVarRef.getValue()
                else:
                    type1 = tmpArgumentReference[1].getType().upper()
                    val1 = tmpArgumentReference[1].getValue()
                if tmpArgumentReference[2].getType().upper() == "VAR":
                    secondVarRef = getVarReference(tmpArgumentReference[2].getType().upper(),tmpArgumentReference[2].getValue(), GF, tmpFrame, frame_Stack,tmpArgumentReference)
                    type2 = secondVarRef.getType().upper()
                    val2 = secondVarRef.getValue()
                else:
                    type2 = tmpArgumentReference[2].getType().upper()
                    val2 = tmpArgumentReference[2].getValue()
                varRef = getVarReference(tmpArgumentReference[0].getType().upper(),tmpArgumentReference[0].getValue(), GF, tmpFrame, frame_Stack,tmpArgumentReference)
                if type1.upper() == "BOOL" and type2.upper() == "BOOL":
                    if operation == "AND":
                        if val1 == "true" and val2 == "true":
                            returnValue = "true"
                        else:
                            returnValue = "false"
                    if operation == "OR":
                        if val1 == "true" or val2 == "true":
                            returnValue = "true"
                        else:
                            returnValue = "false"
                    varRef.setValueAndType(returnValue,"BOOL")
                else:
                    exit(53)
                totalInstructionsDone = totalInstructionsDone + 1

        if loadedInstruction.getName().upper() == "NOT":
            operation = loadedInstruction.getName().upper()
            returnValue = ""
            val1 = ""
            type1 = ""
            tmpArgumentReference = loadedInstruction.getArg()
            if tmpArgumentReference[0].getType().upper() == "VAR":
                varRef = getVarReference(tmpArgumentReference[0].getType().upper(),tmpArgumentReference[0].getValue(), GF, tmpFrame, frame_Stack,tmpArgumentReference)
                if tmpArgumentReference[1].getType().upper() == "VAR":
                    firstVarRef = getVarReference(tmpArgumentReference[1].getType().upper(),tmpArgumentReference[1].getValue(), GF, tmpFrame, frame_Stack,tmpArgumentReference)
                    type1 = firstVarRef.getType().upper()
                    val1 = firstVarRef.getValue()
                else:
                    type1 = tmpArgumentReference[1].getType().upper()
                    val1 = tmpArgumentReference[1].getValue()
                if type1 == "BOOL" :
                    if val1 == "true":
                        returnValue = "false"
                    else:
                        returnValue = "true"
                    varRef.setValueAndType(returnValue, "BOOL")
                else:
                    exit(53)
            else:
                exit(53)
            totalInstructionsDone = totalInstructionsDone + 1

        if loadedInstruction.getName().upper() == "TYPE":
            type = ""
            tmpArgumentReference = loadedInstruction.getArg()
            if tmpArgumentReference[0].getType().upper() == "VAR":
                varRef = getVarReference(tmpArgumentReference[0].getType().upper(),tmpArgumentReference[0].getValue(), GF, tmpFrame, frame_Stack,tmpArgumentReference)
                if tmpArgumentReference[1].getType().upper() == "VAR":
                    varTypeRef = getVarReference(tmpArgumentReference[1].getType().upper(),tmpArgumentReference[1].getValue(), GF, tmpFrame, frame_Stack,tmpArgumentReference)
                    type = varTypeRef.getType()
                elif tmpArgumentReference[1].getType().upper() in symbols:
                    type = tmpArgumentReference[1].getType().lower()
                else:
                    exit(32)
                varRef.setValueAndType(type,"STRING")
            else:
                exit(32)

            totalInstructionsDone = totalInstructionsDone + 1

        if loadedInstruction.getName().upper() == "CONCAT":
            tmpArgumentReference = loadedInstruction.getArg()
            if tmpArgumentReference[0].getType().upper() == "VAR":
                varRef = getVarReference(tmpArgumentReference[0].getType().upper(), tmpArgumentReference[0].getValue(),GF, tmpFrame, frame_Stack, tmpArgumentReference)
                val1 = getSymbolValue(1,GF,tmpFrame,frame_Stack,tmpArgumentReference)
                val2 = getSymbolValue(2, GF, tmpFrame, frame_Stack, tmpArgumentReference)
                type1 = getSymbolType(1, GF, tmpFrame, frame_Stack, tmpArgumentReference)
                type2 = getSymbolType(2, GF, tmpFrame, frame_Stack, tmpArgumentReference)
                if type1 == "STRING" and type2 == "STRING":
                    varRef.setValueAndType(str(val1) + str(val2),"STRING")
                else:
                    exit(53)
            else:
                exit(53)

        if loadedInstruction.getName().upper() == "STRLEN":
            tmpArgumentReference = loadedInstruction.getArg()
            if tmpArgumentReference[0].getType().upper() == "VAR":
                varRef = getVarReference(tmpArgumentReference[0].getType().upper(), tmpArgumentReference[0].getValue(),GF, tmpFrame, frame_Stack, tmpArgumentReference)
                val1 = getSymbolValue(1, GF, tmpFrame, frame_Stack, tmpArgumentReference)
                type1 = getSymbolType(1, GF, tmpFrame, frame_Stack, tmpArgumentReference)
                if type1.upper() == "STRING":
                    varRef.setValueAndType(len(val1),"INT")
                else:
                    exit(53)
            else:
                exit(53)
        if loadedInstruction.getName().upper() == "GETCHAR":
            tmpArgumentReference = loadedInstruction.getArg()
            if tmpArgumentReference[0].getType().upper() == "VAR":
                varRef = getVarReference(tmpArgumentReference[0].getType().upper(), tmpArgumentReference[0].getValue(),GF, tmpFrame, frame_Stack, tmpArgumentReference)
                val1 = getSymbolValue(1, GF, tmpFrame, frame_Stack, tmpArgumentReference)
                type1 = getSymbolType(1, GF, tmpFrame, frame_Stack, tmpArgumentReference)
                val2 = getSymbolValue(2, GF, tmpFrame, frame_Stack, tmpArgumentReference)
                type2 = getSymbolType(2, GF, tmpFrame, frame_Stack, tmpArgumentReference)
                try :
                    val2 = int(val2)
                except:
                    exit(32)
                if type1.upper() == "STRING" and type2.upper() == "INT":
                    if len(val1)-1 >= val2:
                        varRef.setValueAndType(val1[val2],"STRING")
                    else:
                        exit(58)
                else:
                    exit(53)
            else:
                exit(53)

        if loadedInstruction.getName().upper() == "SETCHAR":
            tmpArgumentReference = loadedInstruction.getArg()
            if tmpArgumentReference[0].getType().upper() == "VAR":
                varRef = getVarReference(tmpArgumentReference[0].getType().upper(), tmpArgumentReference[0].getValue(),GF, tmpFrame, frame_Stack, tmpArgumentReference)
                val = varRef.getValue()
                type = varRef.getType()
                val1 = getSymbolValue(1, GF, tmpFrame, frame_Stack, tmpArgumentReference)
                type1 = getSymbolType(1, GF, tmpFrame, frame_Stack, tmpArgumentReference)
                val2 = getSymbolValue(2, GF, tmpFrame, frame_Stack, tmpArgumentReference)
                type2 = getSymbolType(2, GF, tmpFrame, frame_Stack, tmpArgumentReference)
                try :
                    val1 = int(val1)
                except:
                    exit(32)
                if type1.upper() == "INT" and type2.upper() == "STRING" and type.upper() == "STRING":
                    if len(val)-1 >= val1:
                        val = list(val)
                        val[val1] = val2
                        val = "".join(val)
                        varRef.setValueAndType(val,"STRING")
                    else:
                        exit(58)
                else:
                    exit(53)
            else:
                exit(53)
        if loadedInstruction.getName().upper() == "PUSHS":
            tmpArgumentReference = loadedInstruction.getArg()
            val = getSymbolValue(0, GF, tmpFrame, frame_Stack, tmpArgumentReference)
            type = getSymbolType(0, GF, tmpFrame, frame_Stack, tmpArgumentReference)
            dataStack.pushVal(type,val)

        if loadedInstruction.getName().upper() == "POPS":
            tmpArgumentReference = loadedInstruction.getArg()
            if tmpArgumentReference[0].getType().upper() == "VAR":
                varRef = getVarReference(tmpArgumentReference[0].getType().upper(), tmpArgumentReference[0].getValue(),GF, tmpFrame, frame_Stack, tmpArgumentReference)
                popedVal = dataStack.popVal()
                varRef.setValueAndType(popedVal.getValue(),popedVal.getType())
            else:
                exit(53)

    instructionOrder = instructionOrder + 1

