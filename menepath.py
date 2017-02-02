#!/usr/bin/python3
#-*- coding: utf-8 -*-

import argparse
import sys
import inspect
import os
from pyasp.asp import *
from src import utils, query, sbml

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

    args = parser.parse_args()

    draft_sbml = args.draftnet
    seeds_sbml = args.seeds
    targets_sbml = args.targets

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
        print(t)
        single_target = TermSet()
        single_target.add(t)
        print('\nComputing topologically essential reactions for',t,'...',end=' ')
        sys.stdout.flush()
        essentials = query.get_intersection_of_paths(draftnet, seeds, single_target)
        print('done.')
        print(' ',len(essentials), 'essential reactions found:')
        utils.print_met(essentials.to_list())

    utils.clean_up()
    quit()
