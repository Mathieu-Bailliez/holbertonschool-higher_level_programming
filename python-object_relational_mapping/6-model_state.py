#!/usr/bin/python3
"""Creates the states table in the database from the State model."""
import sys
from model_state import Base, State
from sqlalchemy import create_engine


if __name__ == "__main__":
    # L'engine = la connexion à MySQL, décrite par une URL :
    # dialecte+pilote://user:mot_de_passe@hôte:port/base
    engine = create_engine("mysql+mysqldb://{}:{}@localhost:3306/{}"
                           .format(sys.argv[1], sys.argv[2], sys.argv[3]),
                           pool_pre_ping=True)

    # Crée toutes les tables des classes héritant de Base (ici : states)
    # State doit être importé AVANT, sinon Base ne la connaît pas
    Base.metadata.create_all(engine)
