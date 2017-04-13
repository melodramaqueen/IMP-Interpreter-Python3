#!/usr/bin/python3
import lexer
import sys
import re

def lex(characters, token_exprs):
	pos = 0
	tokens = []
	while pos<len(characters):
		match = None
		for token_expr in token_exprs:
			pattern, tag = token_expr
			regex = re.compile(pattern) #https://pymotw.com/2/re/
			match = regex.match(characters,pos) #https://pymotw.com/2/re/
			if match:
				text = match.group(0)
				if tag: 
					token = (text,tag)
					tokens.append(token) 
				break 
		if not match:
			sys.stderr.write("Illegal character : %s\n" %characters[pos]) #throw an error
			sys.exit(1) 
		else :
			pos = match.end(0)
	return tokens