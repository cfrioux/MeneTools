# -*- coding: utf-8 -*-
import os
import logging

logger = logging.getLogger(__name__)


def clean_up() :
    if os.path.isfile("parser.out"): os.remove("parser.out")
    if os.path.isfile("parsetab.py"): os.remove("parsetab.py")
    if os.path.isfile("asp_py_lextab.py"): os.remove("asp_py_lextab.py")
    if os.path.isfile("asp_py_lextab.pyc"): os.remove("asp_py_lextab.pyc")
    if os.path.isfile("asp_py_parsetab.py"): os.remove("asp_py_parsetab.py")
    if os.path.isfile("asp_py_parsetab.pyc"): os.remove("asp_py_parsetab.pyc")


def print_met(predictions) :
    for p in predictions:
        if p.pred() == "xreaction" : logging.info(' ' + str(p.arg(0)))
        if p.pred() == "unproducible_target" : logging.info(' ' + str(p.arg(0)))
        if p.pred() == "dscope" : logging.info(' ' + str(p.arg(0)).rstrip('"').lstrip('"'))
        if p.pred() == "target" : logging.info(' ' + str(p.arg(0)))
        if p.pred() == "needed_rxn" : logging.info(' ' + str(p.arg(0)))
        if p.pred() == "needed_mrxn" : logging.info(' ' + str(p.arg(0)))
        if p.pred() == "selected" : logging.info(' ' + str(p.arg(0)))
