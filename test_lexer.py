#!/usr/bin/python3

import unittest
from lexer import *

KEYWORD = 'KEYWORD'
INT = 'INT'
ID = 'ID'
token_exprs = [
    (r'[ \t\n]+', None),
    (r'#[^\n]*', None),
    (r'keyword', KEYWORD),
    (r'[0-9]+', INT),
    (r'[A-Za-z][A-Za-z0-9_]*', ID)
]

class TestLexer(unittest.TestCase):
    def lexer_test(self, code, expected):
        actual = lex(code, token_exprs)
        self.assertEquals(expected, actual)

    def test_empty(self):
        self.lexer_test('', [])

    def test_id(self):
        self.lexer_test('abc', [('abc', ID)])

    def test_keyword_first(self):
        self.lexer_test('keyword', [('keyword', KEYWORD)])

    def test_space(self):
        self.lexer_test(' ', [])

    def test_id_space(self):
        self.lexer_test('abc def', [('abc', ID), ('def', ID)])


'''
The unittest module provides a rich set of tools for constructing and running tests. 
This section demonstrates that a small subset of the tools suffice to meet the needs of most users.


 assertEqual(first, second, msg=None)

    Test that first and second are equal. If the values do not compare equal, the test will fail.

    In addition, if first and second are the exact same type and one of list, tuple, dict, set, frozenset 
    or str or any type that a subclass registers with addTypeEqualityFunc() the type-specific equality 
    function will be called in order to generate a more useful default error message (see also the list of type-specific methods).



assertEqual(a, b)               a == b   
assertNotEqual(a, b)            a != b   
assertTrue(x)                   bool(x) is True      
assertFalse(x)                  bool(x) is False     
assertIs(a, b)                  a is b  
assertIsNot(a, b)               a is not b  
assertIsNone(x)                 x is None   
assertIsNotNone(x)              x is not None   
assertIn(a, b)                  a in b  
assertNotIn(a, b)               a not in b  
assertIsInstance(a, b)          isinstance(a, b)    
assertNotIsInstance(a, b)       not isinstance(a, b)   

'''