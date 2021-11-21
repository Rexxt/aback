from aback import AbackLanguage
from sys import argv
from blessed import Terminal

lang = AbackLanguage()
term = Terminal()

def repr_error(source, line, word, name, line_string, error_details, time): # time = "preprocess" or "run"
    # fancy error printing
    return f"""{term.bold + term.green}{source}{term.normal}({line}:{word}) {term.bold + term.red}{name}{term.normal} [at {time}-time]:
    {term.blue}|{term.normal} {line_string}
    {term.blue}|{term.normal} {error_details}"""

if len(argv) > 1:
    lang.source = argv[1]
    with open(argv[1]) as file:
        code = file.read()
        """preprocess_success, preprocess_intr, preprocess_err, preprocess_pos, preprocess_do_exit = lang.pre_process(code)
        if not preprocess_success:
            print(repr_error(preprocess_intr.source, preprocess_pos[0], preprocess_pos[1], preprocess_err[0], preprocess_pos[2], preprocess_err[1], "preprocess"))
            # preprocessing failed, so we don't need to run the code
            exit(1)"""
        success, intr, err, pos, do_exit = lang.interpret(code)
        if not success:
            print(repr_error(intr.source, pos[0], pos[1], err[0], pos[2], err[1], "run"))
else:
    print(f"""Aback v{lang.version} shell
Predefined variables: {lang.repr_vars(lang.vars)}""")
    lang.source = '<stdin>'
    while True:
        code = input('aback> ')
        """preprocess_success, preprocess_intr, preprocess_err, preprocess_pos, preprocess_do_exit = lang.pre_process(code)
        if not preprocess_success:
            print(repr_error(preprocess_intr.source, preprocess_pos[0], preprocess_pos[1], preprocess_err[0], preprocess_pos[2], preprocess_err[1], "preprocess"))
            # preprocessing failed, so we don't need to run the code
            continue"""
        success, intr, err, pos, do_exit = lang.interpret(code)
        if not success:
            print(repr_error(intr.source, pos[0], pos[1], err[0], pos[2], err[1], "run"))
        print(term.orange + term.bold + '[' + intr.repr_stack(intr.stack) + ']' + term.normal)
        if do_exit:
            break