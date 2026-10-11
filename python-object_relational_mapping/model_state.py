#!/usr/bin/python3
"""Defines the State class mapped to the MySQL table states."""
from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

# Base = classe mère de tous les modèles : elle enregistre chaque classe
# qui hérite d'elle pour pouvoir créer les tables correspondantes
Base = declarative_base()


class State(Base):
    """Represents a state, each instance is one row of the states table."""

    # Nom de la table MySQL à laquelle cette classe est liée
    __tablename__ = 'states'

    # Colonne id : entier, clé primaire, auto-incrémenté, jamais NULL
    id = Column(Integer, primary_key=True, autoincrement=True,
                nullable=False)

    # Colonne name : chaîne de 128 caractères max, jamais NULL
    name = Column(String(128), nullable=False)
