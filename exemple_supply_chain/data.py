#! /usr/bin/env python
# -*- coding: utf-8 -*-
"""Description.

Classes principales: Tache, CahierDesCharges, Intervalle.
"""
from typing import Any
from pydantic import BaseModel, PositiveInt, PositiveFloat, ConfigDict, field_validator, model_validator, ValidationError  # type: ignore


class Tache(BaseModel):
    """Une classe représentant une tâche avec un nom, une durée et des prérequis.

    Attributes:
        nom (str): Le nom de la tâche.
        duree (int | float): La durée de la tâche en minutes.
        prerequis (FrozenSet[str]): Les prérequis de la tâche sous forme de noms de tâches.
    """

    nom: str
    duree: PositiveFloat | PositiveInt
    prerequis: frozenset[str] = frozenset()

    model_config = ConfigDict(frozen=True)

    @field_validator("prerequis")
    def absence_cycle(cls, prerequis, champs):
        if champs.data["nom"] in prerequis:
            raise ValueError(f"Prérequis {champs.data['nom']} cyclique!")
        return prerequis

    def __hash__(self):
        """
        Calcule le hachage de la tâche en fonction de ses attributs.

        Returns:
            int: Le hachage de la tâche.
        """
        return hash((self.nom, self.duree, self.prerequis))


class CahierDesCharges(BaseModel):
    """Classe représentant un cahier des charges.

    Attributes:
        taches (frozenset[Tache]): L'ensemble des tâches du cahier des charges.

    Raises:
        ValueError: Si un prérequis n'est pas une tâche valide.
    """

    taches: frozenset[Tache]

    model_config = ConfigDict(frozen=True)

    @field_validator("taches")
    def prerequis_existent(cls, taches: frozenset[Tache]) -> frozenset[Tache]:
        """Vérifie que tous les prérequis des tâches existent dans l'ensemble des tâches.

        Args:
            taches (frozenset[Tache]): L'ensemble des tâches du cahier des charges.

        Raises:
            ValueError: Si un prérequis n'est pas une tâche valide.

        Returns:
            frozenset[Tache]: L'ensemble des tâches du cahier des charges.
        """
        noms_taches_existantes = set(tache.nom for tache in taches)
        for tache in taches:
            for prerequis in tache.prerequis:
                if prerequis not in noms_taches_existantes:
                    raise ValueError(f"{prerequis} n'est pas un prérequis valide!")
        return taches


class Intervalle(BaseModel):
    """Classe représentant un intervalle de temps.

    Attributes:
        debut (PositiveFloat): Le début de l'intervalle.
        fin (PositiveFloat): La fin de l'intervalle.

    Raises:
        ValueError: Si la fin est avant le début.
    """

    debut: PositiveFloat
    fin: PositiveFloat

    @model_validator(mode="before")
    def bon_ordre(cls, donnees: Any) -> Any:
        """Vérifie que le début de l'intervalle est avant la fin.

        Args:
            donnees (Any): Les données de l'intervalle.

        Raises:
            ValueError: Si la fin est avant le début.

        Returns:
            Any: Les données de l'intervalle.
        """
        if donnees["debut"] > donnees["fin"]:
            raise ValueError(
                "La fin est avant le début: debut={valeurs[debut]} fin={valeurs[fin]}"
            )
        return donnees
