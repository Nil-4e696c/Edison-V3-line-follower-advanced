# 🤖 Robot Suiveur de Ligne – Compétition Alstom 2025

Projet réalisé dans le cadre d'une compétition inter-écoles organisée par **Alstom**

## 🧠 Objectifs

- Suivi de ligne précis sur parcours plus complexe que ceux de alstom
- Pause au dessert, et en cas d'obstacle (autres robot)
- Calibration automatique des capteurs sur du blanc
- Détection de départ via capteur de son (clap)

## 🛠️ Technologies

- **Edison V3** (robot programmable)
- **Python** (API Ed.V3)
- Utilisation de capteurs :
  - Détection de ligne
  - Détection d’obstacle
  - Clap sonore
  - Feedback LED & bip

## 📁 Contenu du dépôt

| Fichier         | Description |
|----------------|-------------|
| `circuit1.py`   | Version du robot qui suit la ligne noire à **droite** |
| `circuit2.py`   | Version inversée qui suit la ligne noire à **gauche** (sens opposé adapté à certains circuits) |
