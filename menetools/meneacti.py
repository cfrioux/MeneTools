#!/usr/bin/python3
#-*- coding: utf-8 -*-

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

import json
import logging
import sys

from menetools import query, sbml
from xml.etree.ElementTree import ParseError

logger = logging.getLogger('menetools.meneacti')


def run_meneacti(draft_sbml,seeds_sbml,output=None):
    """get activable reactions in a metabolic network, starting from seeds
    
    Args:
        draft_sbml (str): SBML metabolic network file
        seeds_sbml (str): SBML seeds file
        output (str): path to json output file

    Returns:
        list: activable reactions
    """
    logger.info(f'Reading draft network from {draft_sbml}')
    try:
        draftnet = sbml.readSBMLnetwork_clyngor(draft_sbml, 'draft')
    except FileNotFoundError:
        logger.critical(f'File not found: {draft_sbml}')
        sys.exit(1)
    except ParseError:
        logger.critical(f'Invalid syntax in SBML file: {draft_sbml}')
        sys.exit(1)

    logger.info(f'Reading seeds from {seeds_sbml}')
    try:
        seeds = sbml.readSBMLspecies_clyngor(seeds_sbml,'seed')
    except FileNotFoundError:
        logger.critical(f'File not found: {seeds_sbml}')
        sys.exit(1)
    except ParseError:
        logger.critical(f'Invalid syntax in SBML file: {seeds_sbml}')
        sys.exit(1)

    logger.info('\nChecking reaction activation in metabolic network')
    sys.stdout.flush()
    model = query.get_acti(draftnet, seeds)
    activ = []
    for pred in model:
        if pred == 'activ':
            for a in model[pred, 1]:
                activ.append(a[0])
    logger.info(' ' + str(len(activ)) + ' activable reactions:')
    logger.info('\n'.join(activ))

    results = {}
    results['activ'] = activ
    if output:
        with open(output, "w") as output_file:
            json.dump(results, output_file, indent=True, sort_keys=True)

    return activ
