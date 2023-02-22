from PLY.lex import lex
from PLY.yacc import yacc


def parse(inputStr):

    tokens = ('INT', 'FLOAT', 'STRING', 'BOOL',
              'OPENBRACKET', 'CLOSEBRACKET', 'COMMA')

    t_OPENBRACKET = r'\['
    t_CLOSEBRACKET = r'\]'
    t_COMMA = r','

    def t_FLOAT(t):
        r'-?\d+\.\d+'
        t.value = float(t.value)
        return t

    def t_INT(t):
        r'-?\d+'
        t.value = int(t.value)
        return t

    def t_STRING(t):
        r'\".*?\"|\'.*?\''
        t.value = str(t.value)[1:-1]
        return t

    def t_BOOL(t):
        r'True|False'
        if t.value == 'True':
            t.value = True
        else:
            t.value = False
        return t

    def p_variable(p):
        '''variable : OPENBRACKET elements CLOSEBRACKET
                    | element'''
        if len(p) == 2:
            p[0] = p[1]
        else:
            p[0] = p[2]

    def p_elements(p):
        '''elements : element COMMA element
                    | elements COMMA element
        '''
        p[0] = []
        if isinstance(p[1], list):
            for item in p[1]:
                p[0].append(item)
            p[0].append(p[3])
        else:
            p[0].append(p[1])
            p[0].append(p[3])

    def p_element(p):
        '''element : INT
                | FLOAT
                | STRING
                | BOOL
        '''
        p[0] = p[1]

    def p_error(p):
        print("Syntax error in input!")

    def t_error(t):
        #print("Illegal character '%s'" % t.value[0])
        t.lexer.skip(1)

    lexer = lex()
    parser = yacc()

    return parser.parse(inputStr)


#     print(ast)
#     for item in ast:
#         print(item, type(item))

# ast = parser.parse('False')
# print(ast, type(ast))

# ast = parser.parse('324145')
# print(ast, type(ast))

# ast = parser.parse('"324145"')
# print(ast, type(ast))

# ast = parser.parse("'324145'")
# print(ast, type(ast))
