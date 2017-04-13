#!/usr/bin/python3
import sys
from imp_parser import *

if __name__=='main':
	if len(sys.argv) != 3:
		sys.stderr.write('usage : %s filename parsername \n' %sys.argv[0])
		sys.exit(1)
	filename = sys.argv[1]
	file = open(filename)
	characters = file.read()
	file.close()
	tokens = imp_lex(characters)
    parser = globals()[sys.argv[2]]()
    result = parser(tokens, 0)
    print result

#https://docs.python.org/3/library/sys.html


'''

sys.argv

    The list of command line arguments passed to a Python script. argv[0] is the script name (it is operating system dependent 
    whether this is a full pathname or not). If the command was executed using the -c command line option to the interpreter, 
    argv[0] is set to the string '-c'. If no script name was passed to the Python interpreter, argv[0] is the empty string.

    To loop over the standard input, or the list of files given on the command line, see the fileinput module.

'''


'''

 sys.stdin
sys.stdout
sys.stderr

    File objects used by the interpreter for standard input, output and errors:

        stdin is used for all interactive input (including calls to input());
        stdout is used for the output of print() and expression statements and for the prompts of input();
        The interpreter’s own prompts and its error messages go to stderr.


'''