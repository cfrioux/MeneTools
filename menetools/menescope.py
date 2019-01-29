#!/usr/bin/python3
#-*- coding: utf-8 -*-

import argparse
import sys
import inspect
import os

from menetools import utils, query, sbml
from pyasp.asp import *



def cmd_menescope():
    parser = argparse.ArgumentParser()
    parser.add_argument("-d", "--draftnet",
                        help="metabolic network in SBML format", required=True)
    parser.add_argument("-s", "--seeds",
                        help="seeds in SBML format", required=True)

    args = parser.parse_args()

    draft_sbml = args.draftnet
    #repair_sbml = args.repairnetwork
    seeds_sbml = args.seeds
    run_menescope(draft_sbml,seeds_sbml)

def run_menescope(draft_sbml,seeds_sbml):
    print('Reading draft network from ', draft_sbml, '...', end='')
    sys.stdout.flush()
    draftnet = sbml.readSBMLnetwork(draft_sbml, 'draft')
    #print(draftnet)
    print('done.')

    print('Reading seeds from ', seeds_sbml, '...', end='')
    sys.stdout.flush()
    seeds = sbml.readSBMLspecies(seeds_sbml,'seed')
    #print(seeds)
    print('done.')
    #seeds.to_file("seeds.lp")

    print('\nChecking draft network scope ...', end='')
    sys.stdout.flush()
    model = query.get_scope(draftnet, seeds)
    print('done.')
    print(' ', len(model), 'compounds on scope:')
    utils.print_met(model.to_list())
    utils.clean_up()

    return model

if __name__ == '__main__':
    cmd_menescope()