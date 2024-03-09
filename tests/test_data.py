#! /usr/bin/env python
# -*- coding: utf-8 -*-
"""Description.

Tests du module data.py
"""

import pytest
from exemple_supply_chain.data import Tache, CahierDesCharges, Intervalle
from pydantic import ValidationError


def test_creation_tache():
    """Teste la création d'une tâche avec des prérequis vides."""
    tache = Tache(nom="tache1", duree=10, prerequis=frozenset())
    assert tache.nom == "tache1"
    assert tache.duree == 10
    assert tache.prerequis == frozenset()


def test_duree_negative():
    """
    Teste la validation de la durée d'une tâche.
    """
    with pytest.raises(ValidationError):
        Tache(nom="tache1", duree=-1, prerequis=frozenset())


def test_prerequis_cyclique():
    """Teste la détection de prérequis cycliques."""
    with pytest.raises(ValidationError):
        Tache(nom="tache3", duree=30, prerequis=frozenset({"tache3"}))


def test_hash():
    """Teste le hachage des instances de Tache."""
    tache1 = Tache(nom="tache1", duree=10, prerequis=frozenset())
    tache2 = Tache(nom="tache2", duree=20, prerequis=frozenset({"tache1"}))
    tache3 = Tache(nom="tache3", duree=30, prerequis=frozenset({"tache1", "tache2"}))
    tache4 = Tache(nom="tache3", duree=30, prerequis=frozenset({"tache1", "tache2"}))
    assert hash(tache1) != hash(tache2)
    assert hash(tache1) != hash(tache3)
    assert hash(tache2) != hash(tache3)
    assert hash(tache3) == hash(tache4)


def test_egalite():
    """Teste l'égalité des instances de Tache."""
    tache1 = Tache(nom="tache1", duree=10, prerequis=frozenset())
    tache2 = Tache(nom="tache2", duree=20, prerequis=frozenset({"tache1"}))
    tache3 = Tache(nom="tache3", duree=30, prerequis=frozenset({"tache1", "tache2"}))
    tache4 = Tache(nom="tache3", duree=30, prerequis=frozenset({"tache1", "tache2"}))
    assert tache1 != tache2
    assert tache3 == tache4


def test_cahier_des_charges_valide():
    """Teste que le cahier des charges est valide."""
    tache1 = Tache(nom="tâche 1", duree=10, prerequis=frozenset())
    tache2 = Tache(nom="tâche 2", duree=20, prerequis=frozenset({"tâche 1"}))
    tache3 = Tache(nom="tâche 3", duree=30, prerequis=frozenset({"tâche 2"}))

    cahier_des_charges = CahierDesCharges(taches=frozenset({tache1, tache2, tache3}))

    assert len(cahier_des_charges.taches) == 3
    assert tache1 in cahier_des_charges.taches
    assert tache2 in cahier_des_charges.taches
    assert tache3 in cahier_des_charges.taches


def test_cahier_des_charges_invalide():
    """Teste que le cahier des charges est invalide si une tâche a un prérequis qui n'existe pas."""
    tache1 = Tache(nom="tâche 1", duree=10, prerequis=frozenset())
    tache2 = Tache(nom="tâche 2", duree=20, prerequis=frozenset({"tâche 1"}))
    tache3 = Tache(nom="tâche 3", duree=30, prerequis=frozenset({"tâche 4"}))

    with pytest.raises(ValidationError):
        CahierDesCharges(taches=frozenset({tache1, tache2, tache3}))


def test_cahier_des_charges_immuable():
    """Teste que le cahier des charges est immuable."""
    tache1 = Tache(nom="tâche 1", duree=10, prerequis=frozenset())
    tache2 = Tache(nom="tâche 2", duree=20, prerequis=frozenset({"tâche 1"}))
    tache3 = Tache(nom="tâche 3", duree=30, prerequis=frozenset({"tâche 2"}))

    cahier_des_charges = CahierDesCharges(taches=frozenset({tache1, tache2, tache3}))

    with pytest.raises(ValidationError):
        cahier_des_charges.taches = frozenset({tache1, tache2})

    with pytest.raises(AttributeError):
        cahier_des_charges.taches.add(tache3)

    with pytest.raises(AttributeError):
        cahier_des_charges.taches.remove(tache1)


def test_serialisation_tache():
    """Test de la sérialisation d'une Tache"""
    tache = Tache(nom="tâche 1", duree=10)
    json_tache = tache.model_dump_json()
    assert json_tache == '{"nom":"tâche 1","duree":10.0,"prerequis":[]}'


def test_serialisation_deserialisation_tache():
    """Teste que l'on peut effectivement désérialiser après avoir sérialiser une Tache"""
    tache = Tache(nom="tâche 1", duree=10)
    json_tache = tache.model_dump_json()
    tache_deserialisee = Tache.model_validate_json(json_tache)
    assert tache == tache_deserialisee


def test_serialisation_deserialisation_cahier_des_charges():
    """Teste que l'on peut effectivement désérialiser après avoir sérialiser un CahierDesCharges"""
    cdc = CahierDesCharges(
        taches=frozenset(
            [
                Tache(nom="tâche 1", duree=10),
                Tache(nom="tâche 2", duree=20, prerequis=frozenset(["tâche 1"])),
                Tache(nom="tâche 3", duree=30, prerequis=frozenset(["tâche 2"])),
            ]
        )
    )
    json_cdc = cdc.model_dump_json()
    cdc_deserialise = CahierDesCharges.model_validate_json(json_cdc)
    assert cdc == cdc_deserialise


def test_creation_intervalle_valide():
    """Test la création d'un intervalle valide."""
    intervalle = Intervalle(debut=1.0, fin=2.0)
    assert intervalle.debut == 1.0
    assert intervalle.fin == 2.0


def test_creation_intervalle_invalide():
    """Test la création d'un intervalle invalide (la fin est avant le début)."""
    with pytest.raises(ValidationError) as excinfo:
        Intervalle(debut=3.0, fin=2.0)

    assert "La fin est avant le début" in str(excinfo.value)


def test_creation_intervalle_valeurs_negatives():
    """Test la création d'un intervalle avec des valeurs négatives."""
    with pytest.raises(ValidationError) as excinfo:
        Intervalle(debut=-2.0, fin=-1.0)

    assert "Input should be greater than 0" in str(excinfo.value)
