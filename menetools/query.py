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

import os
import tempfile
import clyngor
import logging
from menetools import utils

logger = logging.getLogger('menetools.query')

root = os.path.dirname(__file__)
scope_prg = os.path.join(*[root, 'encodings', 'get_scope.lp'])
acti_prg = os.path.join(*[root, 'encodings', 'get_activated.lp'])
unproducible_prg = os.path.join(*[root, 'encodings', 'get_unproducible_targets.lp'])
path_prg = os.path.join(*[root, 'encodings', 'get_paths.lp'])
min_path_prg = os.path.join(*[root, 'encodings', 'get_min_paths.lp'])
cof_prg = os.path.join(*[root, 'encodings', 'get_cofs.lp'])
cof_w_prg = os.path.join(*[root, 'encodings', 'get_cofs_weighted.lp'])
dead_prg = os.path.join(*[root, 'encodings', 'get_deadends.lp'])
seed_prg = os.path.join(*[root, 'encodings', 'get_seeds.lp'])


def get_scope(draft, seeds):
    draft_f = utils.to_file(draft)
    seed_f =  utils.to_file(seeds)
    prg = [scope_prg, draft_f, seed_f]
    options = ''
    # solver = Gringo4Clasp()
    # models = solver.run(prg,collapseTerms=True,collapseAtoms=False)
    best_model = None
    models = clyngor.solve(prg, options=options, use_clingo_module=False)
    for model in models.discard_quotes.by_arity:
        best_model = model
    os.unlink(draft_f)
    os.unlink(seed_f)
    return best_model

def get_acti(draft, seeds):
    draft_f = utils.to_file(draft)
    seed_f =  utils.to_file(seeds)
    prg = [acti_prg, draft_f, seed_f]
    options = ''
    best_model = None
    models = clyngor.solve(prg, options=options, use_clingo_module=False)
    for model in models.discard_quotes.by_arity:
        best_model = model
    os.unlink(draft_f)
    os.unlink(seed_f)
    return best_model


def get_unproducible(draft, seeds, targets):
    draft_f = utils.to_file(draft)
    seed_f =  utils.to_file(seeds)
    target_f = utils.to_file(targets)
    prg = [unproducible_prg, draft_f, seed_f, target_f ]
    options = ''
    # solver = Gringo4Clasp()
    # models = solver.run(prg,collapseTerms=True,collapseAtoms=False)
    best_model = None
    models = clyngor.solve(prg, options=options, use_clingo_module=False)
    for model in models.discard_quotes.by_arity:
        best_model = model
    os.unlink(draft_f)
    os.unlink(seed_f)
    os.unlink(target_f)
    return best_model

def get_paths(instance, min_bool):
    instance_f = utils.to_file(instance)
    if min_bool:
        prg = [min_path_prg, instance_f]
    else:
        prg = [path_prg, instance_f]
    options ='--configuration jumpy --opt-strategy=usc,oll'
    # solver = Gringo4Clasp()
    # models = solver.run(prg,collapseTerms=True,collapseAtoms=False)
    best_model = None
    models = clyngor.solve(prg, options=options, use_clingo_module=False)
    for model in models.discard_quotes.by_arity.with_optimization:
        best_model = model

    return best_model #models[0]

def get_union_of_paths(instance, optimum, min_bool):
    instance_f = utils.to_file(instance)
    if min_bool:
        prg = [min_path_prg, instance_f]
        options ='--configuration jumpy --opt-strategy=usc,oll --enum-mode=brave --opt-mode=optN,'+str(optimum)
    else:
        prg = [path_prg, instance_f]
        options = '--configuration jumpy --opt-strategy=usc,oll --enum-mode=brave --opt-mode=ignore '
    # solver = Gringo4Clasp(clasp_options=options)
    # union = solver.run(prg, collapseTerms=True, collapseAtoms=False)
    models = clyngor.solve(prg, options=options, use_clingo_module=False)
    for model in models.discard_quotes.by_arity.with_optimization:
        best_model = model

    os.unlink(instance_f)
    return best_model #union[0]

def get_intersection_of_paths(instance, optimum, min_bool):
    instance_f = utils.to_file(instance)
    if min_bool:
        prg = [min_path_prg, instance_f]
        options = '--configuration jumpy --opt-strategy=usc,oll --enum-mode cautious --opt-mode=optN,' +str(optimum)
    else:
        prg = [path_prg, instance_f]
        options = '--configuration jumpy --opt-strategy=usc,oll --enum-mode cautious --opt-mode=ignore'
    models = clyngor.solve(prg, options=options, use_clingo_module=False)
    for model in models.discard_quotes.by_arity.with_optimization:
        best_model = model
    # solver = Gringo4Clasp(clasp_options=options)
    # intersec = solver.run(prg, collapseTerms=True, collapseAtoms=False)
    #print(os.path.abspath(instance_f))
    os.unlink(instance_f)
    return best_model #intersec[0]

def get_all_paths(instance, optimum, min_bool, nmodels=0):
    instance_f = utils.to_file(instance)
    if min_bool:
        prg = [min_path_prg, instance_f]
        options = '--configuration handy --opt-strategy=usc,oll --opt-mode=optN,' +str(optimum)
    else:
        prg = [path_prg, instance_f]
        options = '--configuration handy --opt-strategy=usc,oll --opt-mode=enum'
    # solver = Gringo4Clasp(clasp_options=options)
    # models = solver.run(prg, collapseTerms=True, collapseAtoms=False)
    models = clyngor.solve(prg, options=options, nb_model=nmodels, use_clingo_module=False).by_arity
    if min_bool:
        allmodels = clyngor.opt_models_from_clyngor_answers(models)
    else:
        allmodels = models
    # allmodels = [model for model in models.by_arity.with_optimization]
    # os.unlink(instance_f)
    return allmodels

def get_cofs(draft, seeds, targets, cofactors):
    draft_f = utils.to_file(draft)
    seed_f =  utils.to_file(seeds)
    targets_f =  utils.to_file(targets)
    cofactors_f =  utils.to_file(cofactors)
    prg = [cof_prg, draft_f, seed_f, targets_f, cofactors_f]
    # solver = Gringo4Clasp()
    # models = solver.run(prg,collapseTerms=True,collapseAtoms=False)
    #print(models)
    # print(os.path.abspath(draft_f))
    # print(os.path.abspath(seed_f))
    # print(os.path.abspath(targets_f))
    # print(os.path.abspath(cofactors_f))
    best_model = None
    options = ''
    models = clyngor.solve(prg, options=options, use_clingo_module=False)
    for model in models.discard_quotes.by_arity.with_optimization:
        best_model = model
    os.unlink(draft_f)
    os.unlink(seed_f)
    os.unlink(targets_f)
    os.unlink(cofactors_f)

    return best_model #models[0]

def get_cofs_weighted(draft, seeds, targets, cofactors):
    draft_f = utils.to_file(draft)
    seed_f =  utils.to_file(seeds)
    targets_f =  utils.to_file(targets)
    cofactors_f =  utils.to_file(cofactors)
    prg = [cof_w_prg, draft_f, seed_f, targets_f, cofactors_f]
    options ='--configuration jumpy --opt-strategy=usc,oll'
    # solver = Gringo4Clasp(clasp_options='--configuration jumpy --opt-strategy=usc,oll')
    # models = solver.run(prg,collapseTerms=True,collapseAtoms=False)
    #print(models)
    # print(os.path.abspath(draft_f))
    # print(os.path.abspath(seed_f))
    # print(os.path.abspath(targets_f))
    # print(os.path.abspath(cofactors_f))
    best_model = None
    models = clyngor.solve(prg, options=options, use_clingo_module=False)
    for model in models.discard_quotes.by_arity.with_optimization:
        best_model = model
    os.unlink(draft_f)
    os.unlink(seed_f)
    os.unlink(targets_f)
    os.unlink(cofactors_f)
    return best_model #models[0]

def get_intersection_of_optimal_solutions_cof(draft, seeds, targets, cofactors, optimum, weighted=False):
    draft_f = utils.to_file(draft)
    seed_f =  utils.to_file(seeds)
    targets_f =  utils.to_file(targets)
    cofactors_f =  utils.to_file(cofactors)
    if weighted:
        prg = [cof_w_prg, draft_f, seed_f, targets_f, cofactors_f]
    else:
        prg = [cof_prg, draft_f, seed_f, targets_f, cofactors_f]
    options='--configuration jumpy --opt-strategy=usc,oll --enum-mode=cautious --opt-mode=optN,'+str(optimum)
    best_model = None
    models = clyngor.solve(prg, options=options, use_clingo_module=False)
    for model in models.discard_quotes.by_arity.with_optimization:
        best_model = model
    # solver = Gringo4Clasp(clasp_options=options)
    # intersec = solver.run(prg, collapseTerms=True, collapseAtoms=False)
    os.unlink(draft_f)
    os.unlink(seed_f)
    os.unlink(targets_f)
    os.unlink(cofactors_f)
    return best_model #models[0]


def get_union_of_optimal_solutions_cof(draft, seeds, targets, cofactors, optimum, weighted=False):
    draft_f = utils.to_file(draft)
    seed_f =  utils.to_file(seeds)
    targets_f =  utils.to_file(targets)
    cofactors_f =  utils.to_file(cofactors)
    if weighted:
        prg = [cof_w_prg, draft_f, seed_f, targets_f, cofactors_f]
    else:
        prg = [cof_prg, draft_f, seed_f, targets_f, cofactors_f]
    options='--configuration jumpy --opt-strategy=usc,oll --enum-mode=cautious --opt-mode=optN,'+str(optimum)
    # solver = Gringo4Clasp(clasp_options=options)
    # union = solver.run(prg, collapseTerms=True, collapseAtoms=False)
    best_model = None
    models = clyngor.solve(prg, options=options, use_clingo_module=False)
    for model in models.discard_quotes.by_arity.with_optimization:
        best_model = model
    os.unlink(draft_f)
    os.unlink(seed_f)
    os.unlink(targets_f)
    os.unlink(cofactors_f)
    return best_model #models[0]


def get_optimal_solutions_cof(draft, seeds, targets, cofactors, optimum, weighted, nmodels=0):
    draft_f = utils.to_file(draft)
    seed_f =  utils.to_file(seeds)
    targets_f =  utils.to_file(targets)
    cofactors_f =  utils.to_file(cofactors)
    if weighted:
        prg = [cof_w_prg, draft_f, seed_f, targets_f, cofactors_f]
    else:
        prg = [cof_prg, draft_f, seed_f, targets_f, cofactors_f]
    options = '--configuration jumpy --opt-strategy=usc,oll --opt-mode=enum,' +str(optimum)
    # solver = Gringo4Clasp(clasp_options=options)
    # models = solver.run(prg, collapseTerms=True, collapseAtoms=False)
    models = clyngor.solve(prg, options=options, use_clingo_module=False)
    # print(os.path.abspath(draft_f), os.path.abspath(seed_f), os.path.abspath(targets_f), os.path.abspath(cofactors_f))
    allmodels = [model for model in models.by_arity.with_optimization]
    os.unlink(draft_f)
    os.unlink(seed_f)
    os.unlink(targets_f)
    os.unlink(cofactors_f)
    return allmodels

def get_dead(draft):
    draft_f = utils.to_file(draft)

    prg = [dead_prg, draft_f]
    options = ''
    models = clyngor.solve(prg, options=options, use_clingo_module=False)
    for model in models.discard_quotes.by_arity:
        best_model = model

    return best_model

def get_seed(draft):
    draft_f = utils.to_file(draft)
    prg = [seed_prg, draft_f]
    options = ''
    models = clyngor.solve(prg, options=options, use_clingo_module=False)
    for model in models.discard_quotes.by_arity:
        best_model = model
    return best_model