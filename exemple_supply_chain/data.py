#! /usr/bin/env python
# -*- coding: utf-8 -*-
"""Description.

Classes principales.
"""

from pydantic import BaseModel, PositiveInt, PositiveFloat, ConfigDict, field_validator  # type: ignore


class Tache(BaseModel):
    """
    Une classe représentant une tâche avec un nom, une durée et des prérequis.

    Attributes:
        nom (str): Le nom de la tâche.
        duree (int | float): La durée de la tâche en minutes.
        prerequis (FrozenSet[str]): Les prérequis de la tâche sous forme de noms de tâches.
    """

    nom: str
    duree: PositiveFloat | PositiveInt
    prerequis: frozenset[str]

    model_config = ConfigDict(frozen=True)

    @field_validator("prerequis")
    def absence_cycle(cls, prerequis, champs):
        if champs.data["nom"] in prerequis:
            raise ValueError("Prérequis cyclique!")
        return prerequis

    def __hash__(self):
        """
        Calcule le hachage de la tâche en fonction de ses attributs.

        Returns:
            int: Le hachage de la tâche.
        """
        return hash((self.nom, self.duree, self.prerequis))
