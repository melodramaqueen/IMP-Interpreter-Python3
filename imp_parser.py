#!/usr/bin/python3


#Exception https://wiki.python.org/moin/HandlingExceptions
from imp_lexer import *
from combinator import *
from imp_ast import *
from functools import *

'''
This is just a specialized version of the Reserved combinator using the RESERVED tag that all keyword tokens are tagged with. 
Remember, Reserved matches a single token where both the text and tag are the same as the ones given.

def keyword(kw):
    return Reserved(kw, RESERVED)

keyword is actually a combinator because it is a function that returns a parser. We will use it directly in other parsers though.

The id parser is used to match variable names. It uses the Tag combinator, which matches a token with the specified tag.

id = Tag(ID)

The num parser is used to match integers. It works just like id, except we use the Process combinator (actually the ^ operator, 
which calls Process) to convert the token into an actual integer value.

num = Tag(INT) ^ (lambda i: int(i))



The lambda operator or lambda function is a way to create small anonymous functions, i.e. functions without a name. 
These functions are throw-away functions, i.e. they are just needed where they have been created. Lambda functions 
are mainly used in combination with the functions filter(), map() and reduce(). The lambda feature was added to Python 
due to the demand from Lisp programmers.

The general syntax of a lambda function is quite simple:

lambda argument_list: expression

'''

#Basic Parser
def keyword(kw):
	return Reserved(kw, RESERVED)
num = Tag(INT)^(lambda i :int(i))
id = Tag(ID)

def imp_parse(tokens):
	ast = parser()(tokens, 0)
	return ast

def parser():
	return Phrase(stmt_list())

#Statements 
def stmt_list():
	separator = keyword(';')^(lambda x: lambda l, r: CompoundStatement(l,r))
	return Exp(stmt(), separator)

def stmt():
	return assign_stmt() | \
		   if_stmt() | \
		   while_stmt()

def assign_stmt():
    def process(parsed):
        ((name, _), exp) = parsed
        return AssignStatement(name, exp)
    return id + keyword(':=') + aexp() ^ process

def if_stmt():
    def process(parsed):
        (((((_, condition), _), true_stmt), false_parsed), _) = parsed
        if false_parsed:
            (_, false_stmt) = false_parsed
        else:
            false_stmt = None
        return IfStatement(condition, true_stmt, false_stmt)
    return keyword('if') + bexp() + \
           keyword('then') + Lazy(stmt_list) + \
           Opt(keyword('else') + Lazy(stmt_list)) + \
           keyword('end') ^ process

def while_stmt():
    def process(parsed):
        ((((_, condition), _), body), _) = parsed
        return WhileStatement(condition, body)
    return keyword('while') + bexp() + \
           keyword('do') + Lazy(stmt_list) + \
           keyword('end') ^ process


def for_stmt():
    def process(parsed):
        ((((_, condition), _), body), _) = parsed
        return IfStatement(condition, body)
    return keyword('for') + bexp() + \
           keyword('do') + Lazy(stmt_list) + \
           keyword('end') ^ process


# Boolean expressions
def bexp():
    return precedence(bexp_term(),
                      bexp_precedence_levels,
                      process_logic)

def bexp_term():
    return bexp_not()   | \
           bexp_relop() | \
           bexp_group()

def bexp_not():
    return keyword('not') + Lazy(bexp_term) ^ (lambda parsed: NotBexp(parsed[1]))

def bexp_relop():
    relops = ['<', '<=', '>', '>=', '=', '!=']
    return aexp() + any_operator_in_list(relops) + aexp() ^ process_relop

def bexp_group():
    return keyword('(') + Lazy(bexp) + keyword(')') ^ process_group

# Arithmetic expressions
def aexp():
    return precedence(aexp_term(),
                      aexp_precedence_levels,
                      process_binop)

def aexp_term():
    return aexp_value() | aexp_group()

def aexp_group():
    return keyword('(') + Lazy(aexp) + keyword(')') ^ process_group
           
def aexp_value():
    return (num ^ (lambda i: IntAexp(i))) | \
           (id  ^ (lambda v: VarAexp(v)))

# An IMP-specific combinator for binary operator expressions (aexp and bexp)
def precedence(value_parser, precedence_levels, combine):
    def op_parser(precedence_level):
        return any_operator_in_list(precedence_level) ^ combine
    parser = value_parser * op_parser(precedence_levels[0])
    for precedence_level in precedence_levels[1:]:
        parser = parser * op_parser(precedence_level)
    return parser

# Miscellaneous functions for binary and relational operators
def process_binop(op):
    return lambda l, r: BinopAexp(op, l, r)

def process_relop(parsed):
    ((left, op), right) = parsed
    return RelopBexp(op, left, right)

def process_logic(op):
    if op == 'and':
        return lambda l, r: AndBexp(l, r)
    elif op == 'or':
        return lambda l, r: OrBexp(l, r)
    else:
        raise RuntimeError('unknown logic operator: ' + op)

def process_group(parsed):
    ((_, p), _) = parsed
    return p

def any_operator_in_list(ops):
    op_parsers = [keyword(op) for op in ops]
    parser = reduce(lambda l, r: l | r, op_parsers)
    return parser

# Operator keywords and precedence levels
aexp_precedence_levels = [
    ['*', '/'],
    ['+', '-'],
]

bexp_precedence_levels = [
    ['and'],
    ['or'],
]
