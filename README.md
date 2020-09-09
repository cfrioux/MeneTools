[![PyPI version](https://img.shields.io/pypi/v/menetools.svg)](https://pypi.org/project/MeneTools/) [![GitHub license](https://img.shields.io/github/license/cfrioux/menetools.svg)](https://github.com/MeneTools/MeneTools/blob/master/LICENSE) [![Actions Status](https://github.com/cfrioux/MeneTools/workflows/Python%20package/badge.svg)](https://github.com/cfrioux/MeneTools/actions) [![](https://img.shields.io/badge/doi-10.1371/journal.pcbi.1006146-blueviolet.svg)](https://doi.org/10.1371/journal.pcbi.1006146)

# MeneTools

MeneTools are Python (3.6 and higher) tools to explore the producibility potential in a metabolic network using the network expansion algorithm. The MeneTools can:
* assess whether targets are producible starting from nutrients (Menecheck)
* get all compounds that are producible starting from nutrients (Menescope)
* get all reactions that are activable from nutrients (Meneacti)
* get production paths of specific compounds (Menepath)
* obtain compounds that if added to the nutrients, would ensure the producibility of targets (Menecof)

MeneTools follows the producibility in metabolic networks as defined by the [network expansion](http://www.ncbi.nlm.nih.gov/pubmed/15712108) algorithm.
Mainly, two rules are followed:
* a *recursive rule*: the products of a reactions are producible if **all** reactants of this reaction are themselves producible
* an *initiation rule*: producibility is initiated by the presence of nutrients, called *seeds*. 

A metabolite that is producible from a set of nutrients is described as being "in the scope of the seeds".
The computation is made using logic solvers (Answer Set Programming). The present modelling ignores the stoichiometry of reactions (2A + B --> C is considered equivalent to A + B --> C), and is therefore suited to non-curated or draft metabolic networks.

**Menescope** computes the set of metabolites that are producible from a set of nutrients: its provides the scope of the seeds in a metabolic network. **Menecheck** assesses whether a list of target metabolites are producible from the nutrients in a metabolic model, following the network expansion algorithm. **Meneacti** has a similar functioning than Menetools but focuses on activable reactions. It computes all reactions that can be activated from the nutritional environment (i.e. whose sets of reactants are in the scope). **Menepath** (*beta* version) proposes a pathway (set of reactions) that explains the producibility of a given target metabolite from the seeds. The objective if to find a path of reactions for metabolites of interest. Lastly, **Menecof** (*beta* version) proposes compounds that would unblock the producibility of taregt metabolites if they were producible. It can therefore identify missing cofactor for the modelling or compounds that would need to be added to the growth medium of the modelled organism.

If you use MeneTools, please cite: 

Aite* M, Chevallier* M, Frioux* C, Trottier* C, Got J, Cortés MP, et al. Traceability, reproducibility and wiki-exploration for “à-la-carte” reconstructions of genome-scale metabolic models. PLoS Comput Biol 2018;14:e1006146. [https://doi.org/10.1371/journal.pcbi.1006146](https://doi.org/10.1371/journal.pcbi.1006146).

## Install

Requires **Python >= 3.6**

Required package (starting from version 2.0 of the package):
* [``Clyngor``](https://github.com/Aluriak/clyngor) or [``Clyngor_with_clingo``](https://github.com/Aluriak/clyngor-with-clingo) that includes the solvers

```
python setup.py install
```

or 

```
pip install menetools
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

## MENEACTI

Meneacti is a python3 tool that retrieve the activable reactions from
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
from menetools import run_menepath

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

Many thanks to [@Aluriak](https://github.com/Aluriak) for his awesome work with [Clyngor](https://github.com/Aluriak/clyngor).
