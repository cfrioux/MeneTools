#!/usr/bin/python3
#-*- coding: utf-8 -*-

import argparse
import sys
import inspect
import os
from pyasp.term import *
from pyasp.asp import *
from menetools import utils, query, sbml

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

    parser.add_argument("--min",
                        help="call this option to obtain minimal-size paths",
                        required=False, action="store_true")

    parser.add_argument("--enumerate",
                        help="call this option for an enumeration of solutions",
                        required=False, action="store_true")

    args = parser.parse_args()

    draft_sbml = args.draftnet
    seeds_sbml = args.seeds
    targets_sbml = args.targets
    min_size = args.min
    enumeration = args.enumerate

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
    #seeds.to_file("targets.lp")

    print('\nChecking network for unproducible targets ...', end=' ')
    sys.stdout.flush()
    model = query.get_unproducible(draftnet, targets, seeds)
    print('done.')
    unproducible_targets = TermSet()
    producible_targets = TermSet()

    #print(model)
    for p in model:
        if p.pred() == "unproducible_target":
            tgt = p.arg(0)
            #print(tgt)
            unproducible_targets.add(Term('unproducible_targets', [tgt]))
        elif p.pred() == "producible_target":
            tgt = p.arg(0)
            producible_targets.add(Term('target', [tgt]))
            #producible_targets = TermSet(producible_targets.union(t))

    print(' ',len(unproducible_targets),'unproducible targets:')
    utils.print_met(model.to_list())



    #print(producible_targets)
    for t in producible_targets:
        print('\n')
        print(t)
        single_target = TermSet()
        single_target.add(t)

        draftfact  = String2TermSet('draft("draft")')
        lp_instance   = TermSet(draftnet.union(draftfact).union(single_target).union(seeds))

    # one solution, minimal or not, depending on option
        if min_size:
            print('\nComputing one solution of cardinality-minimal production paths for ', t)
        else:
            print('\nComputing one solution of production paths for',t,)
        one_model = query.get_paths(lp_instance, min_size)
        optimum = one_model.score
        print('Solution size ',len(one_model), ' reactions')
        utils.print_met(one_model.to_list())

    # union of solutions
        if min_size:
            print('\nComputing union of cardinality-minimal production paths for ', t)
        else:
            print('\nComputing union of production paths for',t,)
        union = query.get_union_of_paths(lp_instance, optimum, min_size)
        print('Union size ',len(union), ' reactions')
        utils.print_met(union.to_list())

    # intersection of solutions
        if min_size:
            print('\nComputing intersection of cardinality-minimal production paths for ', t)
        else:
            print('\nComputing intersection of production paths for',t,)
        intersection = query.get_intersection_of_paths(lp_instance, optimum, min_size)
        print('Intersection size (essential reactions) ',len(intersection), ' reactions')
        utils.print_met(intersection.to_list())

    # if wanted, get union of all solutions
        if enumeration:
            if min_size:
                print('\nComputing all cardinality-minimal production paths for ', t, ' - ', optimum)
            else:
                print('\nComputing all production paths for ', t, ' - ', optimum)

            all_models = query.get_all_paths(lp_instance, optimum, min_size)
            count = 1
            for model in all_models:
                print('\nSolution '+str(count) + ' of size :' + str(len(model)) + ' reactions:')
                count+=1
                utils.print_met(model.to_list())


    utils.clean_up()
    quit()
