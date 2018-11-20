def parse(command):
    """
    a function the parse the command
    input -> string
    output -> tuple (identified, file_name, index)
    identified: is 1 if command is valid and 0 in case of wrong command
    file_name: a string contain file name
    index: the index of the bit that will be flipped, else NONE
    """
    splitted = command.lower().split('|')

    if len(splitted) < 2 or len(splitted) > 3:
        return 0, None, None

    gen = splitted[0].split('<')
    if len(gen) is not 2 or gen[0].strip() != 'generator':
        return 0, None, None
    file_name = gen[1].strip()

    if len(splitted) is 2:
        if splitted[1].strip() == 'verifier':
            return 1, file_name, None
        else:
            return 0, file_name, None

    else:
        arg = splitted[1].strip().split()
        if len(arg) is not 2 or arg[0] != 'alter' or not arg[1].isdigit():
            return 0, file_name, None
        index = int(arg[1])

        if splitted[2].strip() != 'verifier':
            return 0, file_name, index

        return 1, file_name, index

'''
# test cases
cmd1 = 'generator < file | verifier'
cmd2 = 'generator < file | alter 5 | verifier'
cmd3 = 'generator < file | alter arg | verifier'
print(parse(cmd1))
print(parse(cmd2))
print(parse(cmd3))
'''
