#!/usr/bin/python3
import sys
import imp_lexer 

#https://docs.python.org/3/library/sys.html
if __name__=='main':
	filename = sys.argv[1]
	file = open('hello.imp')
	characters = file.read()
	file.close()
	tokens = imp_lexer.imp_lex(characters)
	for token in tokens:
		print(token)

'''

sys.argv

    The list of command line arguments passed to a Python script. argv[0] is the script name (it is operating system dependent 
    whether this is a full pathname or not). If the command was executed using the -c command line option to the interpreter, 
    argv[0] is set to the string '-c'. If no script name was passed to the Python interpreter, argv[0] is the empty string.

    To loop over the standard input, or the list of files given on the command line, see the fileinput module.

'''
