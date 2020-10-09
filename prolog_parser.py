#!/usr/bin/env python3
import sys
from lex import getLex


class Parser:
    def __init__(self):
        self.s = None
        self.end = False
        self.ignore = False
        self.i = 0

    def increment(self):
        self.i += 1
        if self.i >= len(self.s):
            self.end = True

    def error(self):
        if self.ignore:
            return False
        if self.end:
            raise Exception('Syntax error: unexpected end of file')
        else:
            line = str(self.s[self.i][2])
            colon = str(self.s[self.i][3])
            raise Exception('Syntax error: line ' + line + ', colon ' + colon)

    def check_end(self):
        if self.end:
            self.ignore = False
            self.error()

    def parse_with_ignore(self, parse):
        ignore_was = self.ignore
        self.ignore = True
        res = parse()
        self.ignore = ignore_was
        return res

    def parse_list(self, parse_item, parse_sep):
        if self.end:
            return True
        parse_item()
        if not self.parse_with_ignore(parse_sep):
            return True
        parse_sep()
        return self.parse_list(parse_item, parse_sep)

    def parse_element(self, pos, name):
        self.check_end()
        if self.s[self.i][pos] != name:
            return self.error()
        else:
            if not self.ignore:
                self.increment()
            return True

    def parse_dot(self):
        return self.parse_element(1, '.')

    def parse_ID(self):
        return self.parse_element(0, 'ID')

    def parse_shtopor(self):
        return self.parse_element(0, 'SHTOPOR')

    def parse_semicolon(self):
        return self.parse_element(1, ';')

    def parse_comma(self):
        return self.parse_element(1, ',')

    def parse_opening_bracket(self):
        return self.parse_element(1, '(')

    def parse_closing_bracket(self):
        return self.parse_element(1, ')')

    def parse_brackets(self):
        self.parse_opening_bracket()
        self.parse_body()
        self.parse_closing_bracket()

    def parse_atom(self):
        if self.parse_with_ignore(self.parse_opening_bracket):
            self.parse_brackets()
        else:
            self.parse_ID()

    def parse_M(self):
        # M -> (ID,)*ID
        # , = *
        self.parse_list(self.parse_atom, self.parse_comma)

    def parse_body(self):
        # BODY -> (M;)*M
        # ; = +
        self.parse_list(self.parse_M, self.parse_semicolon)

    def parse_R(self):
        self.parse_ID()
        if not self.parse_with_ignore(self.parse_dot):
            self.parse_shtopor()
            self.parse_body()
        return True

    def parse_S(self, s):
        self.s = s
        self.end = len(s) == 0
        try:
            while not self.end:
                self.parse_R()
                self.check_end()
                self.parse_dot()
        except Exception as e:
            print(e)
            return 1
        print('No errors occurred.')
        return 0


def main(args):
    s = getLex(args[0])
    parser = Parser()
    return parser.parse_S(s)


if __name__ == '__main__':
    main(sys.argv[1:])
