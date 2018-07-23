# -*- coding: utf-8 -*-
import os

def clean_up() :
    if os.path.isfile("parser.out"): os.remove("parser.out")
    if os.path.isfile("parsetab.py"): os.remove("parsetab.py")
    if os.path.isfile("asp_py_lextab.py"): os.remove("asp_py_lextab.py")
    if os.path.isfile("asp_py_lextab.pyc"): os.remove("asp_py_lextab.pyc")
    if os.path.isfile("asp_py_parsetab.py"): os.remove("asp_py_parsetab.py")
    if os.path.isfile("asp_py_parsetab.pyc"): os.remove("asp_py_parsetab.pyc")


def print_met(predictions) :
    for p in predictions:
        if p.pred() == "xreaction" : print(' ',str(p.arg(0)))
        if p.pred() == "unproducible_target" : print(' ',str(p.arg(0)))
        if p.pred() == "dscope" : print(' ',str(p.arg(0)))
        if p.pred() == "target" : print(' ',str(p.arg(0)))
        if p.pred() == "needed_rxn" : print(' ',str(p.arg(0)))
        if p.pred() == "needed_mrxn" : print(' ',str(p.arg(0)))
        if p.pred() == "selected" : print(' ',str(p.arg(0)))
