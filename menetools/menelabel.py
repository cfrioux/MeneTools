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

import json
import logging
import statistics
import sys

from menetools import query, sbml
from xml.etree.ElementTree import ParseError


logger = logging.getLogger('menetools.menescope')


def run_menelabel(draft_sbml,seeds_sbml,output=None):
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
        seeds, labelled_seeds = sbml.readSBMLspecies_labelled_clyngor(seeds_sbml,'seed')
    except FileNotFoundError:
        logger.critical(f'File not found: {seeds_sbml}')
        sys.exit(1)
    except ParseError:
        logger.critical(f'Invalid syntax in SBML file: {seeds_sbml}')
        sys.exit(1)

    logger.info('\nChecking draft network scope')
    sys.stdout.flush()
    model = query.get_labelled_scope(draftnet, seeds)

    labelled_scope = {}
    metabolite_produced = {}
    produced_seeds = []
    for pred in model:
        if pred == 'dscope':
            for a in model[pred, 2]:
                label_number = int(a[1].strip('"'))
                seed_id = labelled_seeds[label_number]
                metabolite_name = a[0]
                if seed_id not in labelled_scope:
                    labelled_scope[seed_id] = [metabolite_name]
                else:
                    labelled_scope[seed_id].append(metabolite_name)
                if metabolite_name not in metabolite_produced:
                    metabolite_produced[metabolite_name] = [seed_id]
                else:
                    metabolite_produced[metabolite_name].append(seed_id)
        if pred == 'produced_seed':
            for a in model[pred, 1]:
                produced_seeds.append(a[0])
    logger.info(' ' + str(len(metabolite_produced)) + ' compounds on scope.')
    mean_compounds_producible_from_seeds = statistics.mean([len(metabolite_produced[metabolite]) for metabolite in metabolite_produced])
    logger.info(' At mean compounds are producible from ' + str(mean_compounds_producible_from_seeds) + ' seeds.')
    mean_seeds_producing = statistics.mean([len(labelled_scope[seed]) for seed in labelled_scope])
    logger.info(' At mean a seed helped to produce ' + str(mean_seeds_producing) + ' compounds.')

    results = {'labelled_scope': labelled_scope, 'metabolite_produced': metabolite_produced, 'produced_seeds': produced_seeds}
    if output:
        with open(output, "w") as output_file:
            json.dump(results, output_file, indent=True, sort_keys=True)

    return results
