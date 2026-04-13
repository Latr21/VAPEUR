**[Accès au wiki du projet](https://github.com/Latr21/VAPEUR/wiki)**

# Décision d'Architecture
Contexte : Réalisation du concurrent de Steam, "Vapeur", par une équipe de 5 développeurs.

## 1. Architecture Hybride (N-Tiers & Microservices)
Approche hybride, N-tiers pour la séparation des couches de présentation, logique métier et données, et un découpage en microservices métiers.

- Répartition du travail : Le découpage en tiers nous a permis de se répartir les tâches clairement sans créer de conflits au nivea du repo.

- Isolation de la logique métier : En découpant le projet par domaines (Magasin, Bibliothèque, Communauté, etc), nous pouvons développé simultanément différentes features sans craindre un développement bloquant pour certains. Si un développeur prend du retard sur le service "Communauté", cela ne bloque pas le développement ou la mise en prod du service "Magasin".

- Respect de la deadline : Nous avons évité de rendre nos micro servics trop fin pour éviter une infra complexe pour leur gestion, au profit de services de taille moyenne, adaptés à une équipe de 4 personnes.

## 2. Uniformisation de la Stack : 100% Python
Au début pensé en JavaScript (React/Node), le projet a finalement pris la direction d'un écosystème full Python (Django + FastAPI). C'est la décision la plus simple à court terme pour respecter notre deadline.

- Réduction de la charge lié au changement de langage : Passer du front-end au back-end ne demande plus de changer de langage. Un développeur peut coder une interface sur Django le matin et optimiser une route FastAPI l'après-midi sans temps d'adaptation.

- Mutualisation du code : L'utilisation de Python de bout en bout permet de partager des bibliothèques, des modèles de données (via Pydantic et Pydantic-Settings) et des scripts utilitaires entre le front et le back-end.

- Utilisation des outils existants : Django fournit nativement des outils "clés en main" (système de templates, formulaires, sécurité CSRF) qui nous évitent de recoder un front-end complet depuis zéro (comme ce serait le cas avec React), ce qui est un gain de temps.

## 3. Multiple moteurs de BDD (PostgreSQL, MongoDB, Redis)
Plutôt que d'essayer de tout faire rentrer dans une seule base de données (ce qui crée des goulots d'étranglement ou force à faire des compromis), nous utilisons l'outil adapté pour chaque cas d'usage.

- **PostgreSQL**: Utilisé pour les transactions financières (Achats) et la gestion des utilisateurs/bibliothèques. Les transactions exigeant une intégrité absolue (conformité **ACID**).

- **MongoDB**: Utilisé pour l'aspect communautaire (commentaires, avis, discussions). Mongo nous permet d'itérer très vite sur la structure des avis ou des profils sociaux.

- **Redis**: Utilisé comme cache pour le catalogue de jeux. L'affichage du magasin ne doit pas solliciter PostgreSQL en permanence. Redis permet des temps de réponse en quelques millisecondes, offrant une sensation de fluiditépour  l'utilisateur.

## 4. Réplication sur PostgreSQL (Instance Primaire + Répliques)
Mettre en place un cluster PostgreSQL est une nécessité pour une plateforme e-commerce de jeux vidéo.

- Séparation des Lectures/Écritures: Sur une boutique comme Vapeur, 95% du trafic est de la lecture (les joueurs parcourent le catalogue, regardent leurs succès) et 5% de l'écriture (ils achètent un jeu ou s'inscrivent). Les requêtes de consultation sont envoyées aux "Répliques", ce qui libère totalement la base "Primaire" pour qu'elle puisse traiter les paiements rapidement et sans surcharge.

- Haute Disponibilité: Si la base de données principale tombe en panne, une réplique peut prendre le relais instantanément. 

## Ressources et webographie

### Team's GoogleSlide
- [We are Google Slide](https://docs.google.com/presentation/d/1AkrfttjZIH0z7wsUwQalpmRo8OgUjrXfzfWptfO9I_s/edit?usp=sharing)

### Support de cours
[Notion de support du formateur](https://opposite-raft-210.notion.site/Page-apprenants-33b2bbbf507380aea88fef56892767d6)

### Références et documentations
- [c4model.com - How to C4](https://c4model.com/)
- [plantuml.com - A comprehensive guide to masterize PlantUML](https://plantuml.com/)
- [doc.sqlalchemy.org - Toolkit for Database working](https://docs.sqlalchemy.org/en/20/)
- [PyMongo.readthedoc.io - Tool for Python's MongoDB Working](https://pymongo.readthedocs.io/en/3.12.3/migrate-to-pymongo3.html)
- [Kinsta.com : Postgres - Replica](https://kinsta.com/blog/postgresql-replication/)
