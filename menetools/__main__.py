import logging
import sys

logger = logging.getLogger('menetools')
logger.setLevel(logging.DEBUG)
out_hdlr = logging.StreamHandler(sys.stdout)
out_hdlr.setFormatter(logging.Formatter('%(message)s'))
out_hdlr.setLevel(logging.DEBUG)
logger.addHandler(out_hdlr)
logger.propagate = True

from menetools.menescope import cmd_menescope
from menetools.meneacti import cmd_meneacti
from menetools.menecheck import cmd_menecheck
from menetools.menecof import cmd_menecof
from menetools.menepath import cmd_menepath

def main_menescope(args=None):
    cmd_menescope()

def main_meneacti(args=None):
    cmd_meneacti()

def main_menecheck(args=None):
    cmd_menecheck()

def main_menecof(args=None):
    cmd_menecof()

def main_menepath(args=None):
    cmd_menepath()
