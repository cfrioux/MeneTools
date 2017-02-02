# Copyright (c) 2012, Sven Thiele <sthiele78@gmail.com>
#
# This file is part of pyasp.
#
# pyasp is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# pyasp is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with pyasp.  If not, see <http://www.gnu.org/licenses/>.import random

# -*- coding: utf-8 -*-
from __future__ import print_function
import re
import tempfile
import os
import subprocess
import threading
from pyasp.misc import *
import pyasp.ply.lex as lex
import pyasp.ply.yacc as yacc
import errno
import json

root = __file__.rsplit('/', 1)[0]

global optimize
# use 0 for debugging
# use 1 for speed (run python once without -O or -OO and then with -O or -OO)
optimize=1
import sys
if sys.flags.optimize in ['-O', '-OO'] and optimize == 0:
  raise RuntimeError("need to use optimize=1 and run python without -O or -OO once to make parsers work")

def debug(s):
  import inspect
  print("DBG %03d: %s" % \
    (inspect.currentframe().f_back.f_lineno,s), file=sys.stderr)


# mutable and not hashable!
class TermSet(set):
    def __init__(self, terms=[]):
        super(TermSet, self).__init__(terms)
        self.score = None
        
    def filter(self,f):
        accu = TermSet()
        for e in self:
            if f(e): accu.add(e)
        return accu
    def to_list(self):
        ret = []
        for t in self: ret.append(t)
        return ret
    def to_file(self,fn=None):
        if fn:
            file = open(fn,'w')
        else:
            fd, fn = tempfile.mkstemp('.lp')
            file = os.fdopen(fd,'w')
        for t in self:
            #print str(t)
            file.write(str(t) + '.\n')
        file.close()
        return fn
    def exclude_rule(self):
        return ':- ' + ','.join(map(str,self)) + '.'
    def __hash__(self):
        raise "TermSet is mutable and not hashable!"

# immutable and hashable
class Term:
    """an ASP term (used for atoms and for function terms)"""
    def __init__(self,predicate,arguments=[]):
        self.predicate = predicate
        self.arguments = arguments

    def nb_args(self): 
        return len(self.arguments)

    def arg(self,n): 
        return self.arguments[n]
    
    def args(self): 
        return self.arguments

    def pred(self): 
        return self.predicate

    def explode(self):
      return [ self.pred() ] + self.arguments

    def __repr__(self):
        if len(self.arguments) == 0:
            return "Term(%s)" % (repr(self.predicate),)
        else:
            return "Term(%s,[%s])" % (repr(self.predicate),",".join(map(repr,self.arguments)))
    
    def __str__(self):
        if len(self.arguments) == 0:
            return self.predicate
        else:
            return self.predicate + "(" + ",".join(map(str,self.arguments)) + ")"
    
    def __hash__(self):
        return tuple([self.predicate] + self.arguments).__hash__()
    
    def __eq__(self,other):
        return self.predicate == other.predicate and self.arguments == other.arguments
    
    def sip(self,s):
        """sip = string in predicate"""
        return (s in self.predicate)
    
    def p(self,s):
        return (s == self.predicate)

class Lexer:
    tokens = (
        'STRING',
        'IDENT',
        'MIDENT',
        'NUM',
        'LP',
        'RP',
        'COMMA',
        'SPACE',
    )

    # Tokens
    t_STRING = r'"((\\")|[^"])*"'
    t_IDENT = r'[a-zA-Z_][a-zA-Z0-9_]*'
    t_MIDENT = r'-[a-zA-Z_][a-zA-Z0-9_]*'
    t_NUM = r'-?[0-9]+'
    t_LP = r'\('
    t_RP = r'\)'
    t_COMMA = r','
    t_SPACE = r'[ \t\.]+'

    def __init__(self):
        global optimize
        self.lexer = lex.lex(object=self,optimize=optimize, lextab='asp_py_lextab')

    def t_newline(self, t):
        r'\n+'
        t.lexer.lineno += t.value.count("\n")

    def t_error(self, t):
        print("Illegal character "+str(t.value[0]))
        t.lexer.skip(1)

class Parser:
    start = 'answerset'

    def __init__(self,collapseTerms=True,collapseAtoms=False, callback=None):
        """
        collapseTerms: function terms in predicate arguments are collapsed into strings
        collapseAtoms: atoms (predicate plus terms) are collapsed into strings
                       requires that collapseTerms is True

        example: a(b,c(d))
        collapseTerms=True,  collapseAtoms=False: result = Term('a', ['b', 'c(d)'])
        collapseTerms=True,  collapseAtoms=True:  result = 'a(b,c(d))'
        collapseTerms=False, collapseAtoms=False: result = Term('a', ['b', Term('c', ['d'])])
        collapseTerms=False, collapseAtoms=True: invalid arguments
        """
        global optimize
        self.accu = TermSet()
        self.lexer = Lexer()
        self.tokens = self.lexer.tokens
        self.collapseTerms = collapseTerms
        self.collapseAtoms = collapseAtoms
        self.callback = callback

        if collapseAtoms and not collapseTerms:
            raise "if atoms are collapsed, functions must also be collapsed!"
        
        self.parser = yacc.yacc(module=self, optimize=optimize, tabmodule='asp_py_parsetab')

    def p_answerset(self, t):
        """answerset : atom SPACE answerset
                   | atom
        """
        self.accu.add(t[1])

    def p_atom(self, t):
        """atom : IDENT LP terms RP
                | IDENT
                | MIDENT LP terms RP
                | MIDENT
        """
        if self.collapseAtoms:
            if len(t) == 2:
                t[0] = str(t[1])
            elif len(t) == 5:
                t[0] = "%s(%s)" % ( t[1], ",".join(map(str,t[3])) )
        else:
            if len(t) == 2:
                t[0] = Term(t[1])
            elif len(t) == 5:
                t[0] = Term(t[1], t[3])

    def p_terms(self, t):
        """terms : term COMMA terms
                 | term
        """
        if len(t) == 2:
            t[0] = [t[1]]
        else:
            t[0] = [t[1]] + t[3]

    def p_term(self, t):
        """term : IDENT LP terms RP
                | STRING
                | IDENT
                | NUM
        """
        if self.collapseTerms:
            if len(t) == 2:
                t[0] = t[1]
            else:
                t[0] = t[1] + "(" + ",".join(t[3]) + ")"
        else:
            if len(t) == 2:
                if re.match(r'-?[0-9]+', t[1]) != None:
                    t[0] = int(t[1])
                else:
                    t[0] = t[1]
            else:
                t[0] = Term(t[1], t[3])

    def p_error(self, t):
        print("Syntax error at "+str(t))
        import inspect
        print (''.join(map(lambda x: "  %s:%s\n    %s" % (x[1], x[2], x[4][0]),inspect.stack())))

    def parse(self, line):
        self.accu = TermSet()
        line = line.strip()
    
        if len(line) > 0:
            self.parser.parse(line, lexer=self.lexer.lexer)

        if self.callback:
            self.callback(self.accu)
        
        return self.accu

def filter_empty_str(l):
    return [x for x in l if x != '']

class String2TermSet(TermSet):
    def __init__(self,s):
        re.sub(r'\).\s*',") ",s)
        p = Parser(True, False)
        atoms = p.parse(s)
        TermSet.__init__(self,atoms)
    
def exclude_sol(sols,fn=None):
    if fn:
        file = open(fn,'w')
    else:
        fd, fn = tempfile.mkstemp('.lp')
        file = os.fdopen(fd,'w')
    for s in sols:
        file.write(s.exclude_rule() + '\n')
        
    file.close()
    return fn
        
class GringoClaspBase(object):
    def __init__(self, clasp_bin = root + '/bin/clasp', clasp_options = '',
                       gringo_bin = root + '/bin/gringo3', gringo_options = '',
                       optimization = False):
        self.clasp_bin = clasp_bin
        self.gringo_bin = gringo_bin
        self.clasp_options = clasp_options
        self.gringo_options = gringo_options
        self._clasp = None
        self._gringo = None
        self.clasp_stderr = None
        self.gringo_stderr = None
        self.clasp_noerror_retval = set([10, 20, 30])
        self.gringo_noerror_retval = set([0])
        
        if clasp_options.find('--opt-all') != -1:
            #workaround for backwards compatibility
            optimization = True
        
        self.optimization = optimization
        
    def __parse_witnesses__(self, parser, witnesses):
        accu = []
        for answer in witnesses:
            ts = parser.parse(" ".join(answer['Value']))
            if 'Costs' in answer:
                ts.score = answer['Costs']
                
            accu.append(ts)
            
        return accu
        
    def __get_witnesses_key__(self,result):
        key = 'Value'
        if 'Brave' in result['Models']:
            key = 'Brave'
        elif 'Cautious' in result['Models']:
            key = 'Cautious'
            
        return key
        
    def __ground__(self, programs, additionalProgramText):
        try:
            additionalPrograms = []
            if additionalProgramText != None:
                (fd, fn) = tempfile.mkstemp('.lp')
                file = os.fdopen(fd,'w')
                file.write(str(additionalProgramText))
                file.close()
                additionalPrograms.append(fn)
              
            addoptions = []
            if self.gringo_options:
                addoptions = self.gringo_options.split()

            commandline = filter_empty_str([self.gringo_bin] + addoptions + programs + additionalPrograms)
            self._gringo = subprocess.Popen(commandline, stderr=subprocess.PIPE, stdout=subprocess.PIPE)
            
        except OSError as e:
            if e.errno == 2:
                raise Exception('Grounder \'%s\' not found' % self.gringo_bin)
            else: 
                raise e
                
        (grounding,self.gringo_stderr) = self._gringo.communicate()
        if self._gringo.returncode not in self.gringo_noerror_retval:
            raise Exception("got error %d from gringo: '%s'" % \
                (self._gringo.returncode, self.gringo_stderr))
                
        return grounding
                        
    def __solve__(self, grounding, opts = [], json=True):
        try:
            #opts = opts + ['--stats']
            addoptions = []
            if self.clasp_options:
                addoptions = self.clasp_options.split()

            if json:
                opts = opts + ['--outf=2']
            self._clasp = subprocess.Popen(
                filter_empty_str([self.clasp_bin] + addoptions  + opts),
                stdin=subprocess.PIPE,
                stderr=subprocess.PIPE,
                stdout=subprocess.PIPE)
                
        except OSError as e:
            if e.errno == 2:
                raise Exception('Solver \'%s\' not found' % self.clasp_bin)
            else: 
                raise e
                
        (solving,self.clasp_stderr) = self._clasp.communicate(grounding)
        self.clasp_stderr = solving + self.clasp_stderr
        
        if self._clasp.returncode not in self.clasp_noerror_retval:
            raise Exception("got error %d from clasp: '%s' gringo: '%s'" % \
                (self._clasp.returncode, self.clasp_stderr, self.gringo_stderr))
                    
        self._clasp = None
        self._gringo = None
        
        return solving
                
    def run(self, programs, collapseTerms=True, collapseAtoms=True, additionalProgramText=None, callback=None):
        grounding = self.__ground__(programs, additionalProgramText)

        solving = self.__solve__(grounding)
        
        parser = Parser(collapseTerms,collapseAtoms,callback)
        res = json.loads(solving.decode())
        key = self.__get_witnesses_key__(res)

        if res['Result'] == "SATISFIABLE":
            if key == 'Value':
                witnesses = res['Call'][0]['Witnesses']
            else:
                witnesses = [res['Call'][0]['Witnesses'][-1]]

            accu = self.__parse_witnesses__(parser, witnesses)            
                
        elif res['Result'] == "OPTIMUM FOUND":
            if key == 'Value':
                numopts= res['Models']['Optimal']
                if numopts==0 :
                    print('WARNING: OPTIMUM FOUND but zero optimals')
                    witnesses=[]
                else :
                    offset =len(res['Call'][0]['Witnesses'])-numopts
                    witnesses = res['Call'][0]['Witnesses'][offset:]

            else:
                witnesses = [res['Call'][0]['Witnesses'][-1]]

            accu = self.__parse_witnesses__(parser, witnesses)
            
        else:
            accu = []

        return accu

class GringoClasp(GringoClaspBase):
    pass

class Gringo4Clasp(GringoClaspBase):
    def __init__(self, clasp_bin = root + '/bin/clasp', clasp_options = '',
                       gringo_bin = root + '/bin/gringo4', gringo_options = '',
                       optimization = False):
        self.clasp_bin = clasp_bin
        self.gringo_bin = gringo_bin
        self.clasp_options = clasp_options
        self.gringo_options = gringo_options
        self._clasp = None
        self._gringo = None
        self.clasp_stderr = None
        self.gringo_stderr = None
        self.clasp_noerror_retval = set([10, 20, 30])
        self.gringo_noerror_retval = set([0])

        if clasp_options.find('--opt-all') != -1:
            #workaround for backwards compatibility
            optimization = True

        self.optimization = optimization        
