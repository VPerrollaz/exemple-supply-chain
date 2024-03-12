#! /usr/bin/env python
# -*- coding: utf-8 -*-
"""Description.

Transformations de CahierDesCharges et dict[Tache, Intervalle] vers des tables rich pour affichage.
"""

from .data import Tache, Intervalle, CahierDesCharges
from rich.table import Table  # type: ignore


def cahier_to_table(cahier: CahierDesCharges) -> Table:
    """Convertit un CahierDesCharges en une table Rich.

    Args:
        cahier (CahierDesCharges): Le cahier des charges à convertir.

    Returns:
        Table: La table Rich correspondant au cahier des charges.
    """
    resultat = Table(title="Cahier des Charges")
    resultat.add_column("Nom")
    resultat.add_column("Durée")
    resultat.add_column("Prérequis")
    for tache in cahier.taches:
        resultat.add_row(tache.nom, f"{tache.duree:.2f}", ", ".join(tache.prerequis))
    return resultat


def planning_to_table(planning: dict[Tache, Intervalle]) -> Table:
    """Convertit un dictionnaire de Tache vers Intervalle en une table Rich.

    Args:
        planning (dict[Tache, Intervalle]): Le planning à convertir.

    Returns:
        Table: La table Rich correspondant au planning.
    """
    resultat = Table(title="Planning")
    resultat.add_column("Nom")
    resultat.add_column("Début")
    resultat.add_column("Fin")
    resultat.add_column("Durée")
    resultat.add_column("Prérequis")
    for tache, intervalle in planning.items():
        resultat.add_row(
            tache.nom,
            f"{intervalle.debut:.2f}",
            f"{intervalle.fin:.2f}",
            f"{tache.duree:.2f}",
            ", ".join(tache.prerequis),
        )
    return resultat
