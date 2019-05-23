#!/usr/bin/python
#-*- coding: utf-8 -*-

import subprocess

from menetools import run_menecof, run_menescope, run_menecheck, run_menepath

def test_menecof():
    unproducible_targets = set(['M_T2_c', 'M_T1_c'])
    optimum_score = '1,2,31'
    selected_cofactors = set([('"M_c_c"', '1'), ('"M_T1_c"', '2')])
    newly_producible_targets = set(['"M_T2_c"', '"M_T1_c"'])
    intersections = set([('"M_c_c"', '1'), ('"M_T1_c"', '2')])
    unions = set([('"M_c_c"', '1'), ('"M_T1_c"', '2')])

    results = run_menecof('../toy/tiny_toy/draft.xml', '../toy/tiny_toy/seeds.xml', '../toy/tiny_toy/targets.xml')

    assert set(results[5]) == unproducible_targets
    assert results[1] == optimum_score
    assert set(results[4]) == selected_cofactors
    assert set(results[6]) == newly_producible_targets
    assert set(results[3]) == intersections
    assert set(results[2]) == unions

def test_menescope():
    scope = 8
    compounds = ['M_e_c', 'M_g_c', 'M_S_c', 'M_f_c', 'M_S_b', 'M_i_c', 'M_d_c', 'M_T3_c']
    results = run_menescope('../toy/tiny_toy/draft.xml', '../toy/tiny_toy/seeds.xml')

    assert set(results) == set(compounds)
    assert len(results) == scope

def test_menecheck():
    producible_targets = ['M_T3_c']
    unproducible_targets = ['M_T2_c', 'M_T1_c']
    results = run_menecheck('../toy/tiny_toy/draft.xml', '../toy/tiny_toy/seeds.xml', '../toy/tiny_toy/targets.xml')
    unproducible_results = results[0] 
    producible_results = results[1]

    assert set(producible_results) == set(producible_targets)
    assert len(producible_results) == len(producible_targets)

    assert set(unproducible_results) == set(unproducible_targets)
    assert len(unproducible_results) == len(unproducible_targets)

def test_menepath():
    unproducible_targets = set(['"M_T1_c"', '"M_T2_c"'])
    one_solution = set(['"R_4"', '"R_5"', '"R_3"'])
    intersections = set(['"R_4"', '"R_5"', '"R_3"'])
    unions = set(['"R_5"', '"R_4"', '"R_3"', '"R_boundary"', '"R_import_S"'])

    results = run_menepath('../toy/tiny_toy/draft.xml', '../toy/tiny_toy/seeds.xml', '../toy/tiny_toy/targets.xml')
    unproducible_results = [term.args()[0] for term in results[1].to_list()]
    one_solution_results = [term.args()[0] for term in results[2].to_list()]
    union_results = [term.args()[0] for term in results[3].to_list()]
    intersection_results = [term.args()[0] for term in results[4].to_list()]

    assert set(unproducible_results) == unproducible_targets
    assert set(one_solution_results) == one_solution
    assert set(intersection_results) == intersections
    assert set(union_results) == unions


test_menepath()
test_menecheck
test_menecof
test_menescope
print('Done testing.')