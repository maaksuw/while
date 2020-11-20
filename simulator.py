import re

error = False
error_cmd = ""

variablename = "[a-zA-Z]([a-zA-Z]|[0-9])*"
firstrow = re.compile("input:(" + variablename + ",)*" + variablename + ";")
plusmoonus = re.compile(variablename + "=" + variablename + "[+-]([0-9])*;")
whilecmd = re.compile("while[(]" + variablename + "[!][=]0[)][{]")
endbracket = re.compile("[}]")

def remove_whitespace(program):
    ans = []
    lines = program.splitlines()
    for line in lines:
        line = "".join(line.split())
        if line != "": ans.append(line)
    return ans
        
def is_WHILEprogram(program):
    global error
    global error_cmd
    error = False
    error_cmd = ""
    program = remove_whitespace(program)
    commands = [0]*len(program)
    variables = {}
    variables["ans"] = 0
    cnt = 1
    if read_input(program, variables, cnt):
        parse_WHILEprogram(1, program, variables, cnt, commands)
        if not error:
            return (True, commands, len(variables))
        else:
            return (False, error_cmd, None)
    else:
        return (False, error_cmd, None)

def read_input(program, variables, cnt):
    global firstrow
    global error_cmd
    inputrow = program[0]
    if not firstrow.fullmatch(inputrow):
        error_cmd = inputrow
        return False
    inputvars = inputrow[inputrow.index(":") + 1 : len(inputrow) - 1]
    dots = [-1]
    for i in range(len(inputvars)):
        if inputvars[i] == ",": dots.append(i)
    dots.append(len(inputvars))
    for i in range(1, len(dots)):
        varname = inputvars[dots[i - 1] + 1 : dots[i]]
        variables[varname] = cnt
        cnt += 1
    return True
    
        
def parse_WHILEprogram(ind, program, variables, cnt, commands):
    
    global error
    global error_cmd
    global variablename
    global plusmoonus
    global whilecmd
    global endbracket
    
    n = len(program)
    while (ind < n):
        kasky = program[ind]
        if(plusmoonus.fullmatch(kasky)):
            cnt = parse_assignment(kasky, variables, cnt, commands, ind)
        elif(whilecmd.fullmatch(kasky)):
            finalind = parse_WHILEprogram(ind + 1, program, variables, cnt, commands)
            if error: 
                return
            var = kasky[kasky.index("(") + 1 : kasky.index("!")]
            if var not in variables:
                variables[var] = cnt
                cnt += 1
            commands[ind] = (3, variables[var], finalind + 1)
            commands[finalind] = (4, ind)
            ind = finalind
        elif(endbracket.fullmatch(kasky)):
            return ind
        else:
            error = True
            error_cmd = kasky
            return
        ind += 1
        
def parse_assignment(kasky, variables, cnt, commands, ind):
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
    return cnt
        
        
def test(commands, variable_cnt, tests):
    for test in tests:
        input_string = test[0]
        output = test[1]
        input_list = input_string.split()
        input = []
        for number in input_list:
            input.append(int(number))
        result = simulate(commands, variable_cnt, input)
        if result != output:
            return (input_string, output, result)
    return True

def simulate(commands, variable_cnt, input):
    pc = 1
    variables = [0]*variable_cnt
    var = 1
    for input_value in input:
        variables[var] = input_value
        var += 1
    n = len(commands)
    while(pc < n):
        command = commands[pc]
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
    return variables[0]
