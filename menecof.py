#!/usr/bin/python
#-*- coding: utf-8 -*-

import argparse
import sys
import inspect
import os
from pyasp.asp import *
from menetools import utils, query, sbml

# TODO handle preferences

def convert_to_coded_id(uncoded):
    '''
    convert text to SBML-ID friendly text
    '''
    charlist = ['-', '|', '/', '(', ')', '\'', '=', '#', '*', '.', ':', '!', '+']
    for c in charlist:
        uncoded = uncoded.replace(c, "__" + str(ord(c)) + "__")

    if re.search('^[0-9]', uncoded):
        uncoded = "_" + uncoded
    return uncoded

def ascii_replace(match):
    return chr(int(match.group(1)))


if __name__ == '__main__':


    parser = argparse.ArgumentParser()
    parser.add_argument("-d", "--draftnet",
                        help="metabolic network in SBML format", required=True)
    #parser.add_argument("-r", "--repairnet",
    #                    help="metabolic network in SBML format")
    parser.add_argument("-s", "--seeds",
                        help="seeds in SBML format", required=True)
    parser.add_argument("-t", "--targets",
                        help="targets in SBML format", required=True)
    #parser.add_argument("-r", "--repairnet",
    #                    help="metabolic network in SBML format")
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
    #repair_sbml = args.repairnetwork
    seeds_sbml = args.seeds
    targets_sbml = args.targets
    cofactors_txt = args.cofactors
    weights = args.weight
    suffix = args.suffix
    enumerate = args.enumerate

    print('Reading draft network from ', draft_sbml, '...', end='')
    sys.stdout.flush()
    draftnet = sbml.readSBMLnetwork(draft_sbml, 'draft')
    #print(draftnet)
    print('done.')

    print('Reading seeds from ', seeds_sbml, '...', end='')
    sys.stdout.flush()
    seeds = sbml.readSBMLspecies(seeds_sbml, 'seed')
    #print(seeds)
    print('done.')
    #seeds.to_file("seeds.lp")

    print('Reading targets from ', targets_sbml, '...', end='')
    sys.stdout.flush()
    targets = sbml.readSBMLspecies(targets_sbml, 'target')
    #print(targets)
    print('done.')
    #targets.to_file("targets.lp")

    if weights and cofactors_txt:
        print('Reading cofactors with weights from ', cofactors_txt, '...', end='')
        sys.stdout.flush()
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
                print('Input cofactor file is not tabulated (at least not on every line)\
                \n Please check the file, maybe you did not mean to use --weight option?\
                \nUnsuitable input file... Quitting program')
                quit()
        #print(cofactors)
        print('done.')
        #cofactors.to_file("cofactors.lp")

    elif cofactors_txt:
        print('Reading cofactors from ', cofactors_txt)
        with open(cofactors_txt,'r') as f:
            cofactors_list = f.read().splitlines()
        cofactors = TermSet()
        for elem in cofactors_list:
            if '\t' in elem:
                print('A tabulated file was given as input cofactors. \
                \nAre you sure you did not mean to use the weight option? \
                \nUnsuitable input file... Quitting program')
                quit()
            if suffix != None:
                cofactors.add(Term('cofactor', ["\""+convert_to_coded_id(elem) + suffix + "\""]))
            else:
                cofactors.add(Term('cofactor', ["\""+convert_to_coded_id(elem) + "\""]))
        #print(cofactors)
        print('done.')
        #cofactors.to_file("cofactors.lp")

    else:
        print('No cofactor file is given as input.')
        print('Research of cofactors will be done in the network itself')
        species_and_weights = sbml.make_weighted_list_of_species(draft_sbml)
        cofactors = TermSet()
        for elem in species_and_weights:
            cofactors.add(Term('cofactor', ["\""+elem+"\"", species_and_weights[elem]]))
        weights = True

    print('\nChecking draft network for unproducible targets before cofactors selection ...', end='')
    sys.stdout.flush()
    model = query.get_unproducible(draftnet, targets, seeds)
    unprod = [p.arg(0) for p in model if p.pred() == 'unproducible_target']
    print('done.')
    print(' ',len(unprod),'unproducible targets:')
    utils.print_met(model.to_list())

    print('\nChecking minimal sets of cofactors to produce all targets ...', end='')
    sys.stdout.flush()
    if weights:
        model = query.get_cofs_weighted(draftnet, targets, seeds, cofactors)
        optimum = model.score
        if len(optimum) == 2:
            # it means that all targets can be produced with the selected cofactors
            optimum = [0] + optimum
        optimum = ','.join(map(str, optimum))
        #print(optimum)

    else:
        model = query.get_cofs(draftnet, targets, seeds, cofactors)
        optimum = model.score
        if len(optimum) == 1:
            # it means that all targets can be produced with the selected cofactors
            optimum = [0] + optimum
        optimum = ','.join(map(str, optimum))
    #print('done.')
    print('Optimum score {}'.format(optimum))
    solumodel = model.to_list()
    unproduced_targets = []
    chosen_cofactors = []
    newly_producible_targets = []
    for p in solumodel:
        if p.pred() == "needed_cof":
            cof = p.arg(0)
            try:
                weight = p.arg(1)
            except:
                weight = None
            chosen_cofactors.append((cof,weight))
        elif p.pred() == "still_unprod":
            tgt = p.arg(0)
            unproduced_targets.append(tgt)
        else:
            newly_producible_targets.append(p.arg(0))
    print('Still '+ str(len(unproduced_targets)) + ' unproducible targets:')
    print(*unproduced_targets, sep='\n')
    print('\nSelected cofactors:')
    for cofactor in chosen_cofactors:
        if cofactor[1] == None:
            print(cofactor[0])
        else:
            print(cofactor[0] + ' (' + cofactor[1] + ')')
    print('\n' + str(len(newly_producible_targets))+' newly producible targets:')
    print(str(newly_producible_targets))


    print('\nIntersection of solutions') # with size', optimum, '
    model = query.get_intersection_of_optimal_solutions_cof(draftnet, seeds, targets, cofactors, optimum, weights)
    solumodel = model.to_list()
    icofactors = []
    for p in solumodel:
        if p.pred() == "needed_cof":
            cof = p.arg(0)
            try:
                weight = p.arg(1)
            except:
                weight = None
            icofactors.append((cof,weight))
        #print('\nSelected cofactors:')
    for cofactor in icofactors:
        if cofactor[1] == None:
            print(cofactor[0])
        else:
            print(cofactor[0] + ' (' + cofactor[1] + ')')

    print('\nUnion of solutions') # with size', optimum, '
    model = query.get_union_of_optimal_solutions_cof(draftnet, seeds, targets, cofactors, optimum, weights)
    solumodel = model.to_list()
    icofactors = []
    for p in solumodel:
        if p.pred() == "needed_cof":
            cof = p.arg(0)
            try:
                weight = p.arg(1)
            except:
                weight = None
            icofactors.append((cof,weight))
        #print('\nSelected cofactors:')
    for cofactor in icofactors:
        if cofactor[1] == None:
            print(cofactor[0])
        else:
            print(cofactor[0] + ' (' + cofactor[1] + ')')

    if enumerate:
        print('\nComputing all completions with size ',optimum)
        models =  query.get_optimal_solutions_cof(draftnet, seeds, targets, cofactors, optimum, weights)
        count = 1
        for model in models:
            print('\nSolution '+str(count)+':')
            count+=1
            ccofactors = []
            solumodel = model.to_list()
            for p in solumodel:
                if p.pred() == "needed_cof":
                    cof = p.arg(0)
                    try:
                        weight = p.arg(1)
                    except:
                        weight = None
                    ccofactors.append((cof,weight))
            #print('\nSelected cofactors:')
            for cofactor in ccofactors:
                if cofactor[1] == None:
                    print(cofactor[0])
                else:
                    print(cofactor[0] + ' (' + cofactor[1] + ')')

    utils.clean_up()
    quit()
