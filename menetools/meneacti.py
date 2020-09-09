#!/usr/bin/python3
#-*- coding: utf-8 -*-

import argparse
import sys
import inspect
import os
from menetools import utils, query, sbml
from clyngor import as_pyasp
from xml.etree.ElementTree import ParseError
import logging
logger = logging.getLogger('menetools.meneacti')

def cmd_meneacti():
    """run meneacti from shell
    """
    parser = argparse.ArgumentParser()
    parser.add_argument("-d", "--draftnet",
                        help="metabolic network in SBML format", required=True)
    parser.add_argument("-s", "--seeds",
                        help="seeds in SBML format", required=True)

    args = parser.parse_args()

    draft_sbml = args.draftnet
    seeds_sbml = args.seeds

    run_meneacti(draft_sbml,seeds_sbml)

def run_meneacti(draft_sbml,seeds_sbml,quiet=False):
    """get activable reactions in a metabolic network, starting from seeds
    
    Args:
        draft_sbml (str): SBML 2 metabolic network file
        seeds_sbml (str): SBML 2 seeds file
        quiet (bool): boolean for a silent mode
    
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

    return activ

if __name__ == '__main__':
    cmd_meneacti()