import os
import sys
from regex import *         # this will give an error until we finish regex.py


def main():
    
    lines = []
    regex = sys.argv[1] # the regex that will need to be parsed



    test_case_file = open(os.path.join(os.getcwd(), "input_cases.txt"), "r+")
    print("INPUT- - - - - - - - -")
    for line in test_case_file:


        regex_result = False    # parse the test case, return a true or false boolean if it's in the regex. set to false for now.
        lines.append((line[:-1], regex_result)) # appends each line and its boolean to a tuple in the master list
    

    # prints all results 
    for tpl in lines:
        print("RESULTS- - - - - - - - -")
        pass_status = ""
        if tpl[1]:
            pass_status = " : IN REGEX"
        else: pass_status = " : NOT IN REGEX"
        print(tpl[0], pass_status)



