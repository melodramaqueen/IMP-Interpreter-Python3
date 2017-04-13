#!/usr/bin/python3
'''.isinstance(object, classinfo) -- -- -- Return true if the object argument is an instance of the classinfo argument, 
or of a (direct, indirect or virtual) subclass thereof. If object is not an object of the given type, the function 
always returns false. If classinfo is a tuple of type objects (or recursively, other such tuples), return true if object 
is an instance of any of the types. If classinfo is not a type or tuple of types and such tuples, a TypeError exception is raised.

'''
class Equality:
	def __eq__(self,other):
		return isinstance(other, self.__class__) and \
				self.__dict__ == other.__dict__
	def __ne__(self,other):
		return not self.__eq__(other)