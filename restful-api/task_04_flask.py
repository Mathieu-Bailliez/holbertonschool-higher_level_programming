#!/usr/bin/python3
"""API Flask qui gère des utilisateurs stockés en mémoire."""
from flask import Flask, jsonify, request

# Crée l'application Flask
app = Flask(__name__)

# Utilisateurs en mémoire : clé = username, valeur = dict complet.
# Laissé VIDE comme l'exige le sujet (pas de données de test poussées)
users = {}


@app.route("/")
def home():
    """Renvoie le message d'accueil de l'API."""
    return "Welcome to the Flask API!"


@app.route("/data")
def data():
    """Renvoie la liste de tous les usernames enregistrés."""
    # users.keys() donne les clés ; list() les met dans une vraie liste
    return jsonify(list(users.keys()))


@app.route("/status")
def status():
    """Indique que l'API fonctionne."""
    return "OK"


@app.route("/users/<username>")
def get_user(username):
    """Renvoie l'utilisateur demandé, ou une erreur 404."""
    # Route dynamique : la partie <username> de l'URL arrive en paramètre
    user = users.get(username)          # None si le username est absent
    if user is None:
        return jsonify({"error": "User not found"}), 404
    return jsonify(user)


@app.route("/add_user", methods=["POST"])
def add_user():
    """Ajoute un utilisateur à partir du JSON envoyé par le client."""
    # silent=True : renvoie None au lieu de planter si le JSON est invalide
    user_data = request.get_json(silent=True)
    # 1. Corps illisible, ou JSON qui n'est pas un objet { }
    if not isinstance(user_data, dict):
        return jsonify({"error": "Invalid JSON"}), 400
    username = user_data.get("username")
    # 2. Champ username absent ou vide
    if not username:
        return jsonify({"error": "Username is required"}), 400
    # 3. Username déjà pris
    if username in users:
        return jsonify({"error": "Username already exists"}), 409
    # 4. Tout est valide : on enregistre l'objet complet
    users[username] = user_data
    return jsonify({"message": "User added", "user": user_data}), 201


if __name__ == "__main__":
    app.run()
