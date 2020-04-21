#!/usr/bin/python
#-*- coding: utf-8 -*-
import argparse
import sys
import inspect
import os
import re
from xml.etree.ElementTree import ParseError
from .utils import clean_up
from .query import get_unproducible, get_cofs_weighted, get_cofs, get_intersection_of_optimal_solutions_cof, get_union_of_optimal_solutions_cof, get_optimal_solutions_cof
from .sbml import readSBMLspecies_clyngor, make_weighted_list_of_species, readSBMLnetwork_clyngor
from clyngor import as_pyasp
from clyngor.as_pyasp import TermSet, Atom
import logging
logger = logging.getLogger('menetools.menecof')

def convert_to_coded_id(uncoded):
    """encode str components
    
    Args:
        uncoded (str): string to be encoded
    
    Returns:
        str: encoded string
    """
    charlist = ['-', '|', '/', '(', ')', '\'', '=', '#', '*', '.', ':', '!', '+']
    for c in charlist:
        uncoded = uncoded.replace(c, "__" + str(ord(c)) + "__")

    if re.search('^[0-9]', uncoded):
        uncoded = "_" + uncoded
    return uncoded

def cmd_menecof():
    """run menecof from shell
    """
    parser = argparse.ArgumentParser()
    parser.add_argument("-d", "--draftnet",
                        help="metabolic network in SBML format", required=True)
    parser.add_argument("-s", "--seeds",
                        help="seeds in SBML format", required=True)
    parser.add_argument("-t", "--targets",
                        help="targets in SBML format", required=True)
    parser.add_argument("-c", "--cofactors",
                        help="cofactors, in one-per-line text file format", required=False)

    parser.add_argument("--suffix",
                        help="suffix to be added to the compounds of the database. \
                        It can be the suffix for the cytosolic compartment or   \
                        external one. Cytosolic one is prefered to ensure the \
                        impact of the added cofactors. Default = None",
                        required=False)

    parser.add_argument("--weight",
                        help="call this option if cofactors are weighted according \
                        to their occurrence frequency in database. If so, cofactors \
                        file must be tabulated with per line compound'\t'occurrence",\
                        required=False, action="store_true")

    parser.add_argument("--enumerate",
                        help="enumerates all cofactors solutions",\
                        required=False, action="store_true")

    args = parser.parse_args()

    draft_sbml = args.draftnet
    seeds_sbml = args.seeds
    targets_sbml = args.targets
    cofactors_txt = args.cofactors
    weights = args.weight
    suffix = args.suffix
    enumeration = args.enumerate

    run_menecof(draft_sbml,seeds_sbml,targets_sbml,cofactors_txt,weights,suffix,enumeration)

def run_menecof(draft_sbml,seeds_sbml,targets_sbml,cofactors_txt=None,weights=None,suffix=None,enumeration=None):
    """propose cofactor whose producibility could unblock the producibility of targets
    
    Args:
        draft_sbml (str): SBML 2 metabolic network file
        seeds_sbml (str): SBML 2 seeds file
        targets_sbml (str): SBML 2 targets file
        cofactors_txt (str, optional): Defaults to None. Cofactors file, one per line
        weights (bool, optional): Defaults to None. True if cofactors_txt is weighted
        suffix (str, optional): Defaults to None. suffix to be added to metabolites in metabolic model
        enumeration (bool, optional): Defaults to None. enumeration boolean
    
    Returns:
        TermSet,str,TermSet,TermSet,list,list,list: ASP models and lists with cofactors and (un)producible targets
    """
    logger.info(f'Reading draft network from {draft_sbml}')
    try:
        draftnet = readSBMLnetwork_clyngor(draft_sbml, 'draft')
    except FileNotFoundError:
        logger.critical(f'File not found: {draft_sbml}')
        sys.exit(1)
    except ParseError:
        logger.critical(f'Invalid syntax in SBML file: {draft_sbml}')
        sys.exit(1)

    logger.info(f'Reading seeds from {seeds_sbml}')
    try:
        seeds = readSBMLspecies_clyngor(seeds_sbml,'seed')
    except FileNotFoundError:
        logger.critical(f'File not found: {seeds_sbml}')
        sys.exit(1)
    except ParseError:
        logger.critical(f'Invalid syntax in SBML file: {seeds_sbml}')
        sys.exit(1)

    logger.info(f'Reading targets from {targets_sbml}')
    try:
        targets = readSBMLspecies_clyngor(targets_sbml, 'target')
    except FileNotFoundError:
        logger.critical(f"File not found: {targets_sbml}")
        sys.exit(1)
    except ParseError:
        logger.critical(f"Invalid syntax in SBML file: {targets_sbml}")
        sys.exit(1)

    if weights and cofactors_txt:
        logger.info('Reading cofactors with weights from {cofactors_txt}')
        with open(cofactors_txt,'r') as f:
            cofactors_list = f.read().splitlines()
        cofactors = TermSet()
        for elem in cofactors_list:
            try:
                data = elem.split('\t')
                if suffix != None:
                    cofactors.add(Term('cofactor', ["\""+convert_to_coded_id(data[0]) + suffix + "\"", data[1]]))
                else:
                    cofactors.add(Term('cofactor', ["\""+convert_to_coded_id(data[0]) + "\"", data[1]]))
            except:
                logger.critical('Input cofactor file is not tabulated (at least not on every line)\
                \n Please check the file, maybe you did not mean to use --weight option?\
                \nUnsuitable input file... Quitting program')
                quit()

    elif cofactors_txt:
        looger.info('Reading cofactors from {cofactors_txt}')
        with open(cofactors_txt,'r') as f:
            cofactors_list = f.read().splitlines()
        cofactors = TermSet()
        for elem in cofactors_list:
            if '\t' in elem:
                logger.critical('A tabulated file was given as input cofactors. \
                \nAre you sure you did not mean to use the weight option? \
                \nUnsuitable input file... Quitting program')
                quit()
            if suffix != None:
                cofactors.add(Term('cofactor', ["\""+convert_to_coded_id(elem) + suffix + "\""]))
            else:
                cofactors.add(Term('cofactor', ["\""+convert_to_coded_id(elem) + "\""]))

    else:
        logger.warning('No cofactors file is given as input.')
        logger.info('Research of cofactors will be done in the network itself')
        species_and_weights = make_weighted_list_of_species(draft_sbml)
        cofactors = TermSet()
        for elem in species_and_weights:
            cofactors.add(Atom('cofactor', ["\""+elem+"\"",+species_and_weights[elem]]))
        weights = True

    logger.info('\nChecking draft network for unproducible targets before cofactors selection ...')
    model = get_unproducible(draftnet, targets, seeds)
    unprod = []
    for pred in model :
        if pred == 'unproducible_target':
            for a in model[pred, 1]:
                unprod.append(a[0])
    logger.info(f'{len(unprod)} unproducible targets:')
    logger.info('\n'.join(unprod))

    logger.info('\nChecking minimal sets of cofactors to produce all targets ...')
    sys.stdout.flush()
    if weights:
        model = get_cofs_weighted(draftnet, targets, seeds, cofactors)
        optimum = model[1]
        # optimum = model.score
        if len(optimum) == 2:
            # it means that all targets can be produced with the selected cofactors
            optimum = [0] + optimum
        optimum = ','.join(map(str, optimum))
        #print(optimum)

    else:
        model = get_cofs(draftnet, targets, seeds, cofactors)
        # optimum = model.score
        optimum = model[1]
        if len(optimum) == 1:
            # it means that all targets can be produced with the selected cofactors
            optimum = [0] + optimum
        optimum = ','.join(map(str, optimum))
    logger.info('Optimum score {optimum}')
    # solumodel = model.to_list()
    unproduced_targets = []
    chosen_cofactors = []
    newly_producible_targets = []
    for pred in model[0]:
        if pred == 'needed_cof':
            if model[0][pred, 2]:
                for a in model[0][pred, 2]:
                    chosen_cofactors.append((a[0],a[1]))
            else:
                for a in model[0][pred, 1]:
                    chosen_cofactors.append((a[0],None))
        elif pred == 'still_unprod':
            for a in model[0][pred, 1]:
                unproduced_targets.append(a[0])
        elif pred == 'newly_prod':
            for a in model[0][pred, 1]:
                newly_producible_targets.append(a[0])
    # for p in solumodel:
    #     if p.pred() == "needed_cof":
    #         cof = p.arg(0)
    #         try:
    #             weight = p.arg(1)
    #         except:
    #             weight = None
    #         chosen_cofactors.append((cof,weight))
    #     elif p.pred() == "still_unprod":
    #         tgt = p.arg(0)
    #         unproduced_targets.append(tgt)
    #     else:
    #         newly_producible_targets.append(p.arg(0))
    logger.info(f'Still {len(unproduced_targets)} unproducible targets:')
    logger.info('\n'.join(unproduced_targets))
    logger.info('\nSelected cofactors:')
    for cofactor in chosen_cofactors:
        if cofactor[1] == None:
            logger.info(cofactor[0])
        else:
            logger.info(f'{cofactor[0]} ({str(cofactor[1])})')
    logger.info(f'\n{len(newly_producible_targets)} newly producible targets:')
    logger.info(str(newly_producible_targets))


    logger.info('\nIntersection of solutions') # with size', optimum, '
    intersection = get_intersection_of_optimal_solutions_cof(draftnet, seeds, targets, cofactors, optimum, weights)
    # solumodel = intersection_model.to_list()
    intersection_icofactors = []
    # for p in solumodel:
    #     if p.pred() == "needed_cof":
    #         cof = p.arg(0)
    #         try:
    #             weight = p.arg(1)
    #         except:
    #             weight = None
    #         intersection_icofactors.append((cof,weight))
        #print('\nSelected cofactors:')
    intersection_model = intersection[0]
    for pred in intersection_model:
        if pred == 'needed_cof':
            if intersection_model[pred, 2]:
                for a in intersection_model[pred, 2]:
                    intersection_icofactors.append((a[0],a[1]))
            else:
                for a in intersection_model[pred, 1]:
                    intersection_icofactors.append((a[0],None))
    for cofactor in intersection_icofactors:
        if cofactor[1] == None:
            logger.info(cofactor[0])
        else:
            logger.info(f'{cofactor[0]} ({str(cofactor[1])})')

    logger.info('\nUnion of solutions') # with size', optimum, '
    union = get_union_of_optimal_solutions_cof(draftnet, seeds, targets, cofactors, optimum, weights)
    union_model= union[0]
    union_icofactors = []
    for pred in union_model:
        if pred == 'needed_cof':
            if union_model[pred, 2]:
                for a in union_model[pred, 2]:
                    union_icofactors.append((a[0],a[1]))
            else:
                for a in union_model[pred, 1]:
                    union_icofactors.append((a[0],None))
        #print('\nSelected cofactors:')
    for cofactor in union_icofactors:
        if cofactor[1] == None:
            logger.info(cofactor[0])
        else:
            logger.info(f'{cofactor[0]} ({str(cofactor[1])})')

    if enumeration:
        logger.info(f'\nComputing all solutions with size {optimum}')
        all_models =  get_optimal_solutions_cof(draftnet, seeds, targets, cofactors, optimum, weights)
        count = 1
        all_models_lst = []
        for model in all_models:
            logger.info(f'\nSolution {str(count)}:')
            count+=1
            current_cofactors = []
            for pred in model[0]:
                if pred == 'needed_cof':
                    if model[0][pred, 2]:
                        for a in model[0][pred, 2]:
                            current_cofactors.append((a[0],a[1]))
                    else:
                        for a in model[0][pred, 1]:
                            current_cofactors.append((a[0],None))
            #print('\nSelected cofactors:')
            for cofactor in current_cofactors:
                if cofactor[1] == None:
                    logger.info(cofactor[0])
                else:
                    logger.info(f'{cofactor[0]} ({str(cofactor[1])})')
            all_models_lst.append(current_cofactors)
        clean_up()
        return all_models_lst, optimum, set(union_icofactors), set(intersection_icofactors), set(chosen_cofactors), set(unprod), set(newly_producible_targets)

    clean_up()
    return model, optimum, set(union_icofactors), set(intersection_icofactors), set(chosen_cofactors), set(unprod), set(newly_producible_targets)

if __name__ == '__main__':
    cmd_menecof()