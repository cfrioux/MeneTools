#!/usr/bin/python3
#-*- coding: utf-8 -*-

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

from clyngor.as_pyasp import TermSet, Atom
from menetools import utils, query, sbml
from xml.etree.ElementTree import ParseError

logger = logging.getLogger('menetools.menepath')


def run_menepath(draft_sbml,seeds_sbml,targets_sbml,min_size=None,enumeration=None,output=None):
    """Get production pathways of targets in metabolic networks, started from seeds
    
    Args:
        draft_sbml (str): SBML metabolic network file
        seeds_sbml (str): SBML seeds file
        targets_sbml (str): SBML targets file
        min_size (bool, optional): Defaults to None. minimal size paths
        enumeration (bool, optional): Defaults to None. enumeration of all paths
        output (str): path to json output file

    Returns:
        TermSet, set, set, set, set: Model, unproducible targets and paths
    """
    results = {}
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

    logger.info('\nChecking network for unproducible targets')
    sys.stdout.flush()
    model = query.get_unproducible(draftnet, targets, seeds)
    # unproducible_targets_atoms = set()
    producible_targets_atoms = set()
    unproducible_targets_lst = []

    for pred in model :
        if pred == 'unproducible_target':
            for a in model[pred, 1]:
                # unproducible_targets_atoms.add(Atom('unproducible_targets', ['"'+a[0]+'"']))
                unproducible_targets_lst.append(a[0])
        elif pred == 'producible_target':
            for a in model[pred, 1]:
                producible_targets_atoms.add(Atom('target', ['"'+a[0]+'"']))
    results['unproducible_targets_lst'] = unproducible_targets_lst

    logger.info(f'{len(unproducible_targets_lst)} unproducible targets:')
    logger.info("\n".join(unproducible_targets_lst))

    for t in producible_targets_atoms:
        single_target = TermSet()
        single_target.add(t)

        logger.info(f'\n{single_target}')
        draft_str = 'draft'
        draftfact = TermSet()
        draftatom = Atom('draft', ["\""+draft_str+"\""])
        draftfact.add(draftatom)
        lp_instance   = TermSet.union(draftnet,draftfact,single_target,seeds)

    # one solution, minimal or not, depending on option
        if min_size:
            logger.info(f'\nComputing one solution of cardinality-minimal production paths for {t}')
        else:
            logger.info(f'\nComputing one solution of production paths for {t}')
        # """
        one_model = query.get_paths(lp_instance, min_size)
        one_path = []
        for pred in one_model[0]:
            if pred == 'selected':
                for a in one_model[0][pred, 2]:
                    one_path.append(a[0])
        results['one_path'] = one_path
        optimum = one_model[1]
        if optimum:
            optimum = ','.join(map(str, optimum))
        logger.info(f'Solution size {len(one_path)} reactions')
        logger.info('\n'.join(one_path))
        # """
        """
        one_model = query.get_paths(lp_instance, min_size)
        print(one_model.score)
        optimum = one_model.score
        print('Solution size ',len(one_model), ' reactions')
        utils.print_met(one_model.to_list())
        """

    # union of solutions
        if min_size:
            logger.info(f'\nComputing union of cardinality-minimal production paths for {t}')
        else:
            logger.info(f'\nComputing union of production paths for {t}')
        union = query.get_union_of_paths(lp_instance, optimum, min_size)
        union_model = union[0]
        union_path = []
        for pred in union_model:
            if pred == 'selected':
                for a in union_model[pred, 2]:
                    union_path.append(a[0])
        results['union_path'] = union_path
        logger.info(f'Union size {len(union_path)} reactions')
        logger.info('\n'.join(union_path))

    # intersection of solutions
        if min_size:
            logger.info(f'\nComputing intersection of cardinality-minimal production paths for {t}')
        else:
            logger.info(f'\nComputing intersection of production paths for {t}')
        intersection = query.get_intersection_of_paths(lp_instance, optimum, min_size)
        intersection_model = intersection[0]
        intersection_path = []
        for pred in intersection_model:
            if pred == 'selected':
                for a in intersection_model[pred, 2]:
                    intersection_path.append(a[0])
        results['intersection_path'] = intersection_path
        logger.info(f'Intersection size {len(intersection_path)} reactions')
        logger.info('\n'.join(intersection_path))

    # if wanted, get enumeration of all solutions
        if enumeration:
            if min_size:
                logger.info(f'\nComputing all cardinality-minimal production paths for {t} - {optimum}')
            else:
                logger.info(f'\nComputing all production paths for {t}')

            all_models = query.get_all_paths(lp_instance, optimum, min_size)
            all_models_lst = []
            count = 1
            for model in all_models:
                current_enum_path=[]
                for pred in model:
                    if pred == 'selected':
                        for a in model[pred, 2]:
                            current_enum_path.append(a[0])
                logger.info(f'\nSolution {str(count)} of size : {str(len(current_enum_path))} reactions:')
                count+=1
                logger.info('\n'.join(current_enum_path))
                all_models_lst.append(current_enum_path)
            if output:
                with open(output, "w") as output_file:
                    json.dump(results, output_file, indent=True, sort_keys=True)

            utils.clean_up()
            return all_models_lst, set(unproducible_targets_lst), set(one_path), set(union_path), set(intersection_path)

    if output:
        with open(output, "w") as output_file:
            json.dump(results, output_file, indent=True, sort_keys=True)

    #TODO store for all targets
    utils.clean_up()
    return model, set(unproducible_targets_lst), set(one_path), set(union_path), set(intersection_path)
