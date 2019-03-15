from menetools.menescope import cmd_menescope
from menetools.menecheck import cmd_menecheck
from menetools.menecof import cmd_menecof
from menetools.menepath import cmd_menepath
import logging

logging.basicConfig(format='%(message)s', level=logging.DEBUG)
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

def main_menescope(args=None):
    cmd_menescope()

def main_menecheck(args=None):
    cmd_menecheck()

def main_menecof(args=None):
    cmd_menecof()

def main_menepath(args=None):
    cmd_menepath()
