import re
import messages

error = False
error_msg = ""
cnt = 0

variablename = "[a-zA-Z]([a-zA-Z]|[0-9])*"
firstrow = re.compile("input:(" + variablename + ",)*" + variablename + ";")
plusmoonus = re.compile(variablename + "=" + variablename + "[+-]([0-9])*;")
whilecmd = re.compile("while[(]" + variablename + "[!][=]0[)][{]")
endbracket = re.compile("[}]")

max_steplimit = 1000000

def remove_whitespace(program):
    ans = []
    lines = program.splitlines()
    for line in lines:
        line = "".join(line.split())
        if line != "": ans.append(line)
    return ans
        
def is_WHILEprogram(program):
    global error
    global error_msg
    global cnt
    error = False
    error_msg = ""
    program = remove_whitespace(program)
    commands = [0]*len(program)
    variables = {}
    variables["ans"] = 0
    cnt = 1
    if read_input(program, variables):
        parse_WHILEprogram(1, program, variables, commands, 0)
        if not error:
            return (True, commands, len(variables))
    return (False, error_msg)

def read_input(program, variables):
    global firstrow
    global cnt
    inputrow = program[0]
    if not firstrow.fullmatch(inputrow):
        raise_error(inputrow)
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
    
        
def parse_WHILEprogram(ind, program, variables, commands, level):
    
    global error
    global variablename
    global plusmoonus
    global whilecmd
    global endbracket
    global cnt
    
    n = len(program)
    while (ind < n):
        cmd = program[ind]
        if(plusmoonus.fullmatch(cmd)):
            parse_assignment(cmd, variables, commands, ind)
        elif(whilecmd.fullmatch(cmd)):
            finalind = parse_WHILEprogram(ind + 1, program, variables, commands, level + 1)
            if error: 
                return
            if finalind == -1:
                raise_error(messages.bracket_missing())
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
    global error_msg
    error = True
    error_msg = message
        
def parse_assignment(cmd, variables, commands, ind):
    global cnt
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
        
        
def test(commands, variable_cnt, tests):
    global error
    global error_msg
    error = False
    for test in tests:
        input_string = test[0]
        output = test[1]
        input_list = input_string.split()
        input = []
        for number in input_list:
            input.append(int(number))
        result = simulate(commands, variable_cnt, input)
        if error:
            return (1, error_msg)
        if result != output:
            return (2, input_string, output, result)
    return True

def simulate(commands, variable_cnt, input):
    global max_steplimit
    steps = 0
    pc = 1
    variables = [0]*variable_cnt
    var = 1
    for input_value in input:
        variables[var] = input_value
        var += 1
    n = len(commands)
    while(pc < n):
        steps += 1
        if steps >= max_steplimit:
            raise_error(messages.steplimit_exceeded())
            return
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
