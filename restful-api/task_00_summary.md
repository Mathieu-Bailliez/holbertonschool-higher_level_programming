# HTTP/HTTPS

## 1.0 Anatomie d'une requête

>POST /users HTTP/1.1                <- 1. ligne de requête : MÉTHODE  CHEMIN  VERSION

>Host: api.exemple.com               <- 2. en-têtes (headers) : "Nom: valeur"

>Content-Type: application/json         un par ligne, autant qu'il faut

>Authorization: Bearer abc123

><- 3. ligne vide OBLIGATOIRE : fin des en-têtes

>{"username": "alice"} <- 4. corps (body) : optionnel, les données envoyées

- La méthode dit l'intention (lire, créer, supprimer...).
- Le chemin dit sur quelle ressource.
- Les en-têtes sont des métadonnées, c'est-à-dire des données sur le message : son format, sa taille, qui l'envoie.
- Le corps contient les données elles-mêmes. Une requête GET n'en a généralement pas.

## 1.1 Anatomie d'une réponse

>HTTP/1.1 201 Created                <- 1. ligne de statut : VERSION  CODE  MESSAGE

>Content-Type: application/json      <- 2. en-têtes

>Content-Length: 41

><- 3. ligne vide obligatoire

>{"message": "User added", "id": 7}  <- 4. corps : les données renvoyées

Même structure que la requête ; seule la première ligne change. Retiens ce schéma en 4 étages : première ligne, en-têtes, ligne vide, corps.

## 1.3 Les méthodes : quoi faire de la ressource

Une API gère presque toujours quatre opérations de base, qu'on appelle **CRUD** : Create (créer), Read (lire), Update (modifier), Delete (supprimer). Chaque opération correspond à une méthode HTTP.

| Méthode | CRUD | Ce qu'elle fait | Exemple d'usage | Corps envoyé ? |
|---|---|---|---|---|
| `GET` | Read | Récupère une ressource sans la modifier | Lire la fiche de l'utilisateur 1 | Non |
| `POST` | Create | Crée une nouvelle ressource | Inscrire un nouvel utilisateur | Oui |
| `PUT` | Update | Remplace entièrement une ressource | Réécrire tout le profil | Oui |
| `PATCH` | Update | Modifie une partie d'une ressource | Changer seulement l'email | Oui |
| `DELETE` | Delete | Supprime une ressource | Supprimer un article | Non |
| `HEAD` | (Read) | Comme `GET`, mais sans le corps de la réponse | Vérifier qu'une page existe | Non |

Deux propriétés à connaître, car elles reviennent en entretien :

- **Sûre (safe)** : la méthode ne modifie rien sur le serveur. `GET` et `HEAD` sont sûres.
- **Idempotente** : la répéter 10 fois produit le même état qu'une seule fois. `GET`, `PUT` et `DELETE` le sont ; **`POST` ne l'est pas** (10 `POST` = 10 utilisateurs créés). C'est pour cela que ton navigateur te prévient avant de renvoyer un formulaire.

## 1.4 Les codes de statut : comment ça s'est passé

Le **premier chiffre** suffit à savoir qui est concerné :

| Famille | Sens | Qui est concerné |
|---|---|---|
| `1xx` | Information, traitement en cours | Rare, tu ne le verras presque jamais |
| `2xx` | Succès | Personne, tout va bien |
| `3xx` | Redirection, « va voir ailleurs » | Le client doit refaire sa requête ailleurs |
| `4xx` | Erreur du client | Toi : ta requête est fausse |
| `5xx` | Erreur du serveur | Le serveur : son code a planté |

Les codes à connaître par cœur pour ce projet :

| Code | Nom | Scénario typique |
|---|---|---|
| `200` | OK | Un `GET` réussi renvoie la ressource |
| `201` | Created | Un `POST` a créé un utilisateur |
| `204` | No Content | Un `DELETE` a réussi, rien à renvoyer |
| `301` | Moved Permanently | `http://github.com` redirige vers `https://github.com` |
| `400` | Bad Request | Le JSON envoyé est mal formé ou un champ manque |
| `401` | Unauthorized | Route protégée, mais tu n'as pas dit qui tu es |
| `403` | Forbidden | On sait qui tu es, mais tu n'as pas le droit |
| `404` | Not Found | La ressource demandée n'existe pas |
| `405` | Method Not Allowed | Un `POST` sur une route qui n'accepte que `GET` |
| `500` | Internal Server Error | Une exception Python non gérée côté serveur |

### Exercice de prédiction

**Avant chaque commande, écris sur papier le code que tu attends.**

```bash
# -s : silencieux ; -o /dev/null : jeter le corps ; -w : n'afficher que le code
curl -s -o /dev/null -w '%{http_code}\n' https://jsonplaceholder.typicode.com/users/1
curl -s -o /dev/null -w '%{http_code}\n' https://jsonplaceholder.typicode.com/users/999
curl -s -o /dev/null -w '%{http_code}\n' -X POST https://jsonplaceholder.typicode.com/users
curl -s -o /dev/null -w '%{http_code}\n' http://github.com
```

Ce que tu dois constater : 200, 404, 201, 301.


### 1.5 HTTPS : la même chose, dans une enveloppe scellée

En HTTP, ton texte voyage **en clair** : tout appareil sur le chemin (Wi-Fi public, box, fournisseur d'accès) peut le lire et le modifier. Ton exercice 2.1 l'a montré : tu as lu la réponse en texte brut.

**HTTPS = HTTP + TLS.** TLS (Transport Layer Security, autrefois appelé SSL) ajoute trois garanties :

| Garantie | Sens | Ce qui se passe sans |
|---|---|---|
| Confidentialité | Le contenu est chiffré, illisible en route | Un voisin sur le Wi-Fi lit ton mot de passe |
| Authenticité | Un **certificat** prouve que le serveur est bien celui qu'il prétend | Un faux site se fait passer pour ta banque |
| Intégrité | Toute modification en route est détectée | Quelqu'un insère une publicité ou un virus dans la page |

Un **certificat** est une carte d'identité numérique du serveur, signée par une **autorité de certification** (CA) en qui ton système a confiance, comme une préfecture qui signe une carte d'identité.

HTTP utilise le port **80**, HTTPS le port **443**. Le contenu HTTP (méthodes, codes, en-têtes) est **strictement identique** ; seul le transport change.

```bash
# port HTTPS 443, sans chiffrement
printf 'GET / HTTP/1.1\r\nHost: example.com\r\n\r\n' | timeout 5 nc example.com 443 | head -5

# Observer le certificat présenté par le serveur
openssl s_client -connect example.com:443 -servername example.com </dev/null 2>/dev/null | grep -E 'subject=|issuer='
```
