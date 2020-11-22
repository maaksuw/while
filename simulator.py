import messages

steplimit_exceeded = False
max_steplimit = 1000000

def test(commands, variable_cnt, tests):
    global steplimit_exceeded
    steplimit_exceeded = False
    for test in tests:
        input_string = test[0]
        output = test[1]
        input_list = input_string.split()
        input = []
        for number in input_list:
            input.append(int(number))
        result = simulate(commands, variable_cnt, input)
        if steplimit_exceeded:
            return (1, "Step limit exceeded.")
        if result != output:
            return (2, input_string, output, result)
    return True

def simulate(commands, variable_cnt, input):
    global max_steplimit
    global steplimit_exceeded
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
            steplimit_exceeded = True
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
