import re

cnt = 0

def removewhitespace(program):
    ans = []
    lines = program.splitlines()
    for line in lines:
        line = "".join(line.split())
        if line != "": ans.append(line)
    return ans
        
def isWHILEprogram(program):
    global cnt
    program = removewhitespace(program)
    print(program)
    commands = [0]*1000
    variables = {}
    variables["ans"] = 0
    cnt = 1
    # Käsittele ensimmäinen rivi erikseen
    parsewhile(1, commands, program, variables)
    print(commands)
    print()
    return False

def parsewhile(ind, commands, program, variables):
    global cnt
    n = len(program)
    variablename = "[a-zA-Z]([a-zA-Z]|[0-9])*"
    whilecmd = "(W|w)(H|h)(I|i)(L|l)(E|e)"
    type1 = re.compile(variablename + "=" + variablename + "[+]([0-9])*;")
    type2 = re.compile(whilecmd + "[(]" + variablename + "[!][=]0[)][{]")
    type3 = re.compile("[}]")
    while (ind < n):
        kasky = program[ind]
        if(type1.fullmatch(kasky)):
            firstvar = kasky[ : kasky.index("=")]
            secondvar = kasky[len(firstvar) + 1 : kasky.index("+")]
            constant = kasky[len(firstvar) + len(secondvar) + 2 : len(kasky) - 1]
            if firstvar not in variables:
                variables[firstvar] = cnt
                cnt += 1
            if secondvar not in variables:
                variables[secondvar] = cnt
                cnt += 1
            commands[ind] = (1, variables[firstvar], variables[secondvar], int(constant))
        elif(type2.fullmatch(kasky)):
            finalind = parsewhile(ind + 1, commands, program, variables)
            var = kasky[kasky.index("(") + 1 : kasky.index("!")]
            if var not in variables:
                variables[var] = cnt
                cnt += 1
            commands[ind] = (2, variables[var], finalind + 1)
            commands[finalind] = (3, ind)
        elif(type3.fullmatch(kasky)):
            return ind
        else:
            #Ohjelma ei ole kelvollinen, lopetetaan
            pass
        ind += 1
        
        
def simulate():
    
    return False
