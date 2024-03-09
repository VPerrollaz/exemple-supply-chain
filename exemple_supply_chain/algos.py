#! /usr/bin/env python
# -*- coding: utf-8 -*-
"""Description.

Topological sorting des Taches puis production d'un planning.
"""
from .data import Tache, CahierDesCharges, Intervalle


def valide_tri_topologique(taches: list[Tache], cahier: CahierDesCharges) -> bool:
    """
    Vérifie si un tri topologique donné est valide pour un cahier des charges donné.

    Args:
        taches: Liste des tâches triées topologiquement.
        cahier: Cahier des charges contenant les tâches et leurs prérequis.

    Returns:
        True si le tri topologique est valide, False sinon.
    """
    precedents = set()
    for tache in taches:
        if not all(precedent in precedents for precedent in tache.prerequis):
            return False
        precedents.add(tache.nom)
    return len(precedents) == len(cahier.taches)


def tri_topologique(cahier: CahierDesCharges) -> list[Tache]:
    """Effectue un tri topologique des tâches dans un cahier des charges.

    Cette fonction utilise l'algorithme de tri topologique pour trouver un ordre linéaire des tâches
    dans un cahier des charges tel que tous les prérequis d'une tâche sont traités avant la tâche elle-même.

    Args:
        cahier (CahierDesCharges): Le cahier des charges contenant les tâches et leurs prérequis.

    Returns:
        list[Tache]: Une liste de tâches triées topologiquement.

    Raises:
        ValueError: Si le cahier des charges est insoluble, c'est-à-dire s'il contient des cycles
                     de dépendances entre les tâches.
    """
    resultat = list()
    deja_traitees = {tache.nom: False for tache in cahier.taches}
    while True:
        boucle_utile = False
        for tache in cahier.taches:
            if not deja_traitees[tache.nom] and all(
                deja_traitees[prerequis] for prerequis in tache.prerequis
            ):
                resultat.append(tache)
                deja_traitees[tache.nom] = True
                boucle_utile = True
        if not boucle_utile:
            break
    if all(deja_traitees.values()):
        return resultat
    else:
        raise ValueError("Le cahier des charges est insolubles!")


def produit_planning(cahier: CahierDesCharges) -> dict[Tache, Intervalle]:
    """Produit un planning pour le cahier des charges donné.

    Le planning est un dictionnaire associant chaque tâche à un intervalle de temps.
    Les intervalles de temps sont calculés en fonction des prérequis et de la durée de chaque tâche.

    Args:
        cahier (CahierDesCharges): Le cahier des charges contenant les tâches et leurs prérequis.

    Returns:
        dict[Tache, Intervalle]: Un dictionnaire associant chaque tâche à un intervalle de temps.

    Raises:
        ValueError: Si le cahier des charges est insoluble, c'est-à-dire s'il contient des cycles de dépendances.
    """
    taches_ordonnees = tri_topologique(cahier)
    resultat = dict()
    for tache in taches_ordonnees:
        if tache.prerequis:
            debut = max(resultat[prerequis].fin for prerequis in tache.prerequis)
        else:
            debut = 0.0
        resultat[tache.nom] = Intervalle(debut=debut, fin=debut + tache.duree)
    return {tache: resultat[tache.nom] for tache in cahier.taches}
