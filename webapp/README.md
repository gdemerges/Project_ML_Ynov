# Application Web Streamlit - Prédiction de Dépression

Cette application web permet aux utilisateurs de prédire s'ils sont à risque de dépression en fonction de leur style de vie et de leurs conditions académiques.

## Fonctionnalités

- **Interface utilisateur intuitive** : Formulaire simple pour saisir les informations
- **Prédiction en temps réel** : Appel à l'API de serving pour obtenir une prédiction
- **Recommandations** : Conseils basés sur le résultat de la prédiction
- **Système de feedback** : Permet aux utilisateurs de fournir la vraie valeur pour améliorer le modèle

## Structure

```
webapp/
├── app.py                  # Application Streamlit principale
├── Dockerfile             # Configuration Docker
├── docker-compose.yml     # Orchestration Docker Compose
├── requirements.txt       # Dépendances Python
└── README.md             # Ce fichier
```

## Prérequis

- Docker et Docker Compose installés
- L'API de serving doit être démarrée et accessible

## Lancement de l'application

### 1. Démarrer l'API de serving (prérequis)

Depuis le dossier racine du projet :

```bash
docker compose -f serving/docker-compose.yml up
```

### 2. Démarrer l'application web

Depuis le dossier racine du projet :

```bash
docker compose -f webapp/docker-compose.yml up
```

Pour forcer la reconstruction de l'image (après modification du code) :

```bash
docker compose -f webapp/docker-compose.yml up --build --force-recreate
```

### 3. Accéder à l'application

Ouvrez votre navigateur et accédez à :

```
http://localhost:8081
```

## Utilisation

1. **Remplir le formulaire** avec vos informations :
   - Informations démographiques (genre, âge, ville, profession)
   - Informations académiques (CGPA, heures d'étude)
   - Style de vie (sommeil, habitudes alimentaires)
   - Niveaux de stress et satisfaction

2. **Cliquer sur "Prédire"** pour obtenir une prédiction

3. **Consulter le résultat** :
   - ⚠️ Risque de dépression détecté
   - ✅ Pas de risque détecté

4. **Optionnel : Fournir un feedback** pour aider à améliorer le modèle

## Données collectées

L'application collecte les informations suivantes :

- **Démographiques** : Genre, Âge, Ville, Profession
- **Académiques** : CGPA (moyenne), Heures d'étude
- **Style de vie** : Durée de sommeil, Habitudes alimentaires
- **Psychologiques** : Pression académique, Pression au travail, Satisfaction des études, Satisfaction du travail, Stress financier
- **Médicales** : Antécédents familiaux de maladie mentale

## API utilisée

L'application communique avec l'API de serving via deux endpoints :

- **POST** `http://serving-api:8080/predict` : Prédiction
- **POST** `http://serving-api:8080/feedback` : Envoi de feedback

## Notes importantes

⚠️ **Disclaimer** : Cette application est à but éducatif uniquement. Elle ne remplace pas un diagnostic médical professionnel.

## Ressources de soutien

En cas de détresse psychologique :

- **SOS Amitié** : 09 72 39 40 50
- **Fil Santé Jeunes** : 0 800 235 236
- **Suicide Écoute** : 01 45 39 40 00

## Développement

### Exécution en local (sans Docker)

```bash
cd webapp
pip install -r requirements.txt
streamlit run app.py --server.port 8081
```

Note : Modifiez les URLs de l'API dans `app.py` pour pointer vers `http://localhost:8080` au lieu de `http://serving-api:8080`.

### Arrêt de l'application

```bash
docker compose -f webapp/docker-compose.yml down
```

## Projet

- **Cours** : Concepts, fonctionnements et technologies de l'IA
- **Formation** : M1 DataEng - Ynov
- **Année** : 2025-2026
