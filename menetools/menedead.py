#!python
# -*- coding: utf-8 -*-
import json
import logging
import os
import sys

from menetools import utils, query, sbml
from pkg_resources import resource_filename
from xml.etree.ElementTree import ParseError

logger = logging.getLogger('menetools.menedead')


def run_menedead(draft_sbml, output=None):
    """
    Identify dead ends in a metabolic network.

    Args:
        draft_sbml (str): SBML metabolic network file
        output (str): path to json output file
    
    Returns:
        dictionary: non produced and non consumed compounds
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

    logger.info('\nChecking draft network deadend')
    sys.stdout.flush()
    model = query.get_dead(draftnet)

    non_consumed = []
    non_produced = []
    for pred in model:
        if pred == "deadend_np":
            [non_produced.append(a[0]) for a in model[pred, 1]]
        elif pred == "deadend_nc":
            [non_consumed.append(a[0]) for a in model[pred, 1]]
    logger.info(
        f"{len(non_consumed)} non-consumed metabolites: \n {', '.join(non_consumed)}"
    )
    logger.info(
        f"{len(non_produced)} non-produced metabolites: \n {', '.join(non_produced)}"
    )

    results = {'non_produced_metabolites': non_produced,
        'non_consumed_metabolites': non_consumed}
    if output:
        with open(output, "w") as output_file:
            json.dump(results, output_file, indent=True, sort_keys=True)

    return results
