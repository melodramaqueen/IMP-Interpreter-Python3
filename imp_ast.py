#!/usr/bin/python3
'''
Every syntactic element of IMP will have a corresponding class. Objects of these classes will represent nodes in the AST.

There are three kinds of structures in IMP: arithmetic expressions (used to compute numbers), Boolean expressions 
(used to compute conditions for if- and while-statements), and statements. We will start with arithmetic expressions, 
since the other two elements depend on them.

An arithmetic expression can take one of three forms:

    Literal integer constants, such as 42
    Variables, such as x
    Binary operations, such as x + 42. These are made out of other arithmetic expressions.

We can also group expressions together with parenthesis (like (x + 2) * 3. This isn't a different kind of expression so much
 as a different way to parse the expression.

We will define three classes for these forms, plus a base class for arithmetic expressions in general. For now, the classes
won't do much except contain data. We will include a __repr__ method, so we can print out the AST for debugging. 
All AST classes will subclass Equality so we can check if two AST objects are the same. This helps with testing.


The environment is also easy. IMP only has global variables, so we can model the environment with a simple Python dictionary. 
Whenever an assignment is made, we will update the variable's value in the dictionary.


'''


#https://docs.python.org/3/library/functions.html

from equality import *

#Arithematic Expression
class Aexp(Equality):
	pass

#Boolean Expression
class Bexp(Equality):
	pass

#Statement 
class Statement(Equality):
	pass

#Integer Aexp --     Literal integer constants, such as 42
class IntAexp(Aexp):
	def __init__(self, i):
		self.i = i
	def __repr__(self):
		return ('IntrAexp(%d)' %self.i)
	def eval(self, env):
		return self.i

#Var / String --     Variables, such as x
class VarAexp(Aexp):
	def __init__(self, name):
		self.name = name
	def __repr__(self):
		return ('VarAexp(%s)' %self.name)
	def eval(self, env):
		if self.name in env:
			return env[self.name]
		else: return 0


#Two operation Arithematic Exp  --  Binary operations, such as x + 42. These are made out of other arithmetic expressions.
class BinopAexp(Aexp):
	def __init__(self, op, left, right):
		self.op = op
		self.left = left
		self.right =right
	def __repr__(self):
		return ('BinopAexp (%s, %s, %s)' %(self.op, self.left, self.right))
	def eval(self, env):
		left_value = self.left.eval(env)
		right_value = self.right.eval(env)
		if self.op == '+':
			value = left_value + right_value
		elif self.op == '-':
			value = left_value - right_value
		elif self.op == '*':
			value = left_value * right_value
		elif self.op == '/':
			try:
				value = left_value/right_value
			except ZeroDivisionError:
				print("Division by zero!")
		else : 
			raise RuntimeError('unknown operator: '+self.op)
		return value

#Relational Operator Noolean Expression
class RelopBexp(Bexp):
	def __init__(self, op, left, right):
		self.op = op
		self.right = right
		self.left = left
	def __repr__(self):
		return ('RelopBexp (%s, %s, %s)' %(self.op, self.left, self.right))
	def eval(self, env):
		left_value = self.left.eval(env)
		right_value = self.right.eval(env)
		if self.op == '>':
			value = left_value > right_value
		elif self.op == '<':
			value = left_value < right_value
		elif self.op == '==':
			value = left_value == right_value
		elif self.op == '!=':
			value = left_value != right_value
		elif self.op == '<=':
			value = left_value <= right_value
		elif self.op == '>=':
			value = left_value >= right_value
		else : 
			raise RuntimeError('unknown operator: '+ self.op)
		return value

class AndBexp(Bexp):
	def __init__(self, left, right):
		self.left = left
		self.right = right
	def __repr__(self):
		return ('AndBexp (%s, %s)' %(self.left, self.right))
	def eval(self, env):
		left_value = self.left.eval(env)
		right_value = self.right.eval(env)
		return (left_value and right_value)

class OrBexp(Bexp):
	def __init__(self, left,right):
		self.left = left
		self.right = right
	def __repr__(self):
		return ('OrBexp (%s, %s)' %(self.left, self.right))
	def eval(self, env):
		left_value = self.left.eval(env)
		right_value = self.right.eval(env)
		return (left_value or right_value)

class NotBexp(Bexp):
	def __init__(self, exp):
		self.exp = exp
	def __repr__(self):
		return ('NotBexp (%s)' %(self.exp))
	def eval(self, env):
		value = self.exp.eval(env)
		return (not value)

class AssignStatement(Statement):
	def __init__(self, name, aexp):
		self.name = name
		self.aexp = aexp
	def __repr__(self):
		return ('AssignStatement (%s, %s)' %(self.name, self.exp))
	def eval(self, env):
		value = self.aexp.eval(env)
		env[self.name] = value

class CompoundStatement(Statement):
	def __init__(self, first, second):
		self.first = first
		self.second = second
	def __repr__(self):
		return ('CompoundStatement (%s, %s)' %(self.first, self.second))
	def eval(self, env):
		self.first.eval(env)
		self.second.eval(env)

class IfStatement(Statement):
	def __init__(self, condition, true_statement, false_statement):
		self.condition = condition
		self.true_statement = true_statement
		self.false_statement = false_statement
	def __repr__(self):
		return ('IfStatement (%s, %s, %s)' %(self.condition, self.true_statement, self.false_statement))
	def eval(self, env):
		condition_value = self.condition.eval(env)
		if condition_value:
			self.true_statement.eval(env)
		else :
			if false_value:
				self.false_value.eval(env)

class WhileStatement(Statement):
	def __init__(self, condition, body):
		self.condition = condition
		self.body = body
	def __repr__(self):
		return ('WhileStatement (%s, %s)' %(self.condition, self.body))
	def eval(self, env):
		condition_value = self.condition.eval(env)
		while condition_value:
			self.body.eval(env)
			condition_value = self.condition.eval(env)


class ForStatement(Statement):
	def __init__(self, condition, body):
		self. condition = condition
		self.body = body
	def __repr__(self):
		return ('forStatement (%s, %s)' %(self.condition, self.body))
	def eval(self,env):
		condition_value = self.condition.eval(env)
		while condition_value:
			self.body.eval(env)
			condition_value = self.condition.eval(env)

class PrintStatement(Statement):
	def __init__(self, body):
		self.body = body
	def __repr__(self):
		return ('PrintStatement (%s)' %(self.body)) 
	def eval(self,env):
		print (self.body.eval(env))



'''
n := 5;
p := 1;
while n > 0 do
  p := p * n;
  n := n - 1
end


'''