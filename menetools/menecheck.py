#!python
# -*- coding: utf-8 -*-
import argparse
import json
import logging
import sys

from menetools import utils, query, sbml
from clyngor import as_pyasp
from xml.etree.ElementTree import ParseError

logger = logging.getLogger('menetools.menecheck')


def run_menecheck(draft_sbml,seeds_sbml,targets_sbml,output=None):
    """checks the producibility of targets from seeds in a metabolic network
    
    Args:
        draft_sbml (str): metabolic network SBML file
        seeds_sbml (str): SBML file
        targets_sbml (str): SBML file
        output (str): path to json output file

    Returns:
        list, list: model, lists of unproducible and producibile targets
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

    logger.info(f'Reading targets from {targets_sbml}')
    try:
        targets = sbml.readSBMLspecies_clyngor(targets_sbml, 'target')
    except FileNotFoundError:
        logger.critical(f"File not found: {targets_sbml}")
        sys.exit(1)
    except ParseError:
        logger.critical(f"Invalid syntax in SBML file: {targets_sbml}")
        sys.exit(1)

    logger.info('\nChecking draftnet for unproducible targets')
    print(f'Number of targets: {len(targets)}')
    model = query.get_unproducible(draftnet, targets, seeds)
    unprod = []
    prod = []
    for pred in model :
        if pred == 'unproducible_target':
            for a in model[pred, 1]:
                unprod.append(a[0])
        elif pred == 'producible_target':
            for a in model[pred, 1]:
                prod.append(a[0])
    logger.info(f'\n{len(prod)} producible targets:')
    logger.info('\n'.join(prod))
    logger.info(f"\n{len(unprod)} unproducible targets:")
    logger.info('\n'.join(unprod))

    results = {}
    results['producible_target'] = prod
    results['unproducible_target'] = unprod
    if output:
        with open(output, "w") as output_file:
            json.dump(results, output_file, indent=True, sort_keys=True)

    utils.clean_up()
    return unprod, prod
