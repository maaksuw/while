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
        parse_WHILEprogram(1, program, variables, cnt, commands, 0)
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
    
        
def parse_WHILEprogram(ind, program, variables, cnt, commands, level):
    
    global error
    global variablename
    global plusmoonus
    global whilecmd
    global endbracket
    
    n = len(program)
    while (ind < n):
        cmd = program[ind]
        if(plusmoonus.fullmatch(cmd)):
            cnt = parse_assignment(cmd, variables, cnt, commands, ind)
        elif(whilecmd.fullmatch(cmd)):
            finalind = parse_WHILEprogram(ind + 1, program, variables, cnt, commands, level + 1)
            if error: 
                return
            if finalind == -1:
                raise_error("Kaarisulje puuttuu.")
                return
            var = cmd[cmd.index("(") + 1 : cmd.index("!")]
            if var not in variables:
                variables[var] = cnt
                cnt += 1
            commands[ind] = (3, variables[var], finalind + 1)
            commands[finalind] = (4, ind)
            ind = finalind
        elif(endbracket.fullmatch(cmd)):
            if level == 0:
                raise_error(cmd)
                return
            return ind
        else:
            raise_error(cmd)
            return
        ind += 1
    return -1

def raise_error(message):
    global error
    global error_cmd
    error = True
    error_cmd = message
        
def parse_assignment(cmd, variables, cnt, commands, ind):
    firstvar = cmd[ : cmd.index("=")]
    secondvar = 0
    plus = False
    moonus = False
    if "+" in cmd:
        secondvar = cmd[len(firstvar) + 1 : cmd.index("+")]
        plus = True
    if "-" in cmd:
        secondvar = cmd[len(firstvar) + 1 : cmd.index("-")]
        moonus = True
    constant = cmd[len(firstvar) + len(secondvar) + 2 : len(cmd) - 1]
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
