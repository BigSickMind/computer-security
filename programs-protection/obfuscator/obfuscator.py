all_garbage_values = []


def get_lines(file):
    all_lines = []
    with open(file, 'r') as input_code:
        for line in input_code:
            pos = 0
            while line[pos] == ' ' and pos < len(line):
                pos += 1
            line = line[pos:]
            all_lines.append(line)
    return all_lines


def delete_comments(all_lines):
    new_lines = []
    flag = False
    construct_line = ''
    for line in all_lines:
        if not flag:
            pos = line.find('//')
            if pos != -1:
                line = line[:pos] + '\n'
                new_lines.append(line)
                continue
            pos = line.find('/*')
            if pos != -1:
                construct_line += line[:pos]
                flag = True
            if not flag:
                new_lines.append(line)
        if flag:
            pos = line.find('*/')
            if pos != -1:
                construct_line += line[pos + 2:]
                if len(construct_line):
                    new_lines.append(construct_line)
                construct_line = ''
                flag = False
    return new_lines


def get_constants(all_lines):
    all_constants = {}
    # define_constants = {}
    for line in all_lines:
        pos = 0
        while pos < len(line) and not line[pos].isalpha():
            pos += 1
        pos1 = line.find(' ', pos)
        if pos1 != -1:
            word = line[pos:pos1]
            if word == 'const':
                pos = line.find('=')
                if line[pos + 1] == ' ':
                    pos += 2
                else:
                    pos += 1
                if line[len(line) - 1] == '\n':
                    const2 = line[pos:(len(line) - 1)]
                const2 = const2[:(len(const2) - 1)]
                if line[pos - 1] == ' ':
                    pos -= 3
                else:
                    pos -= 2
                if line[pos] == ' ':
                    pos -= 1
                const1 = ''
                while line[pos] != ' ':
                    const1 += line[pos]
                    pos -= 1
                const1 = const1[::-1]
                all_constants[const1] = const2
            elif word == 'typedef':
                pos = line.find(' ')
                pos2 = line.rfind(' ')
                const1 = line[pos + 1:pos2]
                const2 = line[pos2 + 1:]
                if const2[len(const2) - 1] == '\n':
                    const2 = const2[:len(const2) - 1]
                const2 = const2[:len(const2) - 1]
                all_constants[const2] = const1
            elif word == '#define':
                # import re
                # line_define = re.findall(r'\w+[)\n]', line)
                # print(line_define)
                pass
    all_constants['INT_MAX'] = str(2147483647)
    all_constants['INT_MIN'] = str(-2147483647)
    all_constants['LLONG_MAX'] = str(9223372036854775807)
    all_constants['LLONG_MIN'] = str(-9223372036854775807)
    return all_constants


def delete_constants(all_lines):
    new_lines = []
    for line in all_lines:
        pos = 0
        while pos < len(line) and not line[pos].isalpha():
            pos += 1
        pos1 = line.find(' ', pos)
        if pos1 != -1:
            word = line[pos:pos1]
            if word == 'const' or word == 'typedef':  # or word == '#define':
                continue
        new_lines.append(line)
    return new_lines


def get_variables(all_lines, all_constants):
    all_variables = {}
    for line in all_lines:
        import re
        line_variables = re.findall(r'\w+[,;[\]\-\+=/\*%\&\|\^!)(\: ]', line)
        if len(line_variables):
            temp = line_variables[0][:len(line_variables[0]) - 1]
            if temp == 'define' or temp == 'typedef' or temp == 'const':
                continue
        line_variables = re.findall(r'\w+[,;[\]\-\+=/\*%\&\|\^!)(\: ]', line)
        if len(line_variables):
            variables = []
            for variable in line_variables:
                variable = variable[:(len(variable) - 1)]
                if not variable[0].isalpha() and not variable[0].isdigit():
                    variable = variable[1:]
                if len(variable) and not variable[0].isdigit():
                    variables.append(variable)
            if len(variables):
                for variable in variables:
                    from keywords import is_keyword
                    if not is_keyword(variable) and variable not in all_constants.keys():
                        all_variables[variable] = ''
    return all_variables


def rename_variables(all_variables):
    from random import randint
    number = randint(1000000, 100000000)
    symbol = 'a'
    for key in all_variables.keys():
        all_variables[key] = str(symbol + str(number))
        number += 1
    return all_variables


def transform_lines(all_lines, all_variables, all_constants):
    new_lines = []
    for line in all_lines:
        for variable in all_variables.keys():
            pos = line.find(variable)
            while pos != -1:
                grance = pos + len(variable)
                if ((pos >= 1 and not line[pos - 1].isalpha() and line[pos - 1] != '_') or pos == 0) and grance < len(line) and not line[
                    grance].isalpha() and line[grance] != '_':
                    line = line[:pos] + all_variables[variable] + line[pos + len(variable):]
                pos = line.find(variable, pos + len(variable) + 1)

        for constant in all_constants.keys():
            pos = line.find(constant)
            while pos != -1:
                grance = pos + len(constant)
                if ((pos >= 1 and not line[pos - 1].isalpha() and line[pos - 1] != '_') or pos == 0) and grance < len(line) and not line[
                    grance].isalpha() and line[grance] != '_':
                    line = line[:pos] + all_constants[constant] + line[pos + len(constant):]
                pos = line.find(constant, pos + len(constant) + 1)
        new_lines.append(line)
    return new_lines


def generate_values(all_garbage_values):
    while True:
        from random import randint
        symbol = chr(randint(ord('b'), ord('z')))
        number = randint(1000000, 100000000)
        garbage_value = symbol + str(number)
        if garbage_value not in all_garbage_values:
            break
    return garbage_value


def generate_expressions(garbage_value_input, operations):
    from random import randint, choice
    number_of_values_in_expressions = randint(1, 2)
    garbage_string = ''
    for j in range(number_of_values_in_expressions):
        garbage_value = choice(all_garbage_values)
        while garbage_value == garbage_value_input:
            garbage_value = choice(all_garbage_values)
        operation = choice(operations)
        if operation == '<<' or operation == '>>':
            value = hex(randint(10, 30))
        else:
            value = hex(randint(2e10, 2e20))
        garbage_string += '(' + garbage_value + ' ' + operation + ' ' + str(value) + ')'
        if number_of_values_in_expressions == 1:
            new_operation = choice(operations)
            if new_operation == '<<' or new_operation == '>>':
                new_value = hex(randint(10, 30))
            else:
                new_value = hex(randint(2e10, 2e20))
            garbage_string += ' ' + new_operation + ' ' + str(new_value)
        elif j < number_of_values_in_expressions - 1:
            new_operation = choice(['&', '|', '^'])
            garbage_string += ' ' + new_operation + ' '

    return garbage_string


def generate_garbage():
    type_value = 'long long '
    operations = ['<<', '>>', '&', '|', '^']
    from random import randint, choice
    number_of_strings = randint(7, 11)
    garbage_strings = []
    for i in range(3):
        garbage_value = generate_values(all_garbage_values)
        value = hex(randint(2e10, 2e20))
        garbage_string = type_value + garbage_value + ' = ' + str(value) + ';'
        all_garbage_values.append(garbage_value)
        garbage_strings.append(garbage_string)

    for i in range(0, number_of_strings - 3, 4):
        garbage_value_new = generate_values(all_garbage_values)

        garbage_string = generate_expressions(' ', operations)

        garbage_string_new = type_value + garbage_value_new + ' = ' + garbage_string + ';'
        garbage_strings.append(garbage_string_new)

        for k in range(3):
            garbage_value = choice(all_garbage_values)
            garbage_string = generate_expressions(garbage_value, operations)
            garbage_string_new = garbage_value + ' = ' + garbage_string + ';'
            garbage_strings.append(garbage_string_new)

    return garbage_strings


def add_garbage(new_lines):
    open_brackets = 0
    new_new_lines = []
    flag = False
    for line in new_lines:
        pos = line.find('{')
        pos1 = line.find('}')
        if pos != -1:
            open_brackets += 1
            all_garbage_values.clear()
            flag = True
        if pos1 != - 1:
            open_brackets -= 1
        new_new_lines.append(line)
        if open_brackets > 0 and flag:
            garbage_strings = generate_garbage()
            for garbage_string in garbage_strings:
                new_new_lines.append(garbage_string + '\n')
            flag = False
    return new_new_lines


def write_to_file(new_lines):
    with open('out.cpp', 'w') as output_code:
        for line in new_lines:
            output_code.write(line)


def obfuscator(file):
    all_lines = get_lines(file)

    all_lines = delete_comments(all_lines)

    all_constants = get_constants(all_lines)
    all_lines = delete_constants(all_lines)

    all_variables = get_variables(all_lines, all_constants)
    all_variables = rename_variables(all_variables)

    #print(all_variables)
    #print(all_constants)

    new_lines = transform_lines(all_lines, all_variables, all_constants)

    new_new_lines = add_garbage(new_lines)

    write_to_file(new_new_lines)


if __name__ == '__main__':
    file = input()
    obfuscator(file)
