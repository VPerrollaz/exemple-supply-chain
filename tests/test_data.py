#! /usr/bin/env python
# -*- coding: utf-8 -*-
"""Description.

Tests du module data.py
"""

import pytest
from exemple_supply_chain.data import Tache, CahierDesCharges


def test_creation_tache():
    """
    Teste la création d'une tâche avec des prérequis vides.
    """
    tache = Tache(nom="tache1", duree=10, prerequis=frozenset())
    assert tache.nom == "tache1"
    assert tache.duree == 10
    assert tache.prerequis == frozenset()


def test_duree_negative():
    """
    Teste la validation de la durée d'une tâche.
    """
    with pytest.raises(ValueError):
        Tache(nom="tache1", duree=-1, prerequis=frozenset())


def test_prerequis_cyclique():
    """
    Teste la détection de prérequis cycliques.
    """
    with pytest.raises(ValueError):
        Tache(nom="tache3", duree=30, prerequis=frozenset({"tache3"}))


def test_hash():
    """
    Teste le hachage des instances de Tache.
    """
    tache1 = Tache(nom="tache1", duree=10, prerequis=frozenset())
    tache2 = Tache(nom="tache2", duree=20, prerequis=frozenset({"tache1"}))
    tache3 = Tache(nom="tache3", duree=30, prerequis=frozenset({"tache1", "tache2"}))
    assert hash(tache1) != hash(tache2)
    assert hash(tache1) != hash(tache3)
    assert hash(tache2) != hash(tache3)


def test_egalite():
    """
    Teste l'égalité des instances de Tache.
    """
    tache1 = Tache(nom="tache1", duree=10, prerequis=frozenset())
    tache2 = Tache(nom="tache2", duree=20, prerequis=frozenset({"tache1"}))
    tache3 = Tache(nom="tache3", duree=30, prerequis=frozenset({"tache1", "tache2"}))
    tache4 = Tache(nom="tache3", duree=30, prerequis=frozenset({"tache1", "tache2"}))
    assert tache1 != tache2
    assert tache3 == tache4
