#! /usr/bin/env python
# -*- coding: utf-8 -*-
"""Description.

Tests du module algos.py
"""

from pytest import raises
from pydantic import ValidationError
from exemple_supply_chain import CahierDesCharges, Tache, Intervalle, produit_planning
from exemple_supply_chain.algos import valide_tri_topologique, tri_topologique


def test_tri_topologique_vide():
    """
    Teste le cas où le cahier des charges est vide.
    La fonction doit renvoyer une liste vide.
    """
    cahier = CahierDesCharges(taches=frozenset())
    assert tri_topologique(cahier) == []


def test_tri_topologique_simple():
    """
    Teste le cas où le cahier des charges contient une séquence simple de tâches sans prérequis multiples.
    La fonction doit renvoyer une liste de tâches triées topologiquement.
    """
    tache_a = Tache(nom="A", prerequis=frozenset(), duree=1)
    tache_b = Tache(nom="B", prerequis=frozenset("A"), duree=2)
    tache_c = Tache(nom="C", prerequis=frozenset("B"), duree=3)
    cahier = CahierDesCharges(taches=frozenset([tache_a, tache_b, tache_c]))
    assert valide_tri_topologique(tri_topologique(cahier), cahier)


def test_tri_topologique_multiple_precedences():
    """
    Teste le cas où le cahier des charges contient une séquence de tâches avec des prérequis multiples.
    La fonction doit renvoyer une liste de tâches triées topologiquement.
    """
    tache_a = Tache(nom="A", prerequis=frozenset(), duree=1)
    tache_b = Tache(nom="B", prerequis=frozenset("A"), duree=2)
    tache_c = Tache(nom="C", prerequis=frozenset("A"), duree=3)
    tache_d = Tache(nom="D", prerequis=frozenset(("B", "C")), duree=4)
    cahier = CahierDesCharges(taches=frozenset([tache_a, tache_b, tache_c, tache_d]))
    assert valide_tri_topologique(tri_topologique(cahier), cahier)


def test_tri_topologique_cycle():
    """
    Teste le cas où le cahier des charges contient un cycle de dépendances entre les tâches.
    La fonction doit lever une exception ValueError.
    """
    tache_a = Tache(nom="A", prerequis=frozenset("B"), duree=1)
    tache_b = Tache(nom="B", prerequis=frozenset("C"), duree=2)
    tache_c = Tache(nom="C", prerequis=frozenset("A"), duree=3)
    cahier = CahierDesCharges(taches=frozenset([tache_a, tache_b, tache_c]))
    with raises(ValueError):
        tri_topologique(cahier)


def test_tri_topologique_tache_inexistante():
    """
    Teste le cas où le cahier des charges contient une tâche avec un prérequis qui n'existe pas.
    La fonction doit lever une exception ValidationError.
    """
    tache_a = Tache(nom="A", prerequis=frozenset(), duree=1)
    tache_b = Tache(nom="B", prerequis=frozenset("C"), duree=2)
    with raises(ValidationError):
        cahier = CahierDesCharges(taches=frozenset([tache_a, tache_b]))
        tri_topologique(cahier)


def test_produit_planning_vide():
    """
    Teste le cas où le cahier des charges est vide.
    La fonction doit renvoyer un dictionnaire vide.
    """
    cahier = CahierDesCharges(taches=frozenset())
    resultat = produit_planning(cahier)
    assert resultat == {}


def test_produit_planning_simple():
    """
    Teste le cas où le cahier des charges contient une seule chaîne de dépendances.
    La fonction doit renvoyer le planning attendu.
    """
    tache_a = Tache(nom="A", prerequis=frozenset(), duree=2.0)
    tache_b = Tache(nom="B", prerequis=frozenset([tache_a.nom]), duree=3.0)
    cahier = CahierDesCharges(taches=frozenset([tache_a, tache_b]))
    resultat = produit_planning(cahier)
    attendu = {
        tache_a: Intervalle(debut=0.0, fin=2.0),
        tache_b: Intervalle(debut=2.0, fin=5.0),
    }
    assert resultat == attendu


def test_produit_planning_multiple_precedences():
    """
    Teste le cas où le cahier des charges contient plusieurs chaînes de dépendances convergeant vers une seule tâche.
    La fonction doit renvoyer le planning attendu.
    """
    tache_a = Tache(nom="A", prerequis=frozenset(), duree=2.0)
    tache_b = Tache(nom="B", prerequis=frozenset([tache_a.nom]), duree=3.0)
    tache_c = Tache(nom="C", prerequis=frozenset([tache_a.nom]), duree=4.0)
    tache_d = Tache(nom="D", prerequis=frozenset([tache_b.nom, tache_c.nom]), duree=5.0)
    cahier = CahierDesCharges(taches=frozenset([tache_a, tache_b, tache_c, tache_d]))
    resultat = produit_planning(cahier)
    attendu = {
        tache_a: Intervalle(debut=0.0, fin=2.0),
        tache_b: Intervalle(debut=2.0, fin=5.0),
        tache_c: Intervalle(debut=2.0, fin=6.0),
        tache_d: Intervalle(debut=6.0, fin=11.0),
    }
    assert resultat == attendu
