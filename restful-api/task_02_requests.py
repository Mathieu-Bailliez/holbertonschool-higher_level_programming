#!/usr/bin/python3
"""Récupère les posts de JSONPlaceholder pour les afficher ou en CSV."""
import csv
import json

import requests

# Adresse de l'endpoint qui renvoie la liste de tous les posts
URL = "https://jsonplaceholder.typicode.com/posts"


def fetch_and_print_posts():
    """Affiche le code de statut puis le titre de chaque post."""
    # Envoie une requête GET : on récupère un objet Response
    response = requests.get(URL)
    # Affiche le code HTTP au format exact demandé par le sujet
    print("Status Code: {}".format(response.status_code))
    # On ne lit le corps que si le serveur a répondu "200 OK"
    if response.status_code == 200:
        # .json() transforme le texte JSON en liste de dicts Python
        posts = response.json()
        # Chaque post est un dict : on affiche sa valeur "title"
        for post in posts:
            print(post["title"])


def fetch_and_save_posts():
    """Enregistre l'id, le titre et le corps des posts dans posts.csv."""
    response = requests.get(URL)
    if response.status_code == 200:
        posts = response.json()
        # Compréhension de liste : un nouveau dict par post,
        # avec seulement les 3 clés demandées (on ignore userId)
        data = [
            {"id": post["id"], "title": post["title"], "body": post["body"]}
            for post in posts
        ]
        # "w" = écrire (écrase l'ancien fichier) ;
        # newline="" évite les lignes vides parasites du module csv
        with open("posts.csv", "w", newline="", encoding="utf-8") as f:
            # fieldnames fixe les colonnes et leur ordre
            writer = csv.DictWriter(f, fieldnames=["id", "title", "body"])
            writer.writeheader()      # écrit la ligne : id,title,body
            writer.writerows(data)    # écrit une ligne par dict
