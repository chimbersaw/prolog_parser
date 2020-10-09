#!/usr/bin/env python3
import ply.lex as lex

tokens = [
    'NUM',
    'DELIM',
    'BRACKET',
    'SHTOPOR',
    'OPERATOR',
    'ID',
]


def t_NUM(t):
    r'[0-9]+'
    t.value = int(t.value)
    return t


t_DELIM = r'\.'
t_BRACKET = r'\(|\)'
t_SHTOPOR = r':-'
t_OPERATOR = r',|;'
t_ID = r'[a-zA-Z_][a-zA-Z_0-9]*'

t_ignore = ' \t'


def find_column(input, token):
    line_start = input.rfind('\n', 0, token.lexpos) + 1
    return token.lexpos - line_start + 1


def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)


def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)


def getLex(filename):
    res = []
    lexer = lex.lex()
    with open(filename) as file:
        content = file.readlines()
    content = ''.join(content)

    lexer.input(content)
    file.close()
    while True:
        token = lexer.token()
        if not token:
            break
        res.append([token.type, token.value, token.lineno, find_column(content, token)])
    return res
