#!/usr/bin/python3
"""Définit la classe City, liée à la table cities de MySQL."""
from sqlalchemy import Column, ForeignKey, Integer, String
from model_state import Base


class City(Base):
    """Représente une ville, une ligne de la table cities."""
    # Nom de la table MySQL associée à cette classe
    __tablename__ = "cities"
    # Clé primaire : entier unique, généré automatiquement, jamais nul
    id = Column(Integer, primary_key=True, autoincrement=True,
                nullable=False)
    # Nom de la ville : 128 caractères maximum, jamais nul
    name = Column(String(128), nullable=False)
    # Clé étrangère : contient l'id d'une ligne de la table states
    state_id = Column(Integer, ForeignKey("states.id"), nullable=False)
