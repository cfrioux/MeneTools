#!/usr/bin/python
#-*- coding: utf-8 -*-

import json
import os
import pytest
import subprocess

from menetools import run_menecof, run_menescope, run_menecheck, run_menepath, run_meneacti, run_menedead, run_meneseed, run_menescope_inc
from menetools import sbml, utils

DRAFT_PATH = os.path.join(*['..', 'toy', 'tiny_toy', 'draft.xml'])
SEED_PATH = os.path.join(*['..', 'toy', 'tiny_toy', 'seeds.xml'])
TARGETS_PATH = os.path.join(*['..', 'toy', 'tiny_toy', 'targets.xml'])

MENEINC_DRAFT_PATH = os.path.join('mene_scope_inc', 'network.sbml')
MENEINC_SEED_PATH = os.path.join('mene_scope_inc', 'seeds.sbml')
MENEINC_UNCORRECT_SEED_PATH = os.path.join('mene_scope_inc', 'uncorrect_seeds.sbml')
MENEINC_TARGETS_PATH = os.path.join('mene_scope_inc', 'targets.sbml')
TEST_DIR = os.path.dirname(__file__)


def _test_file_path(*parts):
    return os.path.normpath(os.path.join(TEST_DIR, *parts))


def _seed_atoms_to_compounds(seed_atoms):
    return {atom.args()[0].strip('"') for atom in seed_atoms}


def test_seed_parsing_tiny_toy_sbml_and_list():
    expected_compounds = {'M_S_c', 'M_foo_c', 'M_l_c'}
    tiny_toy_seed_sbml = _test_file_path('..', 'toy', 'tiny_toy', 'seeds.xml')
    tiny_toy_seed_list = _test_file_path('..', 'toy', 'tiny_toy', 'seeds.list')

    sbml_compounds = _seed_atoms_to_compounds(
        sbml.readSBMLspecies_clyngor(tiny_toy_seed_sbml, 'seed')
    )
    list_compounds = _seed_atoms_to_compounds(
        utils.read_flat_atoms_clyngor(tiny_toy_seed_list, 'seed')
    )

    assert sbml_compounds == expected_compounds
    assert list_compounds == expected_compounds
    assert list_compounds == sbml_compounds


def test_seed_parsing_toy_sbml_and_list():
    toy_seed_sbml = _test_file_path('..', 'toy', 'seeds.sbml')
    toy_seed_list = _test_file_path('..', 'toy', 'seeds.list')

    sbml_compounds = _seed_atoms_to_compounds(
        sbml.readSBMLspecies_clyngor(toy_seed_sbml, 'seed')
    )
    list_compounds = _seed_atoms_to_compounds(
        utils.read_flat_atoms_clyngor(toy_seed_list, 'seed')
    )

    assert list_compounds == sbml_compounds
    assert 'ADP' in list_compounds
    assert 'K+_CCO-BOUNDARY' in list_compounds


def test_seed_parsing_toy_complete_compound_set():
    expected_compounds = set("""
        ADP
        CPD-69_CCO-BOUNDARY
        AMP_CCO-BOUNDARY
        RHAMNOSE_CCO-BOUNDARY
        GLN_CCO-BOUNDARY
        GLYCOLLATE_CCO-BOUNDARY
        TREHALOSE_CCO-BOUNDARY
        AMMONIUM_CCO-BOUNDARY
        DEOXYADENOSINE_CCO-BOUNDARY
        CARNITINE_CCO-BOUNDARY
        N-ACETYL-D-GLUCOSAMINE_CCO-BOUNDARY
        S2O3_CCO-BOUNDARY
        D-ALANINE_CCO-BOUNDARY
        D-GALACTONATE_CCO-BOUNDARY
        RIBOSE_CCO-BOUNDARY
        DEOXYCYTIDINE_CCO-BOUNDARY
        Glucose-6-phosphate_CCO-BOUNDARY
        D-Galactose_CCO-BOUNDARY
        GALACTITOL_CCO-BOUNDARY
        OXYGEN-MOLECULE_CCO-BOUNDARY
        SUC_CCO-BOUNDARY
        BETAINE_CCO-BOUNDARY
        ACETALD_CCO-BOUNDARY
        NICOTINAMIDE_NUCLEOTIDE_CCO-BOUNDARY
        GLYCERALD_CCO-BOUNDARY
        THYMIDINE_CCO-BOUNDARY
        LEU_CCO-BOUNDARY
        GUANINE_CCO-BOUNDARY
        URACIL_CCO-BOUNDARY
        TARTRATE_CCO-BOUNDARY
        L-ASPARTATE_CCO-BOUNDARY
        ILE_CCO-BOUNDARY
        2-KETOGLUTARATE_CCO-BOUNDARY
        TYR_CCO-BOUNDARY
        Alpha-lactose_CCO-BOUNDARY
        D-SERINE_CCO-BOUNDARY
        CARBON-DIOXIDE_CCO-BOUNDARY
        XANTHINE_CCO-BOUNDARY
        ARG_CCO-BOUNDARY
        CADAVERINE_CCO-BOUNDARY
        PUTRESCINE_CCO-BOUNDARY
        SULFATE_CCO-BOUNDARY
        3-KETOBUTYRATE_CCO-BOUNDARY
        D-GALACTARATE_CCO-BOUNDARY
        MALTOSE_CCO-BOUNDARY
        MALTOTETRAOSE_CCO-BOUNDARY
        GUANOSINE_CCO-BOUNDARY
        TRP_CCO-BOUNDARY
        TRIMETHYLAMINE_CCO-BOUNDARY
        GLUCOSAMINE_CCO-BOUNDARY
        L-LACTATE_CCO-BOUNDARY
        CYTIDINE_CCO-BOUNDARY
        SUCROSE_CCO-BOUNDARY
        CYTOSINE_CCO-BOUNDARY
        D-LACTATE_CCO-BOUNDARY
        MET_CCO-BOUNDARY
        CYS_CCO-BOUNDARY
        COB-I-ALAMIN_CCO-BOUNDARY
        HYPOXANTHINE_CCO-BOUNDARY
        3-HYDROXYPHENYL-PROPIONATE_CCO-BOUNDARY
        PALMITATE_CCO-BOUNDARY
        MANNITOL_CCO-BOUNDARY
        NITRITE_CCO-BOUNDARY
        GAMMA-BUTYROBETAINE_CCO-BOUNDARY
        ETOH_CCO-BOUNDARY
        D-GLUCARATE_CCO-BOUNDARY
        CHOLINE_CCO-BOUNDARY
        PROPANE-1-2-DIOL_CCO-BOUNDARY
        3-PHENYLPROPIONATE_CCO-BOUNDARY
        NA+_CCO-BOUNDARY
        MANNOSE_CCO-BOUNDARY
        TRIMENTHLAMINE-N-O_CCO-BOUNDARY
        MALTOPENTAOSE_CCO-BOUNDARY
        Pi_CCO-BOUNDARY
        GLY_CCO-BOUNDARY
        NAD_CCO-BOUNDARY
        L-IDONATE_CCO-BOUNDARY
        CPD-218_CCO-BOUNDARY
        DEOXYURIDINE_CCO-BOUNDARY
        ACET_CCO-BOUNDARY
        GLT_CCO-BOUNDARY
        FRU_CCO-BOUNDARY
        GLUCONATE_CCO-BOUNDARY
        MALTOHEXAOSE_CCO-BOUNDARY
        GLUCURONATE_CCO-BOUNDARY
        PYRUVATE_CCO-BOUNDARY
        Mannose-6-phosphate_CCO-BOUNDARY
        GLYCEROL_CCO-BOUNDARY
        INDOLE_CCO-BOUNDARY
        D-GALACTURONATE_CCO-BOUNDARY
        NITRATE_CCO-BOUNDARY
        ADENOSINE_CCO-BOUNDARY
        FUM_CCO-BOUNDARY
        LYS_CCO-BOUNDARY
        PHE_CCO-BOUNDARY
        MELIBIOSE_CCO-BOUNDARY
        THR_CCO-BOUNDARY
        DIHYDROXYACETONE_CCO-BOUNDARY
        DMSO_CCO-BOUNDARY
        SER_CCO-BOUNDARY
        ASN_CCO-BOUNDARY
        WATER_CCO-BOUNDARY
        ALLANTOIN_CCO-BOUNDARY
        N-ACETYLNEURAMINATE_CCO-BOUNDARY
        PANTOTHENATE_CCO-BOUNDARY
        CPD-10797_CCO-BOUNDARY
        XANTHOSINE_CCO-BOUNDARY
        ADENINE_CCO-BOUNDARY
        THIAMINE_CCO-BOUNDARY
        URIDINE_CCO-BOUNDARY
        FORMATE_CCO-BOUNDARY
        BUTYRIC_ACID_CCO-BOUNDARY
        L-ALPHA-ALANINE_CCO-BOUNDARY
        CPD-488_CCO-BOUNDARY
        DEOXYGUANOSINE_CCO-BOUNDARY
        2-DEHYDRO-3-DEOXY-D-GLUCONATE_CCO-BOUNDARY
        GLYCEROL-3P_CCO-BOUNDARY
        CPD-7836_CCO-BOUNDARY
        FE+2_CCO-BOUNDARY
        SORBITOL_CCO-BOUNDARY
        INOSINE_CCO-BOUNDARY
        MALTOTRIOSE_CCO-BOUNDARY
        HIS_CCO-BOUNDARY
        PROTON_CCO-BOUNDARY
        N-ACETYL-D-MANNOSAMINE_CCO-BOUNDARY
        STEARIC_ACID_CCO-BOUNDARY
        MAL_CCO-BOUNDARY
        XYLOSE_CCO-BOUNDARY
        4-AMINO-BUTYRATE_CCO-BOUNDARY
        CPD-7670_CCO-BOUNDARY
        L-ORNITHINE_CCO-BOUNDARY
        CIT_CCO-BOUNDARY
        DEOXYINOSINE_CCO-BOUNDARY
        VAL_CCO-BOUNDARY
        ALPHA-GLUCOSE_CCO-BOUNDARY
        NIACINE_CCO-BOUNDARY
        MESO-DIAMINOPIMELATE_CCO-BOUNDARY
        SPERMIDINE_CCO-BOUNDARY
        UREA_CCO-BOUNDARY
        TAURINE_CCO-BOUNDARY
        L-ARABINOSE_CCO-BOUNDARY
        L-fucoses_CCO-BOUNDARY
        PRO_CCO-BOUNDARY
        K+_CCO-BOUNDARY
    """.split())
    toy_seed_sbml = _test_file_path('..', 'toy', 'seeds.sbml')
    toy_seed_list = _test_file_path('..', 'toy', 'seeds.list')

    sbml_compounds = _seed_atoms_to_compounds(
        sbml.readSBMLspecies_clyngor(toy_seed_sbml, 'seed')
    )
    list_compounds = _seed_atoms_to_compounds(
        utils.read_flat_atoms_clyngor(toy_seed_list, 'seed')
    )

    assert sbml_compounds == expected_compounds
    assert list_compounds == expected_compounds


def test_menecof():
    print("*** test menecof ***")
    unproducible_targets = set(['M_T2_c', 'M_T1_c'])
    # optimum_score = '1,2,31'
    selected_cofactors = set([('M_c_c', 1), ('M_T1_c', 2)])
    newly_producible_targets = set(['M_T2_c', 'M_T1_c'])
    intersections = set([('M_c_c', 1), ('M_T1_c', 2)])
    unions = set([('M_c_c', 1), ('M_T1_c', 2)])


    results = run_menecof(DRAFT_PATH, SEED_PATH, TARGETS_PATH)
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

    subprocess.call(['mene', 'cof', '-d', DRAFT_PATH,
                        '-s', SEED_PATH, '-t', TARGETS_PATH,
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
    scope = 9
    compounds = ['M_e_c', 'M_g_c', 'M_S_c', 'M_f_c', 'M_S_b', 'M_i_c', 'M_d_c', 'M_T3_c', 'M_l_c']
    seeds_produced = ['M_S_c']
    missing_seeds = ['M_foo_c']
    seeds_non_produced = ['M_l_c']
    results = run_menescope(DRAFT_PATH, SEED_PATH)

    assert set(results['scope']) == set(compounds)
    assert len(results['scope']) == scope
    assert set(results['produced_seeds']) == set(seeds_produced)
    assert set(results['non_produced_seeds']) == set(seeds_non_produced)
    assert set(results['absent_seeds']) == set(missing_seeds)


def test_menescope_cli():
    print("*** test menescope cli ***")
    scope = 9
    compounds = ['M_e_c', 'M_g_c', 'M_S_c', 'M_f_c', 'M_S_b', 'M_i_c', 'M_d_c', 'M_T3_c', 'M_l_c']
    seeds_produced = ['M_S_c']
    missing_seeds = ['M_foo_c']
    seeds_non_produced = ['M_l_c']

    subprocess.call(['mene', 'scope', '-d', DRAFT_PATH,
                        '-s', SEED_PATH,  '--output', 'test.json'])

    results = json.loads(open('test.json', 'r').read())

    assert set(results['scope']) == set(compounds)
    assert len(results['scope']) == scope
    assert set(results['produced_seeds']) == set(seeds_produced)
    assert set(results['non_produced_seeds']) == set(seeds_non_produced)
    assert set(results['absent_seeds']) == set(missing_seeds)
    os.remove('test.json')


def test_meneacti():
    print("*** test meneacti ***")
    activ = 7
    reactions = ['R_boundary', 'R_import_S', 'R_7', 'R_5', 'R_4', 'R_3', 'R_6']
    results = run_meneacti(DRAFT_PATH, SEED_PATH)

    assert set(results) == set(reactions)
    assert len(results) == activ


def test_meneacti_cli():
    print("*** test meneacti cli ***")
    activ = 7
    reactions = ['R_boundary', 'R_import_S', 'R_7', 'R_5', 'R_4', 'R_3', 'R_6']

    subprocess.call(['mene', 'acti', '-d', DRAFT_PATH,
                        '-s', SEED_PATH,  '--output', 'test.json'])

    results = json.loads(open('test.json', 'r').read())

    assert set(results['activ']) == set(reactions)
    assert len(results['activ']) == activ
    os.remove('test.json')


def test_menecheck():
    print("*** test menecheck ***")
    producible_targets = ['M_T3_c']
    unproducible_targets = ['M_T2_c', 'M_T1_c']
    results = run_menecheck(DRAFT_PATH, SEED_PATH, TARGETS_PATH)
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

    subprocess.call(['mene', 'check', '-d', DRAFT_PATH,
                        '-s', SEED_PATH,   '-t', TARGETS_PATH,
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

    results = run_menepath(DRAFT_PATH, SEED_PATH, TARGETS_PATH)
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

    subprocess.call(['mene', 'path', '-d', DRAFT_PATH,
                        '-s', SEED_PATH,   '-t', TARGETS_PATH,
                        '--output', 'test.json'])

    results = json.loads(open('test.json', 'r').read())

    assert set(results['unproducible_targets_lst']) == unproducible_targets
    assert set(results['intersection_path']) == intersections
    assert set(results['union_path']) == unions
    os.remove('test.json')


def test_menedead():
    non_consumed_metabolites = ["M_H_c", "M_B_c"]
    non_produced_metabolites = ['M_A_c', 'M_E_c']

    results = run_menedead('menedead_test.sbml')

    assert sorted(results['non_consumed_metabolites']) == sorted(non_consumed_metabolites)
    assert sorted(results['non_produced_metabolites']) == sorted(non_produced_metabolites)


def test_menedead_cli():
    non_consumed_metabolites = ["M_H_c", "M_B_c"]
    non_produced_metabolites = ['M_A_c', 'M_E_c']

    subprocess.call(['mene', 'dead', '-d', 'menedead_test.sbml',
                      '--output', 'test.json'])

    results = json.loads(open('test.json', 'r').read())

    assert sorted(results['non_consumed_metabolites']) == sorted(non_consumed_metabolites)
    assert sorted(results['non_produced_metabolites']) == sorted(non_produced_metabolites)

    os.remove('test.json')


def test_menedead_toy():
    non_consumed_metabolites = ['M_j_c', 'M_l_c', 'M_i_c', 'M_f_c', 'M_biomass_c', 'M_g_c']
    non_produced_metabolites = ['M_T1_c', 'M_h_c', 'M_k_c', 'M_c_c']

    results = run_menedead(DRAFT_PATH)

    assert sorted(results['non_consumed_metabolites']) == sorted(non_consumed_metabolites)
    assert sorted(results['non_produced_metabolites']) == sorted(non_produced_metabolites)


def test_menedead_toy_cli():
    non_consumed_metabolites = ['M_j_c', 'M_l_c', 'M_i_c', 'M_f_c', 'M_biomass_c', 'M_g_c']
    non_produced_metabolites = ['M_T1_c', 'M_h_c', 'M_k_c', 'M_c_c']

    subprocess.call(['mene', 'dead', '-d', DRAFT_PATH,
                      '--output', 'test.json'])

    results = json.loads(open('test.json', 'r').read())

    assert sorted(results['non_consumed_metabolites']) == sorted(non_consumed_metabolites)
    assert sorted(results['non_produced_metabolites']) == sorted(non_produced_metabolites)

    os.remove('test.json')

def test_meneseed_toy():
    seeds = ["M_A_c", "M_D_c", "M_B_c", "M_C_c", "M_E_c", "M_F_c"]

    results = run_meneseed('meneseed_test.sbml')

    assert sorted(results['seeds']) == sorted(seeds)


def test_meneseed_toy_cli():
    seeds = ["M_A_c", "M_D_c", "M_B_c", "M_C_c", "M_E_c", "M_F_c"]

    subprocess.call(['mene', 'seed', '-d', 'meneseed_test.sbml',
                      '--output', 'test.json'])

    results = json.loads(open('test.json', 'r').read())

    assert sorted(results['seeds']) == sorted(seeds)

    os.remove('test.json')


def test_menescope_inc():
    print("*** test menescope_inc ***")
    scope_step = {"M_A_c": 0, "M_C_c": 0,
                "M_B_c": 1, "M_D_c": 1,
                "M_E_c": 2,
                "M_F_c": 3,
                "M_G_c": 4, "M_H_c": 4
                }
    step_production = { 0: ["M_A_c", "M_C_c"],
                        1: ["M_B_c", "M_D_c"],
                        2: ["M_E_c"],
                        3: ["M_F_c"],
                        4: ["M_H_c", "M_G_c"]
                        }
    results = run_menescope_inc(MENEINC_DRAFT_PATH, MENEINC_SEED_PATH, MENEINC_TARGETS_PATH)

    assert len(results['incremental_scope']) == len(scope_step)
    for metabolite in scope_step:
        assert scope_step[metabolite] == results['incremental_scope'][metabolite]
    for step in step_production:
        assert set(step_production[step]) == set(results['step_produced'][step])


def test_menescope_inc_without_targets():
    scope_step = {"M_A_c": 0, "M_C_c": 0,
                "M_B_c": 1, "M_D_c": 1,
                "M_E_c": 2,
                "M_F_c": 3,
                "M_G_c": 4, "M_H_c": 4
                }

    results = run_menescope_inc(MENEINC_DRAFT_PATH, MENEINC_SEED_PATH, None)

    assert results['incremental_scope'] == scope_step


def test_menescope_inc_unproducible_targets():
    print("*** test menescope_inc unproducible targets ***")

    # Check that mene scope_inc successfully exists when having unproducible targets.
    with pytest.raises(SystemExit) as pytest_wrapped_e:
        run_menescope_inc(MENEINC_DRAFT_PATH, MENEINC_UNCORRECT_SEED_PATH, MENEINC_TARGETS_PATH)
    assert pytest_wrapped_e.type == SystemExit


def test_menescope_inc_cli():
    print("*** test menescope_inc cli ***")
    scope_step = {"M_A_c": 0, "M_C_c": 0,
                "M_B_c": 1, "M_D_c": 1,
                "M_E_c": 2,
                "M_F_c": 3,
                "M_G_c": 4, "M_H_c": 4
                }
    step_production = { "0": ["M_A_c", "M_C_c"],
                        "1": ["M_B_c", "M_D_c"],
                        "2": ["M_E_c"],
                        "3": ["M_F_c"],
                        "4": ["M_H_c", "M_G_c"]
                        }

    subprocess.call(['mene', 'scope_inc', '-d', MENEINC_DRAFT_PATH,
                        '-s', MENEINC_SEED_PATH, '-t', MENEINC_TARGETS_PATH,
                        '--output', 'test.json'])

    results = json.loads(open('test.json', 'r').read())

    assert len(results['incremental_scope']) == len(scope_step)
    for metabolite in scope_step:
        assert scope_step[metabolite] == results['incremental_scope'][metabolite]
    for step in step_production:
        assert set(step_production[step]) == set(results['step_produced'][step])
    os.remove('test.json')


if __name__ == "__main__":
    test_menepath()
    test_menecheck()
    test_menecof()
    test_menescope()
    print('Done testing.')
