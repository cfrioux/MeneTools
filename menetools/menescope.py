#!/usr/bin/python3
#-*- coding: utf-8 -*-

import argparse
import inspect
import json
import logging
import os
import sys

from menetools import utils, query, sbml
from clyngor import as_pyasp
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
    for pred in model:
        if pred == 'dscope':
            for a in model[pred, 1]:
                scope.append(a[0])
    logger.info(' ' + str(len(scope)) + ' compounds on scope:')
    logger.info('\n'.join(scope))

    if output:
        with open(output, "w") as output_file:
            json.dump({'scope': scope}, output_file, indent=True, sort_keys=True)

    return scope
