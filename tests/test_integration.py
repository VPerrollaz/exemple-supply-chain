#! /usr/bin/env python
# -*- coding: utf-8 -*-
"""Description.

Tests d'intégration en l'occurence de l'interface typer
"""
from subprocess import run
from pathlib import Path


def test_demo():
    """Essai de la sous commande demo"""
    run(["python", "-m", "exemple_supply_chain", "demo"])
    chemin_attendu = Path(".").resolve() / "demonstration.json"
    assert chemin_attendu.exists()
    contenu = chemin_attendu.read_text()
    resultat_attendu = """
{
  "taches": [
    {
      "nom": "tâche 1",
      "duree": 10.0,
      "prerequis": []
    },
    {
      "nom": "tâche 2",
      "duree": 20.0,
      "prerequis": [
        "tâche 1"
      ]
    },
    {
      "nom": "tâche 3",
      "duree": 30.0,
      "prerequis": [
        "tâche 2"
      ]
    }
  ]
}
    """.strip()

    assert contenu == resultat_attendu
    chemin_attendu.unlink()


def test_view():
    """Essai de la sous commande view"""
    run(["python", "-m", "exemple_supply_chain", "demo"])
    resultat = run(
        ["python", "-m", "exemple_supply_chain", "view", "demonstration.json"],
        capture_output=True,
    )
    resultat_attendu = (
        "      Cahier des Charges       \n"
        "┏━━━━━━━━━┳━━━━━━━┳━━━━━━━━━━━┓\n"
        "┃ Nom     ┃ Durée ┃ Prérequis ┃\n"
        "┡━━━━━━━━━╇━━━━━━━╇━━━━━━━━━━━┩\n"
        "│ tâche 1 │ 10.00 │           │\n"
        "│ tâche 2 │ 20.00 │ tâche 1   │\n"
        "│ tâche 3 │ 30.00 │ tâche 2   │\n"
        "└─────────┴───────┴───────────┘\n"
    )
    assert resultat.stdout.decode("utf8") == resultat_attendu
    chemin_attendu = Path(".").resolve() / "demonstration.json"
    chemin_attendu.unlink()


def test_solve():
    """Essai de la sous commande solve"""
    run(["python", "-m", "exemple_supply_chain", "demo"])
    resultat = run(
        ["python", "-m", "exemple_supply_chain", "solve", "demonstration.json"],
        capture_output=True,
    )
    resultat_attendu = (
        "                   Planning                    \n"
        "┏━━━━━━━━━┳━━━━━━━┳━━━━━━━┳━━━━━━━┳━━━━━━━━━━━┓\n"
        "┃ Nom     ┃ Début ┃ Fin   ┃ Durée ┃ Prérequis ┃\n"
        "┡━━━━━━━━━╇━━━━━━━╇━━━━━━━╇━━━━━━━╇━━━━━━━━━━━┩\n"
        "│ tâche 1 │ 0.00  │ 10.00 │ 10.00 │           │\n"
        "│ tâche 2 │ 10.00 │ 30.00 │ 20.00 │ tâche 1   │\n"
        "│ tâche 3 │ 30.00 │ 60.00 │ 30.00 │ tâche 2   │\n"
        "└─────────┴───────┴───────┴───────┴───────────┘\n"
    )
    assert resultat.stdout.decode("utf8") == resultat_attendu
    chemin_attendu = Path(".").resolve() / "demonstration.json"
    chemin_attendu.unlink()
