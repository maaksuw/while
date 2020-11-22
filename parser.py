import re
import messages

error = False
error_msg = ""
cnt = 0

def raise_error(message):
    global error
    global error_msg
    error = True
    error_msg = message

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
    if parse_input(program, variables):
        parse_WHILEprogram(1, program, variables, commands, 0)
        if not error:
            return (True, commands, len(variables))
    return (False, error_msg)

def parse_input(program, variables):
    global cnt
    inputrow = program[0]
    if not messages.inputvariables().fullmatch(inputrow):
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
    global cnt
    n = len(program)
    while (ind < n):
        cmd = program[ind]
        if(messages.variable_assignment().fullmatch(cmd)):
            parse_assignment(cmd, variables, commands, ind)
        elif(messages.while_command().fullmatch(cmd)):
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
        elif(messages.endbracket().fullmatch(cmd)):
            if level == 0:
                raise_error(cmd)
                return
            return ind
        else:
            raise_error(cmd)
            return
        ind += 1
    return -1

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
        
