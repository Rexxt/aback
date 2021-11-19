# Aback, a FORTH-like language
class AbackInterpreter:
    def __init__(self):
        self.stack = []
        self.words = {}

    def interpret(self, code):
        lines = code.split('\n')
        line_index = 0
        mode = 'normal'
        def_tree = []
        while line_index < len(lines):
            line = lines[line_index]
            words = line.split()
            word_index = 0
            while word_index < len(words):
                # interpret words
                word = words[word_index]
                if mode == 'normal':
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
                    elif word in self.words:
                        try:
                            self.words[word](self)
                        except IndexError:
                            print('Not enough arguments for ' + word)
                    elif word.isdigit():
                        self.stack.append(int(word))
                    elif word.replace('.', '').isdigit():
                        self.stack.append(float(word))
                    elif word == '"':
                        mode = 'string'
                        def_tree.append(['string', []])
                    elif word[-1] == ':':
                        mode = 'def'
                        def_tree.append(['def', word[:-1], []])
                    elif word == 'flush':
                        self.stack = []
                    elif word in self.words:
                        self.interpret(self.words[word])
                elif mode == 'string':
                    if word == '"':
                        mode = 'normal'
                        self.stack.append(" ".join(def_tree[-1][1]))
                        def_tree.pop()
                    elif word == '\\"':
                        def_tree[-1][1].append('"')
                    else:
                        def_tree[-1][1].append(word)
                elif mode == 'def':
                    if word == ';;':
                        mode = 'normal'
                        self.words[def_tree[-1][1]] = " ".join(def_tree[-1][2])
                        def_tree.pop()
                    else:
                        def_tree[-1][2].append(word)
                word_index += 1
            line_index += 1
        return True, self, None, mode # success, interpreter, error, mode