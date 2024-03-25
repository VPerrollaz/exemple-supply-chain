#! /usr/bin/env python
# -*- coding: utf-8 -*-
"""Description.

Interface typer pour l'ordonnancement de tâche
"""
import sys
from typer import Typer
from .visualisation import cahier_to_table, planning_to_table
from .data import CahierDesCharges, Tache
from .algos import produit_planning
from rich import print

app = Typer()


@app.command()
def demo():
    """Génère un fichier demonstration.json contenant un cahier des charges"""
    cdc = CahierDesCharges(
        taches=tuple(
            [
                Tache(nom="tâche 1", duree=10),
                Tache(nom="tâche 2", duree=20, prerequis=tuple(["tâche 1"])),
                Tache(nom="tâche 3", duree=30, prerequis=tuple(["tâche 2"])),
            ]
        )
    )
    with open("demonstration.json", "w") as fichier:
        fichier.write(cdc.model_dump_json(indent=2))


@app.command()
def view(chemin: str):
    """Visualise un fichier json encodant un cahier des charges"""
    with open(chemin, "r") as fichier:
        donnees = fichier.read()
    try:
        cahier = CahierDesCharges.model_validate_json(donnees)
    except Exception as err:
        print(err)
        sys.exit(1)
    print(cahier_to_table(cahier))


@app.command()
def solve(chemin: str):
    """Produit un planning d'ordonnancement à partir du cahier des charges indiqué par le chemin"""
    with open(chemin, "r") as fichier:
        donnees = fichier.read()
    try:
        cahier = CahierDesCharges.model_validate_json(donnees)
    except Exception as err:
        print(err)
        sys.exit(1)
    planning = produit_planning(cahier)
    print(planning_to_table(planning))


if __name__ == "__main__":
    app()
