# Aback, a FORTH-like language
class AbackInterpreter:
    def __init__(self):
        self.stack = []
        self.words = {}
        self.source = ''

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
                        print(self.stack.pop())
                    elif word == '+':
                        self.stack.append(self.stack.pop() + self.stack.pop())
                    elif word == '-':
                        self.stack.append(-self.stack.pop() + self.stack.pop())
                    elif word == '*':
                        self.stack.append(self.stack.pop() * self.stack.pop())
                    elif word == '/':
                        self.stack.append(self.stack.pop() / self.stack.pop())
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
                        if not word[1].isdigit() and not word[:-1] in ('print', '+', '-', '*', '/', 'dup', 'drop', 'swap', 'over', 'rot', '"', 'flush', ':', ';;'):
                            def_tree.append(['def', word[:-1], []])
                        else:
                            return False, self, ('InvalidNameError', f'Name \'{word[:-1]}\' may not be used.'), (line_index + 1, word_index + 1, line)
                    elif word == 'flush':
                        self.stack = []
                    elif word == '/*':
                        # comment
                        def_tree.append(['comment'])
                    elif word == '':
                        # empty word - do nothing
                        pass
                    elif word in self.words:
                        try:
                            self.interpret(self.words[word])
                        finally: pass
                    else:
                        return False, self, ('UnknownWordError', f'Word \'{word}\' was not found.'), (line_index + 1, word_index + 1, line)
                elif def_tree[-1][0] == 'string':
                    if word == '"':
                        self.stack.append(" ".join(def_tree[-1][1]))
                        def_tree.pop()
                    elif word == '\\"':
                        def_tree[-1][1].append('"')
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
                word_index += 1
            line_index += 1
        # making sure all definitions are finished - if not, return error
        if len(def_tree) > 0:
            def_name_repr = ''
            if def_tree[-1][0] == 'def':
                def_name_repr = 'word'
            else:
                def_name_repr = def_tree[-1][0]
            return False, self, ('EOFError', f'Unexpected end of file while defining {def_name_repr}. Please make sure all definitions are finished.'), (line_index + 1, word_index + 1, line)
        return True, self, None, (line_index + 1, word_index + 1, line) # success, interpreter, error, position