#!/usr/bin/python3
#-*- coding: utf-8 -*-

# Copyright (C) 2017-2021 Clémence Frioux & Arnaud Belcour - Inria Dyliss - Pleiade
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
import inspect
import json
import logging
import os
import sys

from menetools import utils, query, sbml
from clyngor import as_pyasp
from xml.etree.ElementTree import ParseError


logger = logging.getLogger('menetools.meneinc')


def run_meneinc(draft_sbml,seeds_sbml,targets_sbml,output=None):
    """get producible metabolites in a metabolic network, starting from seeds
    using incremental mode to show each activation.
    
    Args:
        draft_sbml (str): SBML metabolic network file
        seeds_sbml (str): SBML seeds file
        targets_sbml (str): SBML targets file
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

    logger.info(f'Reading targets from {targets_sbml}')
    try:
        targets = sbml.readSBMLspecies_clyngor(targets_sbml, 'target')
    except FileNotFoundError:
        logger.critical(f"File not found: {targets_sbml}")
        sys.exit(1)
    except ParseError:
        logger.critical(f"Invalid syntax in SBML file: {targets_sbml}")
        sys.exit(1)

    # Check if all targets are producible, if not stop the script.
    # As the incremental scope will never end if tehre is unproducible targets.
    logger.info('\nChecking network for unproducible targets')
    sys.stdout.flush()
    model = query.get_unproducible(draftnet, targets, seeds)

    unproducible_targets_lst = []
    for pred in model :
        if pred == 'unproducible_target':
            for a in model[pred, 1]:
                unproducible_targets_lst.append(a[0])

    if len(unproducible_targets_lst):
        logger.critical('There is unproducible targets, incremental scope will enter an infinite loop due to them. Remove them if you want to pursue:')
        logger.critical("\n".join(unproducible_targets_lst))
        sys.exit()

    logger.info('\nChecking draft network scope')
    sys.stdout.flush()
    model = query.get_inc_scope(draftnet, targets, seeds)

    incremental_scope = {}
    for pred in model:
        if pred == 'dscope':
            for a in model[pred, 2]:
                metabolite_id = a[0]
                incremental_step = a[1]
                if metabolite_id not in incremental_scope:
                    incremental_scope[metabolite_id] = incremental_step
                else:
                    if incremental_step < incremental_scope[metabolite_id]:
                        incremental_scope[metabolite_id] = incremental_step

    logger.info(' ' + str(len(incremental_scope)) + ' compounds on scope:')

    step_produced = {}
    for metabolite_id in incremental_scope:
        incremental_step = incremental_scope[metabolite_id]
        if incremental_step not in step_produced:
            step_produced[incremental_step] = [metabolite_id]
        else:
            step_produced[incremental_step].append(metabolite_id)

    ordered_steps = sorted(list(step_produced.keys()))
    for step in ordered_steps:
        logger.info('{0} new metabolites producible at step {1}'.format(len(step_produced[step]), step))

    results = {'incremental_scope': incremental_scope, 'step_produced': step_produced}
    if output:
        with open(output, "w") as output_file:
            json.dump(results, output_file, indent=True, sort_keys=True)

    return results