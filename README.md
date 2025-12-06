# RedPill IA - Générateur de Vidéos Publicitaires

Génération de vidéos publicitaires avec IA pour l'application RedPill IA.

## Installation
```bash
# Créer environnement virtuel
python3 -m venv venv
source venv/bin/activate  # Mac/Linux

# Installer dépendances
pip install -r requirements.txt
```

## Utilisation
```bash
# Générer pub 1
python generator.py 1

# Générer pub 2
python generator.py 2

# Générer pub 3
python generator.py 3
```

## Timing estimé (MacBook Air M3)

- Pub 1: ~2h
- Pub 2: ~2h
- Pub 3: ~2h

**Total: 6-8h avec pauses refroidissement**

## Fichiers générés

Les vidéos sont sauvegardées dans `outputs/`:
- `redpill_pub_transformation.mp4`
- `redpill_pub_solution.mp4`
- `redpill_pub_comparaison.mp4`

## Ajouter une nouvelle pub

1. Créer `prompts/pub_X.py`
2. Définir SCENES et VIDEO_NAME
3. Lancer `python generator.py X`