import sys
import os
import re
import ast


class CodeChecker:

    def __init__(self, path_to_file):
        self.path_to_file = path_to_file
        self.current_file = open(path_to_file)
        self.lines = self.current_file.readlines()
        self.tree = ast.parse(open(path_to_file).read())
        self.arg_dict = {}
        self.defaults_dict = {}
        self.var_dict = {}
        self.mistakes = ['',
                        'S001 Too long',
                        'S002 Indentation is not a multiple of four',
                        'S003 Unnecessary semicolon',
                        'S004 At least two spaces required before inline comments',
                        'S005 TODO found',
                        'S006 More than two blank lines used before this line',
                        'S007 Too many spaces after construction_name (def or class)',
                        'S008',
                        'S009',
                        'S010',
                        'S011',
                        'S012 Default argument value is mutable']

    def finding_args_defaults_vals(self):
        for node in ast.walk(self.tree):
            if isinstance(node, ast.FunctionDef):
                arguments = [i for i in node.args.args]
                self.arg_dict[node.lineno] = [i.arg for i in arguments]
                self.defaults_dict[node.lineno] = node.args.defaults
                for i in node.body:
                    if isinstance(i, ast.Assign):
                        for j in i.targets:
                            if isinstance(j, ast.Name):
                                self.var_dict[j.lineno] = j.id

    def length(self, line: str) -> bool:
        critical_length = 79
        if len(line) <= critical_length:
            return False
        return True

    def indentation(self, line: str) -> bool:
        k = len(line) - len(line.lstrip(' '))
        if k % 4 == 0:
            return False
        return True

    def semicolon(self, line: str) -> bool:
        comment_pos = line.find('#')
        semicolon_pos = line.find(';')
        if semicolon_pos == -1:
            return False
        if comment_pos != -1:
            line = line[:comment_pos]
        return line.strip().endswith(';')

    def inline_comment(self, line: str):
        comment_pos = line.find('#')
        if comment_pos != 0 and comment_pos != -1:
            return line[comment_pos-2:comment_pos].count(' ') < 2

    def todo_comment(self, line: str) -> bool:
        comment_pos = line.find('#')
        if comment_pos == -1:
            return False
        return 'todo' in line.lower()[comment_pos:]

    def blank_lines(self, line):
        k = 0
        line_index = self.lines.index(line)
        if line_index > 2 and len(line) > 1:
            for i in range(line_index - 3, line_index):
                if len(self.lines[i]) == 1:
                    k += 1
                else:
                    break
            return k > 2

    def spaces(self, line):
        if line.strip().startswith('class'):
            return re.match(r'class  ', line.strip()) is not None
        elif line.strip().startswith('def'):
            return re.match(r'def  ', line.strip()) is not None

    def class_name(self, line):
        if line.strip().startswith('class') and not self.spaces(line):
            cl_name = line.strip()[line.find(' ') + 1: line.find(':')]
            self.mistakes[8] = f"S008 Class name '{cl_name}' should use CamelCase"
            return re.match(r'class ([A-Z][a-z]*)+[(:]', line.strip()) is None

    def function_name(self, line) -> bool:
        if not (line.strip().startswith('def') and not self.spaces(line)):
            return False
        func_name = line.strip().split()[1][:-1]
        self.mistakes[9] = f"S009 Function name '{func_name}' should use snake_case"
        return re.match(r'def [a-z0-9_]*\(', line.strip()) is None

    def arg_name(self, index):
        if index not in self.arg_dict.keys():
            return False
        for elem in self.arg_dict[index]:
            if re.match(r'[a-z0-9_]+', elem) is None:
                self.mistakes[10] = f"S010 Argument name '{elem}' should be snake_case"
                return True
        return False

    def var_name(self, index):
        if index not in self.var_dict.keys():
            return False
        if re.match(r'[a-z0-9_]+', self.var_dict[index]) is None:
            self.mistakes[11] = f"S011 Variable '{self.var_dict[index]}' in function should be snake_case"
            return True
        return False

    def arg_val(self, index):
        if index not in self.defaults_dict.keys() or self.defaults_dict[index] == []:
            return False
        for elem in self.defaults_dict[index]:
            if str(ast.dump(elem)).find('Dict') == -1 and str(ast.dump(elem)).find('List') == -1 and str(ast.dump(elem)).find('set') == -1:
                return False
        return True

    def analyze(self):
        for index, line in enumerate(self.lines, start=1):
            if self.length(line):
                print(f"{self.path_to_file}: Line {index}: {self.mistakes[1]}")
            if self.indentation(line):
                print(f"{self.path_to_file}: Line {index}: {self.mistakes[2]}")
            if self.semicolon(line):
                print(f"{self.path_to_file}: Line {index}: {self.mistakes[3]}")
            if self.inline_comment(line):
                print(f"{self.path_to_file}: Line {index}: {self.mistakes[4]}")
            if self.todo_comment(line):
                print(f"{self.path_to_file}: Line {index}: {self.mistakes[5]}")
            if self.blank_lines(line):
                print(f"{self.path_to_file}: Line {index}: {self.mistakes[6]}")
            if self.spaces(line):
                print(f"{self.path_to_file}: Line {index}: {self.mistakes[7]}")
            if self.class_name(line):
                print(f"{self.path_to_file}: Line {index}: {self.mistakes[8]}")
            if self.function_name(line):
                print(f"{self.path_to_file}: Line {index}: {self.mistakes[9]}")
            if self.arg_name(index):
                print(f"{self.path_to_file}: Line {index}: {self.mistakes[10]}")
            if self.var_name(index):
                print(f"{self.path_to_file}: Line {index}: {self.mistakes[11]}")
            if self.arg_val(index):
                print(f"{self.path_to_file}: Line {index}: {self.mistakes[12]}")


def main():
    path = sys.argv[1]
    if os.path.isfile(path):
        analyzer = CodeChecker(path)
        analyzer.finding_args_defaults_vals()
        analyzer.analyze()
        return
    os.chdir(path)
    for fle in sorted(os.listdir(path)):
        if not fle.endswith('.py'):
            continue
        path_to_file = f'{path}\\{fle}'
        analyzer = CodeChecker(path_to_file)
        analyzer.finding_args_defaults_vals()
        analyzer.analyze()


if __name__ == '__main__':
    main()
