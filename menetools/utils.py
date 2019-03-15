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
        if p.pred() == "xreaction" : logger.info(' ' + str(p.arg(0)))
        if p.pred() == "unproducible_target" : logger.info(' ' + str(p.arg(0)))
        if p.pred() == "dscope" : logger.info(' ' + str(p.arg(0)).rstrip('"').lstrip('"'))
        if p.pred() == "target" : logger.info(' ' + str(p.arg(0)))
        if p.pred() == "needed_rxn" : logger.info(' ' + str(p.arg(0)))
        if p.pred() == "needed_mrxn" : logger.info(' ' + str(p.arg(0)))
        if p.pred() == "selected" : logger.info(' ' + str(p.arg(0)))
