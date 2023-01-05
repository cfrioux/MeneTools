# Copyright (C) 2017-2023 Clémence Frioux & Arnaud Belcour - Inria Dyliss - Pleiade
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

import argparse
import logging
import pkg_resources
import sys
import time

logger = logging.getLogger('menetools')
logger.setLevel(logging.DEBUG)
out_hdlr = logging.StreamHandler(sys.stdout)
out_hdlr.setFormatter(logging.Formatter('%(message)s'))
out_hdlr.setLevel(logging.DEBUG)
logger.addHandler(out_hdlr)
logger.propagate = True

from menetools.menescope import run_menescope
from menetools.meneacti import run_meneacti
from menetools.menecheck import run_menecheck
from menetools.menecof import run_menecof
from menetools.menepath import run_menepath
from menetools.menedead import run_menedead
from menetools.meneseed import run_meneseed
from menetools.menescope_inc import run_menescope_inc
from shutil import which

VERSION = pkg_resources.get_distribution("menetools").version
LICENSE = """Copyright (C) Clémence Frioux & Arnaud Belcour - Inria Dyliss - Pleiade
This program is free software: you can redistribute it and/or modify
it under the terms of the GNU Lesser General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU Lesser General Public License for more details.

You should have received a copy of the GNU Lesser General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>\n.
"""
MESSAGE = """
Explore the producibility potential in a metabolic network using the network expansion algorithm.
"""
REQUIRES = """
Requires Clingo and clyngor package: "pip install clyngor clyngor-with-clingo"
"""

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

# Check ASP binaries.
if not which('clingo'):
    logger.critical('clingo is not in the Path, menetools can not work without it.')
    logger.critical('You can install with: pip install clyngor-with-clingo')
    sys.exit(1)


def main():
    """Run programm.
    """
    # start_time = time.time()
    parser = argparse.ArgumentParser(
        "mene",
        description=MESSAGE + " For specific help on each subcommand use: mene {cmd} --help",
        epilog=REQUIRES
    )
    parser.add_argument(
        "-v",
        "--version",
        action="version",
        version="%(prog)s " + VERSION + "\n" + LICENSE)

    # parent parser
    # MeneTools common arguments.
    parent_parser_d = argparse.ArgumentParser(add_help=False)
    parent_parser_d.add_argument(
        "-d",
        "--draftnet",
        dest="draftnet",
        help="metabolic network in SBML format",
        required=True,
    )
    parent_parser_s = argparse.ArgumentParser(add_help=False)
    parent_parser_s.add_argument(
        "-s",
        "--seeds",
        dest="seeds",
        help="seeds in SBML format",
        required=True,
    )
    parent_parser_t = argparse.ArgumentParser(add_help=False)
    parent_parser_t.add_argument(
        "-t",
        "--targets",
        dest="targets",
        help="targets in SBML format",
        required=False,
    )
    parent_parser_o = argparse.ArgumentParser(add_help=False)
    parent_parser_o.add_argument(
        "--output",
        dest="output",
        help="json output file",
        required=False,
    )

    # Menepath and Menecof common argument.
    parent_parser_opt_e = argparse.ArgumentParser(add_help=False)
    parent_parser_opt_e.add_argument(
        "--enumerate",
        dest="enumerate",
        help="enumerates all cofactors solutions",
        required=False,
        action="store_true",
    )

    # Menecof specific arguments.
    parent_parser_opt_c = argparse.ArgumentParser(add_help=False)
    parent_parser_opt_c.add_argument(
        "-c",
        "--cofactors",
        dest="cofactors",
        help="cofactors, in one-per-line text file format",
        required=False,
    )
    parent_parser_opt_s = argparse.ArgumentParser(add_help=False)
    parent_parser_opt_s.add_argument(
        "--suffix",
        dest="suffix",
        help="suffix to be added to the compounds of the database. \
        It can be the suffix for the cytosolic compartment or   \
        external one. Cytosolic one is prefered to ensure the \
        impact of the added cofactors. Default = None",
        required=False,
    )
    parent_parser_opt_w = argparse.ArgumentParser(add_help=False)
    parent_parser_opt_w.add_argument(
        "--weight",
        dest="weight",
        help="call this option if cofactors are weighted according \
        to their occurrence frequency in database. If so, cofactors \
        file must be tabulated with per line compound'\t'occurrence",\
        required=False,
        action="store_true",
    )

    # Menepath specific argument.
    parent_parser_opt_m = argparse.ArgumentParser(add_help=False)
    parent_parser_opt_m.add_argument(
        "--min",
        dest="min",
        help="call this option to obtain minimal-size paths",
        required=False,
        action="store_true",
    )

    # subparsers
    subparsers = parser.add_subparsers(
        title='subcommands',
        description='valid subcommands:',
        dest="cmd")

    acti_parser = subparsers.add_parser(
        "acti",
        help="Get activable reactions in a metabolic network, starting from seeds.",
        parents=[
            parent_parser_d, parent_parser_s, parent_parser_o
        ]
    )

    check_parser = subparsers.add_parser(
        "check",
        help="Check the producibility of targets from seeds in a metabolic network.",
        parents=[
            parent_parser_d, parent_parser_s, parent_parser_t, parent_parser_o
        ]
    )

    cof_parser = subparsers.add_parser(
        "cof",
        help="Propose cofactor whose producibility could unblock the producibility of targets.",
        parents=[
            parent_parser_d, parent_parser_s, parent_parser_t, parent_parser_opt_c,
            parent_parser_opt_w, parent_parser_opt_s, parent_parser_opt_e, parent_parser_o
        ]
    )

    dead_parser = subparsers.add_parser(
        "dead",
        help="Identification of dead-end reactions (reactions whose reactants are never consumed or whose reactants are never produced) in metabolic networks.",
        parents=[
            parent_parser_d, parent_parser_o
        ]
    )

    path_parser = subparsers.add_parser(
        "path",
        help="Get production pathways of targets in metabolic networks, started from seeds.",
        parents=[
            parent_parser_d, parent_parser_s, parent_parser_t,
            parent_parser_opt_e, parent_parser_opt_m, parent_parser_o
        ]
    )

    scope_parser = subparsers.add_parser(
        "scope",
        help="Get producible metabolites in a metabolic network, starting from seeds.",
        parents=[
            parent_parser_d, parent_parser_s, parent_parser_o
        ]
    )

    seed_parser = subparsers.add_parser(
        "seed",
        help="Get metabolites from exchange reactions in a metabolic network.",
        parents=[
            parent_parser_d, parent_parser_o
        ]
    )

    scope_inc_parser = subparsers.add_parser(
        "scope_inc",
        help="Get the steps of the network expansion to produce either targets or all the producible compounds, starting from seeds.",
        parents=[
            parent_parser_d, parent_parser_s, parent_parser_t, parent_parser_o
        ]
    )

    args = parser.parse_args()

    # If no argument print the help.
    if len(sys.argv) == 1:
        parser.print_help()
        sys.exit(1)

    if args.cmd == "acti":
        run_meneacti(args.draftnet, args.seeds, args.output)
    elif args.cmd == "check":
        run_menecheck(args.draftnet, args.seeds, args.targets, args.output)
    elif args.cmd == "cof":
        run_menecof(args.draftnet, args.seeds, args.targets, args.cofactors, args.weight, args.suffix, args.enumerate, args.output)
    elif args.cmd == "dead":
        run_menedead(args.draftnet, args.output)
    elif args.cmd == "path":
        run_menepath(args.draftnet, args.seeds, args.targets, args.min, args.enumerate, args.output)
    elif args.cmd == "scope":
        run_menescope(args.draftnet, args.seeds, args.output)
    elif args.cmd == "seed":
        run_meneseed(args.draftnet, args.output)
    elif args.cmd == "scope_inc":
        run_menescope_inc(args.draftnet, args.seeds, args.targets, args.output)
    else:
        logger.critical("Invalid commands for mene.")
        parser.print_help()
        sys.exit(1)
