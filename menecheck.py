#!python
# -*- coding: utf-8 -*-
import argparse
import sys
from pyasp.asp import *
from menetools import query, utils, sbml

if __name__ == '__main__':


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

    print('Reading draft network from ',draft_sbml,'...',end=' ')
    sys.stdout.flush()
    draftnet = sbml.readSBMLnetwork(draft_sbml, 'draft')
    print('done.')

    print('Reading seeds from ',seeds_sbml,'...',end=' ')
    sys.stdout.flush()
    seeds = sbml.readSBMLspecies(seeds_sbml, 'seed')
    print('done.')

    print('Reading targets from ',targets_sbml,'...',end=' ')
    sys.stdout.flush()
    targets = sbml.readSBMLspecies(targets_sbml, 'target')
    print('done.')

    print('\nChecking draftnet for unproducible targets ...',end=' ')
    sys.stdout.flush()
    model = query.get_unproducible(draftnet, targets, seeds)
    # print(model)
    print('done.')
    #utils.print_met(model.to_list())
    unprod = []
    prod = []
    for a in model :
        if a.pred() == 'unproducible_target':
            unprod.append(a.arg(0))
        elif a.pred() == 'producible_target':
            prod.append(a.arg(0))
    print(str(len(prod)),'producible targets:')
    print(*prod, sep='\n')
    print('\n')
    print(str(len(unprod)),'unproducible targets:')
    print(*unprod, sep='\n')


    utils.clean_up()
    quit()
