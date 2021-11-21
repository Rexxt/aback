# Aback, a FORTH-like language
class AbackLanguage:
    def __init__(self):
        self.stack = []
        self.words = {}
        self.vars = {}
        self.source = ''
        self.version = '0.1.0'
        self.defined_words = ('print',
            '+',
            '-',
            '*', 
            '/',
            'dup',
            'drop',
            'swap',
            'over',
            'rot',
            '"',
            'flush',
            ':',
            ';;',
            'include',
            'if',
            'while',
            'true',
            'false',
            'null',
            'and',
            'or',
            'not',
            '>',
            '<',
            '>=',
            '<=',
            '==',
            '!=',
            '$',
            'exit'
        )
        self.processed_code = ''

    def repr_data(self, data):
        if data == True:
            return 'true'
        elif data == False:
            return 'false'
        elif data == None:
            return 'null'
        else:
            return str(data)
    
    def repr_stack(self, stack):
        return ', '.join([self.repr_data(data) for data in stack])
    
    def repr_vars(self, vars):
        return ', '.join([f"{k}: {self.repr_data(vars[k])}" for k in vars])

    """def pre_process(self, code):
        # Check for errors, assign variables, predefine words
        lines = code.split('\n')
        line_index = 0
        def_tree = []
        processed_lines = []
        temp_stack = []
        while line_index < len(lines):
            line = lines[line_index]
            words = line.split()
            word_index = 0
            processed_words = []
            while word_index < len(words):
                # Preprocessor
                word = words[word_index]
                if len(def_tree) == 0: # In normal state
                    if word.startswith("$"):
                        # Variable preassignment
                        if not word[1].isdigit() and not word[1:] in self.words and not word[:-1] in self.defined_words and word[1:].isalnum():
                            self.vars[word[1:]] = temp_stack.pop()
                        else:
                            return False, self, ('InvalidNameError', f'Name \'{word[1:]}\' may not be used.'), (line_index + 1, word_index + 1, line), False
                    elif word[-1] == ':' and len(word) > 1:
                        # Word predefinition
                        if not word[1].isdigit() and not word[:-1] in self.defined_words:
                            def_tree.append(['def', word[:-1], []])
                        else:
                            return False, self, ('InvalidNameError', f'Name \'{word[:-1]}\' may not be used.'), (line_index + 1, word_index + 1, line), False
                    elif word == 'include':
                        # include mode
                        def_tree.append(['include', ['']])
                    elif word.isdigit():
                        temp_stack.append(int(word))
                    elif word.replace('.', '').isdigit():
                        temp_stack.append(float(word))
                    elif word == '"':
                        def_tree.append(['string', []])
                    elif word == '':
                        # empty word - do nothing
                        pass
                    elif word in self.words:
                        processed_words.append(word)
                    elif word in self.vars:
                        temp_stack.append(self.vars[word])
                        processed_words.append(word)
                    else:
                        processed_words.append(word)
                elif def_tree[-1][0] == 'def':
                    if word == ';;':
                        self.words[def_tree[-1][1]] = " ".join(def_tree[-1][2])
                        def_tree.pop()
                    else:
                        def_tree[-1][2].append(word)
                elif def_tree[-1][0] == 'string':
                    if word == '"':
                        self.stack.append(" ".join(def_tree[-1][1]))
                        def_tree.pop()
                    elif word == '\\"':
                        def_tree[-1][1].append('"')
                    elif word == '':
                        def_tree[-1][1].append(' ')
                    else:
                        def_tree[-1][1].append(word)
                elif def_tree[-1][0] == 'include':
                    if word == ';;':
                        for module in def_tree[-1][1]:
                            mod = module + '.abk'
                            try:
                                with open(mod) as f:
                                    success, intr, err, pos, do_exit = self.pre_process(f.read()) # Recursive preprocessing
                                    if not success:
                                        intr.source = module
                                        return False, intr, err, pos, do_exit
                                    if do_exit:
                                        return True, self, None, (line_index + 1, word_index + 1, line), True
                            except FileNotFoundError:
                                return False, self, ('FileNotFoundError', f'File \'{mod}\' was not found.'), (line_index + 1, word_index + 1, line), False
                        def_tree.pop()
                    elif word == '&&':
                        def_tree[-1][1].append('')
                    else:
                        def_tree[-1][1][-1] += word if word != '' else ' '
                word_index += 1
            processed_lines.append(" ".join(processed_words))
            line_index += 1
        if len(def_tree) > 0:
            def_name_repr = ''
            if def_tree[-1][0] == 'def':
                def_name_repr = 'word'
            else:
                def_name_repr = def_tree[-1][0]
            return False, self, ('EOFError', f'Unexpected end of file while defining {def_name_repr}. Please make sure all definitions are finished.'), (line_index + 1, word_index + 1, line), False
        self.processed_code = '\n'.join(processed_lines)
        return True, self, None, (line_index + 1, word_index + 1, line), False # success, interpreter, error, position, exit
"""

    def interpret(self, code):
        lines = code.split('\n')
        line_index = 0
        def_tree = []
        while line_index < len(lines):
            line = lines[line_index]
            words = line.split()
            word_index = 0
            #print(f'{line_index}: {line}')
            while word_index < len(words):
                # interpret words
                word = words[word_index]
                if len(def_tree) == 0:
                    if word == 'print':
                        print(self.repr_data(self.stack.pop()))
                    elif word == '+':
                        # if we directly do self.stack.append(self.stack.pop() + self.stack.pop()), we will add things in reverse order
                        # which is not a problem for numbers, but for strings, it is
                        # so we will opt to do it another way
                        # we will do the same for division and subtraction
                        term_b = self.stack.pop()
                        term_a = self.stack.pop()
                        self.stack.append(term_a + term_b)
                    elif word == '-':
                        term_b = self.stack.pop()
                        term_a = self.stack.pop()
                        self.stack.append(term_a - term_b)
                    elif word == '*':
                        self.stack.append(self.stack.pop() * self.stack.pop())
                    elif word == '/':
                        term_b = self.stack.pop()
                        term_a = self.stack.pop()
                        self.stack.append(term_a / term_b)
                    elif word == 'dup':
                        self.stack.append(self.stack[-1])
                    elif word == 'drop':
                        self.stack.pop()
                    elif word == 'swap':
                        self.stack[-1], self.stack[-2] = self.stack[-2], self.stack[-1]
                    elif word == 'over':
                        self.stack.append(self.stack[-2])
                    elif word == 'rot':
                        self.stack[-1], self.stack[-2], self.stack[-3] = self.stack[-3], self.stack[-1], self.stack[-2]
                    elif word.isdigit():
                        self.stack.append(int(word))
                    elif word.replace('.', '').isdigit():
                        self.stack.append(float(word))
                    elif word == '"':
                        def_tree.append(['string', []])
                    elif word[-1] == ':' and len(word) > 1:
                        # checking if name is valid
                        if not word[1].isdigit() and not word[:-1] in self.defined_words:
                            def_tree.append(['def', word[:-1], []])
                        else:
                            return False, self, ('InvalidNameError', f'Name \'{word[:-1]}\' may not be used.'), (line_index + 1, word_index + 1, line), False
                    elif word == 'flush':
                        self.stack = []
                    elif word == '/*':
                        # comment
                        def_tree.append(['comment'])
                    # booleans
                    elif word == 'true':
                        self.stack.append(True)
                    elif word == 'false':
                        self.stack.append(False)
                    elif word == 'null':
                        self.stack.append(None)
                    elif word == 'include':
                        # include mode
                        def_tree.append(['include', ['']])
                    elif word.startswith("$"):
                        #print(not word[1].isdigit(), not word[:-1] in self.words, not word[:-1] in defined_words, word[:-1].isalnum())
                        if not word[1].isdigit() and not word[1:] in self.words and not word[:-1] in self.defined_words and word[1:].isalnum():
                            self.vars[word[1:]] = self.stack.pop()
                        else:
                            return False, self, ('InvalidNameError', f'Name \'{word[1:]}\' may not be used.'), (line_index + 1, word_index + 1, line), False
                    elif word == 'exit':
                        return True, self, None, (line_index + 1, word_index + 1, line), True
                    elif word == '':
                        # empty word - do nothing
                        pass
                    elif word in self.words:
                        try:
                            self.interpret(self.words[word])
                        finally: pass
                    elif word in self.vars:
                        self.stack.append(self.vars[word])
                    else:
                        return False, self, ('UnknownWordError', f'Word \'{word}\' was not found.'), (line_index + 1, word_index + 1, line), False
                elif def_tree[-1][0] == 'string':
                    if word == '"':
                        self.stack.append(" ".join(def_tree[-1][1]))
                        def_tree.pop()
                    elif word == '\\"':
                        def_tree[-1][1].append('"')
                    elif word == '':
                        def_tree[-1][1].append(' ')
                    else:
                        def_tree[-1][1].append(word)
                elif def_tree[-1][0] == 'def':
                    if word == ';;':
                        self.words[def_tree[-1][1]] = " ".join(def_tree[-1][2])
                        def_tree.pop()
                    else:
                        def_tree[-1][2].append(word)
                elif def_tree[-1][0] == 'comment':
                    if word == '*/':
                        def_tree.pop()
                elif def_tree[-1][0] == 'include':
                    if word == ';;':
                        for module in def_tree[-1][1]:
                            mod = module + '.abk'
                            try:
                                with open(mod) as f:
                                    success, intr, err, pos, do_exit = self.interpret(f.read())
                                    if not success:
                                        intr.source = module
                                        return False, intr, err, pos, do_exit
                                    if do_exit:
                                        return True, self, None, (line_index + 1, word_index + 1, line), True
                            except FileNotFoundError:
                                return False, self, ('FileNotFoundError', f'File \'{mod}\' was not found.'), (line_index + 1, word_index + 1, line), False
                        def_tree.pop()
                    elif word == '&&':
                        def_tree[-1][1].append('')
                    else:
                        def_tree[-1][1][-1] += word if word != '' else ' '
                else:
                    raise Exception('Unknown definition tree state: ' + str(def_tree[-1]))
                word_index += 1
            line_index += 1
        # making sure all definitions are finished - if not, return error
        if len(def_tree) > 0:
            def_name_repr = ''
            if def_tree[-1][0] == 'def':
                def_name_repr = 'word'
            else:
                def_name_repr = def_tree[-1][0]
            return False, self, ('EOFError', f'Unexpected end of file while defining {def_name_repr}. Please make sure all definitions are finished.'), (line_index + 1, word_index + 1, line), False
        return True, self, None, (line_index + 1, word_index + 1, line), False # success, interpreter, error, position, exit
