from typing import NamedTuple
import itertools
import re


class TreeNode:
    def __init__(self, name, parent=None):
        self.name = name
        self.parent = parent
        self.children = []
        self.cached_size = None
    
    def add_child(self, other):
        self.children.append(other)
    
    def calculate_size(self):
        if self.cached_size is not None:
            return self.cached_size

        def child_size(child):
            if isinstance(child, File):
                return child.size
            return child.calculate_size()
        self.cached_size = sum(map(child_size, self.children))
        return self.cached_size
    
    def enumerate_dirs_dfs(self):
        yield self
        for child in self.children:
            if isinstance(child, TreeNode):
                yield from child.enumerate_dirs_dfs()
    

class File(NamedTuple):
    name: str
    size: int


class TerminalParser:
    def __init__(self, input):
        self.__input = input
        self.root = TreeNode('/')
        self.current_dir = None
        self.line_idx = 0
    
    def parse(self):
        while self.line_idx < len(self.__input):
            self.__parse_command(self.__input[self.line_idx])
        return self.root
    
    def __parse_command(self, command):
        command_stripped = command.replace('$ ', '')
        self.line_idx += 1
        if command_stripped == 'ls':
            self.__list_directory()
        else:
            self.__change_directory(command_stripped.replace('cd ', ''))
    
    def __list_directory(self):
        content = self.__collect_listed_content()
        for item in content:
            self.current_dir.add_child(self.__convert_directory_item(item))

    def __change_directory(self, dir):
        if dir == '/':
            self.current_dir = self.root
        elif dir == '..':
            self.current_dir = self.current_dir.parent
        else:
            self.current_dir = next(filter(lambda x: x.name == dir, self.current_dir.children))

    def __collect_listed_content(self):
        content = list(itertools.takewhile(lambda l: l[0] != '$', self.__input[self.line_idx:]))
        self.line_idx += len(content)
        return content
    
    def __convert_directory_item(self, line):
        dir_match = re.match(r'dir (.+)', line)
        if dir_match is not None:
            return TreeNode(dir_match.group(1), self.current_dir)
        file_match = re.match(r'(\d+) (.+)', line)
        size, file_name = file_match.groups()
        return File(file_name, int(size))


def resolve_part1(input):
    root = TerminalParser(input).parse()
    return sum(filter(lambda x: x <= 100000, (node.calculate_size() for node in root.enumerate_dirs_dfs())))


def resolve_part2(input):
    root = TerminalParser(input).parse()
    free_space = 70000000 - root.calculate_size()
    missing_space = 30000000 - free_space

    sizes = sorted(node.calculate_size() for node in root.enumerate_dirs_dfs())
    return next(filter(lambda x: x >= missing_space, sizes))
