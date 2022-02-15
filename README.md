[![PyPI version](https://img.shields.io/pypi/v/menetools.svg)](https://pypi.org/project/MeneTools/) [![GitHub license](https://img.shields.io/github/license/cfrioux/menetools.svg)](https://github.com/cfrioux/MeneTools/blob/master/LICENSE.txt) [![Actions Status](https://github.com/cfrioux/MeneTools/workflows/Python%20package/badge.svg)](https://github.com/cfrioux/MeneTools/actions) [![](https://img.shields.io/badge/doi-10.1371/journal.pcbi.1006146-blueviolet.svg)](https://doi.org/10.1371/journal.pcbi.1006146) [![](https://img.shields.io/badge/doi-10.7554/eLife.61968-blueviolet.svg)](https://doi.org/10.7554/eLife.61968)

# MeneTools

MeneTools are Python (3.6 and higher) tools to explore the producibility potential in a metabolic network using the network expansion algorithm. The MeneTools can:
* assess whether targets are producible starting from nutrients (`Mene check`)
* get all compounds that are producible starting from nutrients (`Mene scope`)
* get all reactions that are activable from nutrients (`Mene acti`)
* get production paths of specific compounds (`Mene path`)
* obtain compounds that if added to the nutrients, would ensure the producibility of targets (`Mene cof`)
* identify metabolic deadends, _i.e._ metabolites that act as reactants of reactions but never as products, or metabolites that act as products of reactions but never as reactants. This is a purely structural analysis (`Mene dead`)
* identify exchanged compounds in metabolic networks based on exchange reactions, _i.e._ outputs of reactions that do not have reactants (`Mene seed`).

MeneTools follows the producibility in metabolic networks as defined by the [network expansion](http://www.ncbi.nlm.nih.gov/pubmed/15712108) algorithm.
Mainly, two rules are followed:
* a *recursive rule*: the products of a reactions are producible if **all** reactants of this reaction are themselves producible
* an *initiation rule*: producibility is initiated by the presence of nutrients, called *seeds*. 

A metabolite that is producible from a set of nutrients is described as being "in the scope of the seeds".
The computation is made using logic solvers (Answer Set Programming). The present modelling ignores the stoichiometry of reactions (2A + B --> C is considered equivalent to A + B --> C), and is therefore suited to non-curated or draft metabolic networks.

**Menescope** computes the set of metabolites that are producible from a set of nutrients: its provides the scope of the seeds in a metabolic network. **Menecheck** assesses whether a list of target metabolites are producible from the nutrients in a metabolic model, following the network expansion algorithm. **Meneacti** has a similar functioning than Menetools but focuses on activable reactions. It computes all reactions that can be activated from the nutritional environment (i.e. whose sets of reactants are in the scope). **Menepath** (*beta* version) proposes a pathway (set of reactions) that explains the producibility of a given target metabolite from the seeds. The objective if to find a path of reactions for metabolites of interest. **Menecof** (*beta* version) proposes compounds that would unblock the producibility of taregt metabolites if they were producible. It can therefore identify missing cofactor for the modelling or compounds that would need to be added to the growth medium of the modelled organism. **Menedead** (*beta* version) identifies deadends in a metabolic network. Deadends are compounds which are not produced or consumed (meaning that they are not reactant or product of a reaction).

**If you use MeneTools, please cite:**

Belcour* A, Frioux* C, Aite M, Bretaudeau A, Hildebrand F, Siegel A. Metage2Metabo, microbiota-scale metabolic complementarity for the identification of key species. eLife 2020;9:e61968 [https://doi.org/10.7554/eLife.61968](https://doi.org/10.7554/eLife.61968).

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

## Usage

```
usage: mene [-h] [-v] {acti,check,cof,dead,path,scope,seed} ...

Explore the producibility potential in a metabolic network using the network
expansion algorithm. For specific help on each subcommand use: mene {cmd}
--help

optional arguments:
  -h, --help            show this help message and exit
  -v, --version         show program's version number and exit

subcommands:
  valid subcommands:

  {acti,check,cof,dead,path,scope,seed}
    acti                Get activable reactions in a metabolic network,
                        starting from seeds.
    check               Check the producibility of targets from seeds in a
                        metabolic network.
    cof                 Propose cofactor whose producibility could unblock the
                        producibility of targets.
    dead                Identification of dead-end reactions (reactions whose
                        reactants are never consumed or whose reactants are
                        never produced) in metabolic networks.
    path                Get production pathways of targets in metabolic
                        networks, started from seeds.
    scope               Get producible metabolites in a metabolic network,
                        starting from seeds.
    seed                Get metabolites from exchange reactions in a metabolic network.

Requires Clingo and clyngor package: "pip install clyngor clyngor-with-clingo"

```

### MENECHECK

Menecheck is a python3 tool to get the topologically producibility status of target compounds

```
usage: mene check [-h] -d DRAFTNET -s SEEDS [-t TARGETS] [--output OUTPUT]

optional arguments:
  -h, --help            show this help message and exit
  -d DRAFTNET, --draftnet DRAFTNET
                        metabolic network in SBML format
  -s SEEDS, --seeds SEEDS
                        seeds in SBML format
  -t TARGETS, --targets TARGETS
                        targets in SBML format
  --output OUTPUT       output file for instance
```


```python
from menetools import run_menecheck

model = run_menecheck(draft_sbml='required',seeds_sbml='required',targets_sbml='required',output='optional')
```

### MENESCOPE

Menescope is a python3 tool to get the topologically reachable compounds from
seeds in a metabolic network.

```
usage: mene scope [-h] -d DRAFTNET -s SEEDS [--output OUTPUT]

optional arguments:
  -h, --help            show this help message and exit
  -d DRAFTNET, --draftnet DRAFTNET
                        metabolic network in SBML format
  -s SEEDS, --seeds SEEDS
                        seeds in SBML format
  --output OUTPUT       output file for instance
```

```python
from menetools import run_menescope

model = run_menescope(draft_sbml='required',seeds_sbml='required',output='optional')
```

### MENEACTI

Meneacti is a python3 tool that retrieve the activable reactions from
seeds in a metabolic network.

```
usage: mene acti [-h] -d DRAFTNET -s SEEDS [--output OUTPUT]

optional arguments:
  -h, --help            show this help message and exit
  -d DRAFTNET, --draftnet DRAFTNET
                        metabolic network in SBML format
  -s SEEDS, --seeds SEEDS
                        seeds in SBML format
  --output OUTPUT       output file for instance
```

```python
from menetools import run_menescope

model = run_mene_acti(draft_sbml='required',seeds_sbml='required',output='optional')
```

### MENEPATH

Menepath is a python3 tool to get the topologically essential reactions with
respects to individual targets in metabolic networks.

```
usage: mene path [-h] -d DRAFTNET -s SEEDS [-t TARGETS] [--enumerate] [--min]
                 [--output OUTPUT]

optional arguments:
  -h, --help            show this help message and exit
  -d DRAFTNET, --draftnet DRAFTNET
                        metabolic network in SBML format
  -s SEEDS, --seeds SEEDS
                        seeds in SBML format
  -t TARGETS, --targets TARGETS
                        targets in SBML format
  --enumerate           enumerates all cofactors solutions
  --min                 call this option to obtain minimal-size paths
  --output OUTPUT       output file for instance
```

```python
from menetools import run_menepath

model = run_menepath(draft_sbml='required',seeds_sbml='required',targets_sbml='required',min_size='optional',enumeration='optional',output='optional')
```

### MENECOF

Menecof is a python3 tool to get the minimal set of cofactors that enables to
maximize the number f producible targets. Study of the metabolic network is made
topologically using reachable compounds from seeds.

```
usage: mene cof [-h] -d DRAFTNET -s SEEDS [-t TARGETS] [-c COFACTORS]
                [--weight] [--suffix SUFFIX] [--enumerate] [--output OUTPUT]

optional arguments:
  -h, --help            show this help message and exit
  -d DRAFTNET, --draftnet DRAFTNET
                        metabolic network in SBML format
  -s SEEDS, --seeds SEEDS
                        seeds in SBML format
  -t TARGETS, --targets TARGETS
                        targets in SBML format
  -c COFACTORS, --cofactors COFACTORS
                        cofactors, in one-per-line text file format
  --weight              call this option if cofactors are weighted according
                        to their occurrence frequency in database. If so,
                        cofactors file must be tabulated with per line
                        compound' 'occurrence
  --suffix SUFFIX       suffix to be added to the compounds of the database.
                        It can be the suffix for the cytosolic compartment or
                        external one. Cytosolic one is prefered to ensure the
                        impact of the added cofactors. Default = None
  --enumerate           enumerates all cofactors solutions
  --output OUTPUT       output file for instance
```

```python
from menetools import run_menecof

model = run_menecof(draft_sbml='required',seeds_sbml='required',targets_sbml='required',cofactors_txt='optional',weights='optional',suffix='optional',enumeration='optional',output='optional')
```

### MENEDEAD

Menedead is a python3 tool to identify dead ends in a metabolic network, by
searching non produced and non consumed metabolites.

```
usage: mene dead [-h] -d DRAFTNET [--output OUTPUT]

optional arguments:
  -h, --help            show this help message and exit
  -d DRAFTNET, --draftnet DRAFTNET
                        metabolic network in SBML format
  --output OUTPUT       json output file
```

```python
from menetools import run_menedead

model = run_menedead(draft_sbml='required',output='optional')
```

### MENESEED

Meneseed identifies metabolites produced by exchange reactions in a metabolic network.
It does not consider the flux value of these exchange reactions, it solely considers the
structure of the network. 

e.g. Given the reactions ` <-> A`, ` -> B`, ` <- C`, A and B would be reported by Meneseed.

```
usage: mene seed [-h] -d DRAFTNET [--output OUTPUT]

optional arguments:
  -h, --help            show this help message and exit
  -d DRAFTNET, --draftnet DRAFTNET
                        metabolic network in SBML format
  --output OUTPUT       json output file
```

```python
from menetools import run_meneseed

model = run_meneseed(draft_sbml='required',output='optional')
```
## Acknowledgements

Many thanks to
* [@Aluriak](https://github.com/Aluriak) for his awesome work with [Clyngor](https://github.com/Aluriak/clyngor).
* [@mablt](https://github.com/mablt) for his contribution to MeneSeed.

