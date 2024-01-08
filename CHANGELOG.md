# Changelog

# MeneTools v3.4.0 (2024-01-08)

## Add

* `Mene scope_inc` identifies the number of steps needed either to produce targets or all producible compounds (computed with menescope) starting from nutrients

## Modify

* Filter the presence of seeds in the scope by removing seeds absent from the network (issue #15)
* Modify if statement that will be deprecated in the future.
* Update license year

# MeneTools v3.3.0 (2023-01-05)

## Add

* `Mene scope_inc` identifies the number of steps needed either to produce targets or all producible compounds (computed with menescope) starting from nutrients
* tests and doc for `Mene scope_inc` 
* CHANGELOG.md file

## Modify

* Remove uneeded imports
* Update license year

# MeneTools v3.2.1 (2022-03-18)

## Fix

- Latest clyngor versions led to errors that can be preventing by not using the clingo module when calling solver #12 

## Test

- Tests are no longer done for Python 3.6 but for versions 3.7, 3.8, 3.9

## Doc

- A small typo is fixed

## Others

- `.gitignore` has been updated

# MeneTools v3.2.0 (2021-08-21)

## Add

* `Mene seed` identifies compounds that would be considered as seeds in network expansion because they are produced by exchange reactions

## Doc

* Update with Meneseed

## Tests

* New tests for Meneseed

## Others

* The MeneTools project is now mirrored on [Gitlab Inria](https://gitlab.inria.fr/pleiade/menetools) via GH CI.

# MeneTools v3.1.1 (2021-02-22)

## Licence

MeneTools is now under the LGPL licence.

## Doc

Update documentation with the latest citation for MeneTools.

# MeneTools v3.1.0 (2020-12-01)

## Add

* `mene scope` now returns (in the json output and API call) a dictionnary with 2 keys: 
    * the usual list of compounds in the scope
    * the list of seeds that are also predicted to be produced by the organism

## Tests

* new tests for the latest version of `mene scope`

# MeneTools v3.0.2 (2020-11-18)

## Add

* Menedead: to identify deadends in metabolic network.
* Windows and MacOS tests in GitHub Actions.
* Windows compatibility.

# MeneTools v3.0.1 (2020-10-30)

## Add

* Error message if SBML files have no reactions.

# MeneTools v3.0.0 (2020-10-26)

## Add

* Merge all commands into one command with subcommands: e.g. `menescope` becomes `mene scope` 
* Version can now be retrieved with `mene --version`

## Fix

* Typos

# MeneTools v2.1.0 (2020-09-09)

## Add

* Meneacti to retrieve activable reactions from nutrients
* Documentation for Meneacti

## Fix

* typos
* output format of Menecheck in console
* 
# MeneTools v2.0.6 (2020-05-21)

* Use of Clyngor for ASP computations
* Improved documentation
* Calls directly from python scripts are possible
* Use of loggers
* Beta developments of Menepath and Menecof 
