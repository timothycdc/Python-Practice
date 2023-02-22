from PLY.yacc import yacc
from PLY.lex import lex
import os
import re
from main import run

passed = 0


def printlog(*args):
    print(*args)
    with open('log.txt', 'a+') as f:
        print(*args, file=f)


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
    '''variable : list
                | element'''
    p[0] = p[1]


def p_list(p):
    '''list : OPENBRACKET elements CLOSEBRACKET'''
    p[0] = p[2]


def p_elements(p):
    '''elements : element COMMA elements
                | element
    '''
    p[0] = []

    if len(p) == 4:
        p[0].append(p[1])
        for item in p[3]:
            p[0].append(item)
    else:
        p[0].append(p[1])


def p_element(p):
    '''element : INT
            | FLOAT
            | STRING
            | BOOL
            | list
    '''
    p[0] = p[1]


def p_error(p):
    print("Parse error!")


def t_error(t):
    #print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)


lexer = lex()
parser = yacc()


# remove all debug outputs
for filename in sorted(os.listdir('output_debug')):
    os.remove(os.getcwd()+"/output_debug/"+filename)

# remove all actual outputs
for filename in sorted(os.listdir('output_actual')):
    os.remove(os.getcwd()+"/output_actual/"+filename)

try:
    os.remove('log.txt')
except:
    printlog("No log file to remove. Continuing...")

# create new blank text file python
with open("log.txt", 'w') as f:
    pass


for filename in sorted(os.listdir('input')):
    with open(os.getcwd()+"/input/"+filename, 'r') as i:
        lines = i.read().splitlines()
        inputs = []
        for line in lines:
            inputs.append(parser.parse(line))
    printlog("")
    printlog(f"==================== Test Case {filename} ====================")

    out_actual_data = run(inputs, filename)

    out_actual_Loc = os.getcwd()+"/output_actual/"+filename
    with open(out_actual_Loc, 'w+') as out_actual:
        print(out_actual_data, file=out_actual)
        out_actual.close()
    printlog("Actual output:")
    printlog(out_actual_data)

    out_expected_Loc = os.getcwd()+"/output_expected/"+filename
    try:
        out_expected_data = []
        with open(out_expected_Loc, 'r') as out_expected:
            # lines = out_expected.readline()
            # for line in lines:
            out_expected_data = parser.parse(out_expected.readline())
            printlog("Expected output:")
            printlog(out_expected_data)
        if out_actual_data == out_expected_data:
            printlog("PASSED")
            passed += 1
        else:
            printlog("FAILED")
        out_expected.close()
    except:
        printlog("Expected output:")
        printlog("ERROR: Expected Test Case File " +
                 filename + " does not exist")
        out_actual.close()
        continue

    out_actual.close()

printlog(
    f"\n\n=== RESULTS =============================================\nTesting Complete. {passed} out of {len(os.listdir('input'))} test cases passed.")
