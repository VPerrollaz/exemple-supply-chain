#! /usr/bin/env python
# -*- coding: utf-8 -*-
"""Description.

Tests du module visualisation.py
"""

from exemple_supply_chain import (
    CahierDesCharges,
    Intervalle,
    Tache,
    cahier_to_table,
    planning_to_table,
)
from rich.console import Console  # type: ignore


def test_cahier_to_table_print():
    tache_a = Tache(nom="A", prerequis=tuple(), duree=2.0)
    tache_b = Tache(nom="B", prerequis=tuple(["A"]), duree=3.0)
    tache_c = Tache(nom="C", prerequis=tuple(["B"]), duree=4.0)
    cahier = CahierDesCharges(taches=tuple([tache_a, tache_b, tache_c]))
    console = Console()
    with console.capture() as capture:
        console.print(cahier_to_table(cahier))
    output = capture.get()

    expected_output = (
        "    Cahier des Charges     \n"
        "┏━━━━━┳━━━━━━━┳━━━━━━━━━━━┓\n"
        "┃ Nom ┃ Durée ┃ Prérequis ┃\n"
        "┡━━━━━╇━━━━━━━╇━━━━━━━━━━━┩\n"
        "│ A   │ 2.00  │           │\n"
        "│ B   │ 3.00  │ A         │\n"
        "│ C   │ 4.00  │ B         │\n"
        "└─────┴───────┴───────────┘\n"
    )

    assert output == expected_output


def test_planning_to_table_print():
    tache_a = Tache(nom="A", prerequis=tuple(), duree=2.0)
    tache_b = Tache(nom="B", prerequis=tuple(["A"]), duree=3.0)
    tache_c = Tache(nom="C", prerequis=tuple(["B"]), duree=4.0)
    planning = {
        tache_a: Intervalle(debut=0.0, fin=2.0),
        tache_b: Intervalle(debut=2.0, fin=5.0),
        tache_c: Intervalle(debut=5.0, fin=9.0),
    }

    console = Console()
    with console.capture() as capture:
        console.print(planning_to_table(planning))
    output = capture.get()
    expected_output = (
        "                 Planning                 \n"
        "┏━━━━━┳━━━━━━━┳━━━━━━┳━━━━━━━┳━━━━━━━━━━━┓\n"
        "┃ Nom ┃ Début ┃ Fin  ┃ Durée ┃ Prérequis ┃\n"
        "┡━━━━━╇━━━━━━━╇━━━━━━╇━━━━━━━╇━━━━━━━━━━━┩\n"
        "│ A   │ 0.00  │ 2.00 │ 2.00  │           │\n"
        "│ B   │ 2.00  │ 5.00 │ 3.00  │ A         │\n"
        "│ C   │ 5.00  │ 9.00 │ 4.00  │ B         │\n"
        "└─────┴───────┴──────┴───────┴───────────┘\n"
    )
    assert output == expected_output
