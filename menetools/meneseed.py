#!python
# -*- coding: utf-8 -*-

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

logger = logging.getLogger('menetools.meneseed')


def run_meneseed(draft_sbml, output=None):
    """
    Identify seeds in a metabolic network.

    Args:
        draft_sbml (str): SBML metabolic network file
        output (str): path to json output file
    
    Returns:
        dictionary: seeds compounds    
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

    logger.info('\nChecking draft network exchange reactions')
    sys.stdout.flush()
    model = query.get_seed(draftnet)

    seeds = []
    for pred in model:
        if pred == "seed":
            [seeds.append(a[0]) for a in model[pred, 1]]
            
    results = {'seeds': seeds}

    logger.info(
        f"{len(seeds)} seed metabolites (related to exchange reactions):"
    )
    logger.info('\n'.join(seeds))

    if output:
        with open(output, "w") as output_file:
            json.dump(results, output_file, indent=True, sort_keys=True)

    return results
