from aback import AbackInterpreter
from sys import argv
from blessed import Terminal

interpreter = AbackInterpreter()
term = Terminal()

def repr_error(source, line, word, name, line_string, error_details):
    # fancy error printing
    return f"""{term.bold + term.green}{source}{term.normal}({line}:{word}) {term.bold + term.red}{name}{term.normal}:
    {term.blue}|{term.normal} {line_string}
    {term.blue}|{term.normal} {error_details}"""

if len(argv) > 1:
    interpreter.source = argv[1]
    with open(argv[1]) as file:
        code = file.read()
        success, intr, err, pos, do_exit = interpreter.interpret(code)
        if not success:
            print(repr_error(intr.source, pos[0], pos[1], err[0], pos[2], err[1]))
else:
    print(f"""Aback v{interpreter.version} shell
Predefined variables: {interpreter.repr_vars(interpreter.vars)}""")
    interpreter.source = '<stdin>'
    while True:
        code = input('aback> ')
        success, intr, err, pos, do_exit = interpreter.interpret(code)
        if not success:
            print(repr_error(intr.source, pos[0], pos[1], err[0], pos[2], err[1]))
        print(term.orange + term.bold + '[' + intr.repr_stack(intr.stack) + ']' + term.normal)
        if do_exit:
            break