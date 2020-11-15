import re

cnt = 0
error = False

def removewhitespace(program):
    ans = []
    lines = program.splitlines()
    for line in lines:
        line = "".join(line.split())
        if line != "": ans.append(line)
    return ans
        
def isWHILEprogram(program):
    global cnt
    global error
    error = False
    program = removewhitespace(program)
    #print(program)
    commands = [0]*len(program)
    variables = {}
    variables["ans"] = 0
    cnt = 1
    readinputvariables(program, variables)
    parsewhile(1, commands, program, variables)
    if error: 
        return (False, None, None)
    #print(commands)
    return (True, commands, len(variables))

def readinputvariables(program, variables):
    global cnt
    firstrow = program[0]
    inputvars = firstrow[firstrow.index(":") + 1 : len(firstrow) - 1]
    dots = [-1]
    for i in range(len(inputvars)):
        if inputvars[i] == ",": dots.append(i)
    dots.append(len(inputvars))
    for i in range(1, len(dots)):
        varname = inputvars[dots[i - 1] + 1 : dots[i]]
        variables[varname] = cnt
        cnt += 1
        
def parsewhile(ind, commands, program, variables):
    global cnt
    global error
    if error: return -1
    n = len(program)
    variablename = "[a-zA-Z]([a-zA-Z]|[0-9])*"
    type12 = re.compile(variablename + "=" + variablename + "[+-]([0-9])*;")
    type3 = re.compile("while[(]" + variablename + "[!][=]0[)][{]")
    type4 = re.compile("[}]")
    while (ind < n):
        kasky = program[ind]
        if(type12.fullmatch(kasky)):
            firstvar = kasky[ : kasky.index("=")]
            secondvar = 0
            plus = False
            moonus = False
            if "+" in kasky:
                secondvar = kasky[len(firstvar) + 1 : kasky.index("+")]
                plus = True
            if "-" in kasky:
                secondvar = kasky[len(firstvar) + 1 : kasky.index("-")]
                moonus = True
            constant = kasky[len(firstvar) + len(secondvar) + 2 : len(kasky) - 1]
            if firstvar not in variables:
                variables[firstvar] = cnt
                cnt += 1
            if secondvar not in variables:
                variables[secondvar] = cnt
                cnt += 1
            if plus: 
                commands[ind] = (1, variables[firstvar], variables[secondvar], int(constant))
            if moonus: 
                commands[ind] = (2, variables[firstvar], variables[secondvar], int(constant))
        elif(type3.fullmatch(kasky)):
            finalind = parsewhile(ind + 1, commands, program, variables)
            if error: return -1
            var = kasky[kasky.index("(") + 1 : kasky.index("!")]
            if var not in variables:
                variables[var] = cnt
                cnt += 1
            commands[ind] = (3, variables[var], finalind + 1)
            commands[finalind] = (4, ind)
            ind = finalind
        elif(type4.fullmatch(kasky)):
            return ind
        else: #Keksitään jokin siistempi tapa myöhemmin
            error = True
            return -1
        ind += 1
        
        
def simulate(commands, cnt):
    ### Testinä 8 ja 13, tehdään kunnolla myöhemmin
    input = (8, 13)
    #output = 21
    ###
    pc = 1
    variables = [0]*cnt
    cnt = 1
    for i in input:
        variables[cnt] = i
        cnt += 1
    print(variables)
    n = len(commands)
    while(pc < n):
        command = commands[pc]
        print(command)
        if command[0] == 1:
            variables[command[1]] = variables[command[2]] + command[3]
        elif command[0] == 2:
            value = variables[command[2]] - command[3]
            if value < 0: variables[command[1]] = 0 
            else: variables[command[1]] = value
        elif command[0] == 3:
            if variables[command[1]] == 0:
                pc = command[2]
                continue
        elif command[0] == 4:
            pc = command[1]
            continue
        pc += 1
    print(variables[0])
    #return variables[0] == output
    return variables[0]
