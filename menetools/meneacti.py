#!/usr/bin/python3
#-*- coding: utf-8 -*-

import argparse
import json
import inspect
import logging
import os
import sys

from clyngor import as_pyasp
from menetools import utils, query, sbml
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
