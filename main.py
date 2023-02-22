import math
import os
import re
import sys

# open every text file from the input folder


def run(inputs, filename):
    orig_stdout = sys.stdout
    debug = open(os.getcwd()+"/output_debug/"+filename, 'w')
    sys.stdout = debug
    ans = main(inputs)
    debug.close()
    sys.stdout = orig_stdout
    return ans


def main(inputs):
    # add your code submission here
    # don't forget to return the answer!




    # example program: print the list of inputs
    # if first two inputs are an integer, return its sum
    # otherwise return the list of inputs
    for item in inputs:
        print(item, type(item))
    a = inputs[0]
    b = inputs[1]
    c = inputs[2]
    if isinstance(a, int) and isinstance(b, int):
        return(a+b)
    else:
        return(inputs)
    # end of example program. you can delete the code sandwiched between the two comments
    

    return inputs
