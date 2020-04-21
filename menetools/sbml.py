#!/usr/bin/python
# -*- coding: utf-8 -*-
import re
import sys
from  clyngor import as_pyasp
from  clyngor.as_pyasp import TermSet, Atom
import xml.etree.ElementTree as etree
from xml.etree.ElementTree import XML, fromstring, tostring
import logging

logger = logging.getLogger('menetools.sbml')

def get_model(sbml):
    """
    return the model of a SBML
    """
    model_element = None
    for e in sbml:
        if e.tag[0] == "{":
            uri, tag = e.tag[1:].split("}")
        else:
            tag = e.tag
        if tag == "model":
            model_element = e
            break
    return model_element

def get_listOfSpecies(model):
    """
    return list of species of a SBML model
    """
    listOfSpecies = None
    for e in model:
        if e.tag[0] == "{":
            uri, tag = e.tag[1:].split("}")
        else:
            tag = e.tag
        if tag == "listOfSpecies":
            listOfSpecies = e
            break
    return listOfSpecies

def get_listOfReactions(model):
    """
    return list of reactions of a SBML model
    """
    listOfReactions = None
    for e in model:
        if e.tag[0] == "{":
            uri, tag = e.tag[1:].split("}")
        else:
            tag = e.tag
        if tag == "listOfReactions":
            listOfReactions = e
            break
    return listOfReactions

def get_listOfReactants(reaction):
    """
    return list of reactants of a reaction
    """
    listOfReactants = None
    for e in reaction:
        if e.tag[0] == "{":
            uri, tag = e.tag[1:].split("}")
        else:
            tag = e.tag
        if tag == "listOfReactants":
            listOfReactants = e
            break
    return listOfReactants

def get_listOfProducts(reaction):
    """
    return list of products of a reaction
    """
    listOfProducts = None
    for e in reaction:
        if e.tag[0] == "{":
            uri, tag = e.tag[1:].split("}")
        else:
            tag = e.tag
        if tag == "listOfProducts":
            listOfProducts = e
            break
    return listOfProducts

def readSBMLnetwork(filename, name) :
    """
    Read a SBML network and turn it into ASP-friendly data
    """
    lpfacts = TermSet()

    tree = etree.parse(filename)
    sbml = tree.getroot()
    model = get_model(sbml)

    listOfReactions = get_listOfReactions(model)
    for e in listOfReactions:
        if e.tag[0] == "{":
            uri, tag = e.tag[1:].split("}")
        else:
            tag = e.tag
        if tag == "reaction":
            reactionId = e.attrib.get("id")
            lpfacts.add(Term('dreaction', ["\""+reactionId+"\""])) #, "\""+name+"\""
            if(e.attrib.get("reversible")=="true"):
                lpfacts.add(Term('reversible', ["\""+reactionId+"\""]))

            listOfReactants = get_listOfReactants(e)
            if listOfReactants == None :
                logger.warning("\n Warning: "+ reactionId + " listOfReactants=None")
            else:
                for r in listOfReactants:
                    lpfacts.add(Term('reactant', ["\""+r.attrib.get("species")+"\"", "\""+reactionId+"\""])) #,"\""+name+"\""

            listOfProducts = get_listOfProducts(e)
            if listOfProducts == None:
                logger.warning("\n Warning: "+reactionId + " listOfProducts=None")
            else:
                for p in listOfProducts:
                    lpfacts.add(Term('product', ["\""+p.attrib.get("species")+"\"", "\""+reactionId+"\""])) #,"\""+name+"\""
    #print(lpfacts)
    return lpfacts

def readSBMLnetwork_clyngor(filename, name) :
    """
    Read a SBML network and turn it into ASP-friendly data
    """
    all_atoms = set()
    tree = etree.parse(filename)
    sbml = tree.getroot()
    model = get_model(sbml)

    listOfReactions = get_listOfReactions(model)
    for e in listOfReactions:
        if e.tag[0] == "{":
            uri, tag = e.tag[1:].split("}")
        else:
            tag = e.tag
        if tag == "reaction":
            reactionId = e.attrib.get("id")
            all_atoms.add(Atom('dreaction', ["\""+reactionId+"\""])) #, "\""+name+"\""
            if(e.attrib.get("reversible")=="true"):
                all_atoms.add(Atom('reversible', ["\""+reactionId+"\""]))

            listOfReactants = get_listOfReactants(e)
            if listOfReactants == None :
                logger.warning("\n Warning: " + reactionId + " listOfReactants=None")
            else:
                for r in listOfReactants:
                    all_atoms.add(Atom('reactant', ["\""+r.attrib.get("species")+"\"", "\""+reactionId+"\""])) #,"\""+name+"\""

            listOfProducts = get_listOfProducts(e)
            if listOfProducts == None:
                logger.warning("\n Warning: "+reactionId+ " listOfProducts=None")
            else:
                for p in listOfProducts:
                    all_atoms.add(Atom('product', ["\""+p.attrib.get("species")+"\"", "\""+reactionId+"\""])) #,"\""+name+"\""
    #print(lpfacts)
    lpfacts = TermSet(all_atoms)
    return lpfacts


def make_weighted_list_of_species(network):
    """
    Read a SBML network and return its list of species with weights
    corresponding to their number of occurrences in reactions
    """
    tree = etree.parse(network)
    sbml = tree.getroot()
    model = get_model(sbml)

    listOfSpecies = get_listOfSpecies(model)

    species = {}

    for e in listOfSpecies:
        if e.tag[0] == "{":
            uri, tag = e.tag[1:].split("}")
        else: tag = e.tag
        if tag == "species":
            species_id = e.attrib.get("id")
            species[species_id] = {0}

    with open(network,'r') as f:
        contents = f.read()
        for compound in species:
            pattern = 'speciesReference species="{}"'.format(compound)
            #print(pattern)
            species[compound] = contents.count(pattern)
            #print(compound, str(species[compound]))
    return(species)


# read the seeds

def readSBMLspecies(filename, speciestype) :
    """
    Read a SBML network return its species as seeds or targets
    """
    lpfacts = TermSet()

    tree = etree.parse(filename)
    sbml = tree.getroot()
    model = get_model(sbml)

    listOfSpecies = get_listOfSpecies(model)
    for e in listOfSpecies:
        if e.tag[0] == "{":
            uri, tag = e.tag[1:].split("}")
        else:
            tag = e.tag
        if tag == "species":
            lpfacts.add(Term(speciestype, ["\""+e.attrib.get("id")+"\""]))
    return lpfacts

def readSBMLspecies_clyngor(filename, speciestype) :
    """
    Read a SBML network return its species as seeds or targets
    """
    all_atoms = set()

    tree = etree.parse(filename)
    sbml = tree.getroot()
    model = get_model(sbml)

    listOfSpecies = get_listOfSpecies(model)
    if listOfSpecies:
        for e in listOfSpecies:
            if e.tag[0] == "{":
                uri, tag = e.tag[1:].split("}")
            else:
                tag = e.tag
            if tag == "species":
                all_atoms.add(Atom(speciestype, ["\""+e.attrib.get("id")+"\""]))
    else:
        sys.exit("Invalid SBML (missing species or listOfSpecies) " + filename)

    lpfacts = TermSet(all_atoms)

    return lpfacts
