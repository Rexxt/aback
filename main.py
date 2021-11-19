from aback import AbackInterpreter
from sys import argv

interpreter = AbackInterpreter()

if len(argv) > 1:
    with open(argv[1]) as file:
        code = file.read()
        success, intr, err, mode = interpreter.interpret(code)
        if not success:
            print(err)
else:
    while True:
        code = input('aback> ')
        if code == 'exit':
            break
        success, intr, err, mode = interpreter.interpret(code)
        if not success:
            print(err)
        print(intr.stack, mode)