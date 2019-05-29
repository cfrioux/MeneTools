# MENETOOLS

MeneTools are Python3 tools to explore the topology of metabolic network to:
* assess whether targets are topologically producible (Menecheck)
* get all compounds that are topologically producible (Menescope)
* get production paths of specific compounds (Menepath)
* obtain compounds that if added to the seeds, would ensure the topological producibility of targets (Menecof)

Requires **Python >= 3.6**

Required package (starting from version 2.0 of the package):
* [``Clyngor``](https://github.com/Aluriak/clyngor) or [``Clyngor_with_clingo``](https://github.com/Aluriak/clyngor-with-clingo) that includes the solvers

## Install

```
python setup.py install
```

## MENECHECK

Menecheck is a python3 tool to get the topologically producibility status of target compounds

### usage

```
menecheck [-h] -d DRAFTNET -s SEEDS -t TARGETS

optional arguments:
  -h, --help            show this help message and exit
  -d DRAFTNET, --draftnet DRAFTNET
                        metabolic network in SBML format
  -s SEEDS, --seeds SEEDS
                        seeds in SBML format
  -t TARGETS, --targets TARGETS
                        targets in SBML format
```


```python
from menetools import run_menecheck

model = run_menecheck(draft_sbml='required',seeds_sbml='required',targets_sbml='required')
```

## MENESCOPE

Menescope is a python3 tool to get the topologically reachable compounds from
seeds in a metabolic network.

### usage

```
menescope [-h] -d DRAFTNET -s SEEDS

optional arguments:
  -h, --help            show this help message and exit
  -d DRAFTNET, --draftnet DRAFTNET
                        metabolic network in SBML format
  -s SEEDS, --seeds SEEDS
                        seeds in SBML format
```

```python
from menetools import run_menescope

model = run_menescope(draft_sbml='required',seeds_sbml='required')
```

## MENEPATH

Menepath is a python3 tool to get the topologically essential reactions with
respects to individual targets in metabolic networks.

### usage

```
menepath [-h] -d DRAFTNET -s SEEDS -t TARGETS

optional arguments:
  -h, --help            show this help message and exit
  -d DRAFTNET, --draftnet DRAFTNET
                        metabolic network in SBML format
  -s SEEDS, --seeds SEEDS
                        seeds in SBML format
  -t TARGETS, --targets TARGETS
                        targets in SBML format
```

```python
from menetools import run_menescope

model = run_menepath(draft_sbml='required',seeds_sbml='required',targets_sbml='required',min_size='optional',enumeration='optional')
```

### MENECOF

Menecof is a python3 tool to get the minimal set of cofactors that enables to
maximize the number f producible targets. Study of the metabolic network is made`
topologically using reachable compounds from seeds.

### usage

```
menecof [-h] -d DRAFTNET -s SEEDS -t TARGETS [-c COFACTORS]
                  [--suffix SUFFIX] [--weight] [--enumerate]

the following arguments are required: -d/--draftnet, -s/--seeds, -t/--targets

optional arguments: --suffix --weight --enumerate -h/--help

  -h, --help            show this help message and exit

  -d DRAFTNET, --draftnet DRAFTNET
                        metabolic network in SBML format

  -s SEEDS, --seeds SEEDS
                        seeds in SBML format

  -t TARGETS, --targets TARGETS
                        targets in SBML format

  -c COFACTORS, --cofactors COFACTORS
                        cofactors, in one-per-line text file format

  --suffix SUFFIX       suffix to be added to the compounds of the database.
                        It can be the suffix for the cytosolic compartment or
                        external one. Cytosolic one is prefered to ensure the
                        impact of the added cofactors. Default = None

  --weight              call this option if cofactors are weighted according
                        to their occurrence frequency in database. If so,
                        cofactors file must be tabulated with per line
                        compound' 'occurrence

  --enumerate           enumerates all cofactors solutions
```

```python
from menetools import run_menecof

model = run_menecof(draft_sbml='required',seeds_sbml='required',targets_sbml='required',cofactors_txt='optional',weights='optional',suffix='optional',enumeration='optional')
```

## Acknowledgements

Thanks [@Aluriak](https://github.com/Aluriak) for his awesome work with [Clyngor](https://github.com/Aluriak/clyngor).