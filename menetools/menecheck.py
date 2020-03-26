#!python
# -*- coding: utf-8 -*-
import argparse
import sys
import logging
from menetools import utils, query, sbml
from  clyngor import as_pyasp
from xml.etree.ElementTree import ParseError

logger = logging.getLogger(__name__)

def cmd_menecheck():
    """run menecheck from shell
    """
    parser = argparse.ArgumentParser()
    parser.add_argument("-d", "--draftnet",
                        help="metabolic network in SBML format", required=True)
    parser.add_argument("-s", "--seeds",
                        help="seeds in SBML format", required=True)
    parser.add_argument("-t", "--targets",
                        help="targets in SBML format", required=True)


    args = parser.parse_args()

    draft_sbml = args.draftnet
    seeds_sbml = args.seeds
    targets_sbml =  args.targets

    run_menecheck(draft_sbml,seeds_sbml,targets_sbml)

def run_menecheck(draft_sbml,seeds_sbml,targets_sbml):
    """checks the producibility of targets from seeds in a metabolic network
    
    Args:
        draft_sbml (str): metabolic network SBML 2 file
        seeds_sbml (str): SBML 2 file
        targets_sbml (str): SBML 2 file
    
    Returns:
        list, list: model, lists of unproducible and producibile targets
    """
    logger.info('Reading draft network from ' + draft_sbml)
    try:
        draftnet = sbml.readSBMLnetwork_clyngor(draft_sbml, 'draft')
    except FileNotFoundError:
        logger.critical("File not found: "+draft_sbml)
        sys.exit(1)
    except ParseError:
        logger.critical("Invalid syntax in SBML file: "+draft_sbml)
        sys.exit(1)

    logger.info('Reading seeds from ' + seeds_sbml)
    try:
        seeds = sbml.readSBMLspecies_clyngor(seeds_sbml, 'seed')
    except FileNotFoundError:
        logger.critical("File not found: "+seeds_sbml)
        sys.exit(1)
    except ParseError:
        logger.critical("Invalid syntax in SBML file: "+seeds_sbml)
        sys.exit(1)

    logger.info('Reading targets from ' + targets_sbml)
    try:
        targets = sbml.readSBMLspecies_clyngor(targets_sbml, 'target')
    except FileNotFoundError:
        logger.critical("File not found: "+targets_sbml)
        sys.exit(1)
    except ParseError:
        logger.critical("Invalid syntax in SBML file: "+targets_sbml)
        sys.exit(1)

    logger.info('\nChecking draftnet for unproducible targets')
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
    logger.info(str(len(prod)) + ' producible targets:')
    logger.info('\n'.join(prod))
    logger.info(str(len(unprod)) + ' unproducible targets:')
    logger.info('\n'.join(unprod))


    utils.clean_up()
    return unprod, prod

if __name__ == '__main__':
    cmd_menecheck()
