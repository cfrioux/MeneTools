#!/usr/bin/python3
#-*- coding: utf-8 -*-

# Copyright (C) 2017-2024 Clémence Frioux & Arnaud Belcour - Inria Dyliss - Pleiade
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


logger = logging.getLogger('menetools.menescope')


def run_menescope(draft_sbml,seeds_sbml,output=None):
    """get producible metabolites in a metabolic network, starting from seeds
    
    Args:
        draft_sbml (str): SBML metabolic network file
        seeds_sbml (str): SBML seeds file
        output (str): path to json output file
    
    Returns:
        list: producible compounds
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

    logger.info('\nChecking draft network scope')
    sys.stdout.flush()
    model = query.get_scope(draftnet, seeds)
    scope = []
    produced_seeds = []
    non_produced_seeds = []
    absent_seeds = []
    for pred in model:
        if pred == 'dscope':
            for a in model[pred, 1]:
                scope.append(a[0])
        if pred == 'produced_seed':
            for a in model[pred, 1]:
                produced_seeds.append(a[0])
        if pred == 'non_produced_seed':
            for a in model[pred, 1]:
                non_produced_seeds.append(a[0])
        if pred == 'absent_seed':
            for a in model[pred, 1]:
                absent_seeds.append(a[0])
    logger.info(' ' + str(len(scope)) + ' compounds on scope:')
    logger.info('\n'.join(scope))
    logger.info(' ' + str(len(produced_seeds)) + ' seeds are producible:')
    logger.info('\n'.join(produced_seeds))
    logger.info(' ' + str(len(non_produced_seeds)) + ' seeds are not producible:')
    logger.info('\n'.join(non_produced_seeds))
    logger.info(' ' + str(len(absent_seeds)) + ' seeds that were provided as input are absent from the network:')
    logger.info('\n'.join(absent_seeds))

    results = {'scope': scope, 'produced_seeds': produced_seeds, 'non_produced_seeds': non_produced_seeds, 'absent_seeds': absent_seeds}
    if output:
        with open(output, "w") as output_file:
            json.dump(results, output_file, indent=True, sort_keys=True)

    return results
