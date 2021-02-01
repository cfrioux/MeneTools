# -*- coding: utf-8 -*-

# Copyright (C) 2017-2021 Clémence Frioux & Arnaud Belcour - Inria Dyliss - Pleiade
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.

# You should have received a copy of the GNU Lesser General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>

import os
import logging
import tempfile

logger = logging.getLogger('menetools.utils')


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

def to_file(termset, outputfile=None):
    """write (append) the content of the TermSet into a file
    
    Args:
        termset (TermSet): ASP termset
        outputfile (str, optional): Defaults to None. name of the output file
    """
    if outputfile:
        f = open(outputfile, 'a')
    else:
        fd, outputfile = tempfile.mkstemp(suffix='.lp', prefix='menetools_')
        f = os.fdopen(fd, 'a')
    for t in termset:
        f.write(str(t) + '.\n')
    f.close()
    return outputfile
