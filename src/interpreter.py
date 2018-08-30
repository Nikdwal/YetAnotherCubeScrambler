import cube
import re
import random

class Interpreter:
    def __init__(self, file, cube : cube.Cube):
        with open(file) as f:
            self._program = f.readlines()
        self._program_counter = 0
        self._cube = cube
        self._end_of_alternatives = 0

        # Remove the comments on all the lines, as well as any double or leading whitespaces
        for i in range(len(self._program)):
            self._program[i] = re.sub(r'#.*','',self._program[i].lstrip()).replace("  ", " ")

    def execute_program(self):
        while self._program_counter < len(self._program):
            line = self._program[self._program_counter]
            if line[0] == "[":
                self._start_alternatives()
            elif self._is_delimiter_of_alternatives(line):
                # We were executing one of the options in a list of alternatives. This marks the end and we can jump forward.
                self._program_counter = self._end_of_alternatives
            else:
                # This is a regular single line command
                self._execute_regular_command()

    @staticmethod
    def _is_delimiter_of_alternatives(line):
        return line[:1].lstrip().lower() == "or"

    def _start_alternatives(self):
        stack = 0
        jump_locations = [self._program_counter + 1]
        for i in range(self._program_counter, len(self._program)):
            line = self._program[self._program_counter]

            if stack == 1 and self._is_delimiter_of_alternatives(line):
                # This is one of the alternatives in this alternative switch block. Remember it.
                jump_locations.append(i + 1)
            elif line[0] == "[":
                stack += 1
            elif line[0] == "]":
                stack -= 1
                if stack == 0:
                    self._end_of_alternatives = i + 1
                    break

        # Jump to any of the alternatives listed in this alternatives block.
        self._program_counter = random.choice(jump_locations)



