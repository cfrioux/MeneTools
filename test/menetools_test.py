#!/usr/bin/python
#-*- coding: utf-8 -*-

import json
import os
import subprocess

from menetools import run_menecof, run_menescope, run_menecheck, run_menepath, run_meneacti


def test_menecof():
    print("*** test menecof ***")
    unproducible_targets = set(['M_T2_c', 'M_T1_c'])
    # optimum_score = '1,2,31'
    selected_cofactors = set([('M_c_c', 1), ('M_T1_c', 2)])
    newly_producible_targets = set(['M_T2_c', 'M_T1_c'])
    intersections = set([('M_c_c', 1), ('M_T1_c', 2)])
    unions = set([('M_c_c', 1), ('M_T1_c', 2)])

    results = run_menecof('../toy/tiny_toy/draft.xml', '../toy/tiny_toy/seeds.xml', '../toy/tiny_toy/targets.xml')
    print(unions)
    print(results[2])
    assert set(results[5]) == unproducible_targets
    # assert results[1] == optimum_score
    assert set(results[4]) == selected_cofactors
    assert set(results[6]) == newly_producible_targets
    assert set(results[3]) == intersections
    assert set(results[2]) == unions


def test_menecof_cli():
    print("*** test menecof cli ***")
    unproducible_targets = set(['M_T2_c', 'M_T1_c'])
    selected_cofactors = set([('M_c_c', 1), ('M_T1_c', 2)])
    newly_producible_targets = set(['M_T2_c', 'M_T1_c'])
    intersections = set([('M_c_c', 1), ('M_T1_c', 2)])
    unions = set([('M_c_c', 1), ('M_T1_c', 2)])

    subprocess.call(['mene', 'cof', '-d', '../toy/tiny_toy/draft.xml',
                        '-s', '../toy/tiny_toy/seeds.xml', '-t', '../toy/tiny_toy/targets.xml',
                        '--output', 'test.json'])

    results = json.loads(open('test.json', 'r').read())

    assert set(results['unprod']) == unproducible_targets
    chosen_cofactors = set([tuple(list_cof) for list_cof in results['chosen_cofactors']])
    assert chosen_cofactors == selected_cofactors
    assert set(results['newly_producible_targets']) == newly_producible_targets
    intersection_icofactors = set([tuple(list_cof) for list_cof in results['intersection_icofactors']])
    assert intersection_icofactors == intersections
    union_icofactors = set([tuple(list_cof) for list_cof in results['union_icofactors']])
    assert union_icofactors == unions
    os.remove('test.json')


def test_menescope():
    print("*** test menescope ***")
    scope = 8
    compounds = ['M_e_c', 'M_g_c', 'M_S_c', 'M_f_c', 'M_S_b', 'M_i_c', 'M_d_c', 'M_T3_c']
    results = run_menescope('../toy/tiny_toy/draft.xml', '../toy/tiny_toy/seeds.xml')

    assert set(results) == set(compounds)
    assert len(results) == scope


def test_menescope_cli():
    print("*** test menescope cli ***")
    scope = 8
    compounds = ['M_e_c', 'M_g_c', 'M_S_c', 'M_f_c', 'M_S_b', 'M_i_c', 'M_d_c', 'M_T3_c']

    subprocess.call(['mene', 'scope', '-d', '../toy/tiny_toy/draft.xml',
                        '-s', '../toy/tiny_toy/seeds.xml',  '--output', 'test.json'])

    results = json.loads(open('test.json', 'r').read())

    assert set(results['scope']) == set(compounds)
    assert len(results['scope']) == scope
    os.remove('test.json')


def test_meneacti():
    print("*** test meneacti ***")
    activ = 7
    reactions = ['R_boundary', 'R_import_S', 'R_7', 'R_5', 'R_4', 'R_3', 'R_6']
    results = run_meneacti('../toy/tiny_toy/draft.xml', '../toy/tiny_toy/seeds.xml')

    assert set(results) == set(reactions)
    assert len(results) == activ


def test_meneacti_cli():
    print("*** test meneacti cli ***")
    activ = 7
    reactions = ['R_boundary', 'R_import_S', 'R_7', 'R_5', 'R_4', 'R_3', 'R_6']

    subprocess.call(['mene', 'acti', '-d', '../toy/tiny_toy/draft.xml',
                        '-s', '../toy/tiny_toy/seeds.xml',  '--output', 'test.json'])

    results = json.loads(open('test.json', 'r').read())

    assert set(results['activ']) == set(reactions)
    assert len(results['activ']) == activ
    os.remove('test.json')


def test_menecheck():
    print("*** test menecheck ***")
    producible_targets = ['M_T3_c']
    unproducible_targets = ['M_T2_c', 'M_T1_c']
    results = run_menecheck('../toy/tiny_toy/draft.xml', '../toy/tiny_toy/seeds.xml', '../toy/tiny_toy/targets.xml')
    unproducible_results = results[0] 
    producible_results = results[1]

    assert set(producible_results) == set(producible_targets)
    assert len(producible_results) == len(producible_targets)

    assert set(unproducible_results) == set(unproducible_targets)
    assert len(unproducible_results) == len(unproducible_targets)

def test_menecheck_cli():
    print("*** test menecheck cli ***")
    producible_targets = ['M_T3_c']
    unproducible_targets = ['M_T2_c', 'M_T1_c']

    subprocess.call(['mene', 'check', '-d', '../toy/tiny_toy/draft.xml',
                        '-s', '../toy/tiny_toy/seeds.xml',   '-t', '../toy/tiny_toy/targets.xml',
                        '--output', 'test.json'])

    results = json.loads(open('test.json', 'r').read())
    print(results)
    assert set(results['producible_target']) == set(producible_targets)
    assert len(results['producible_target']) == len(producible_targets)

    assert set(results['unproducible_target']) == set(unproducible_targets)
    assert len(results['unproducible_target']) == len(unproducible_targets)
    os.remove('test.json')


def test_menepath():
    print("*** test menepath ***")
    unproducible_targets = set(['M_T1_c', 'M_T2_c'])
    one_solution = set(['R_4', 'R_5', 'R_3'])
    intersections = set(['R_4', 'R_5', 'R_3'])
    unions = set(['R_5', 'R_4', 'R_3', 'R_boundary', 'R_import_S'])

    results = run_menepath('../toy/tiny_toy/draft.xml', '../toy/tiny_toy/seeds.xml', '../toy/tiny_toy/targets.xml')
    unproducible_results = results[1]
    one_solution_results = results[2]
    union_results = results[3]
    intersection_results = results[4]

    assert set(unproducible_results) == unproducible_targets
    # assert set(one_solution_results) == one_solution
    assert set(intersection_results) == intersections
    assert set(union_results) == unions


def test_menepath_cli():
    print("*** test menepath cli ***")
    unproducible_targets = set(['M_T1_c', 'M_T2_c'])
    intersections = set(['R_4', 'R_5', 'R_3'])
    unions = set(['R_5', 'R_4', 'R_3', 'R_boundary', 'R_import_S'])

    subprocess.call(['mene', 'path', '-d', '../toy/tiny_toy/draft.xml',
                        '-s', '../toy/tiny_toy/seeds.xml',   '-t', '../toy/tiny_toy/targets.xml',
                        '--output', 'test.json'])

    results = json.loads(open('test.json', 'r').read())

    assert set(results['unproducible_targets_lst']) == unproducible_targets
    assert set(results['intersection_path']) == intersections
    assert set(results['union_path']) == unions
    os.remove('test.json')


if __name__ == "__main__":
    test_menepath()
    test_menecheck()
    test_menecof()
    test_menescope()
    print('Done testing.')
