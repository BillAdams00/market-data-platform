# Market Data Platform

Plateforme de données de marché — modélisation, ingestion, entrepôt et qualité.

## 1. Le problème

Dans une société de gestion, le gérant, l'analyste risque et le reporting
client travaillent sur les mêmes titres. Mais chacun télécharge ses données
depuis sa propre source : l'un depuis Bloomberg, l'autre depuis un export du
dépositaire, le troisième depuis un fichier reçu par courriel.

Les chiffres divergent. L'un prend le cours de clôture, l'autre le dernier
cours traité ; l'un annualise la volatilité sur 252 jours, l'autre sur 260 ;
et le même titre porte trois identifiants différents selon la source.

Les réunions se passent alors à réconcilier des chiffres au lieu de décider.
Ce projet construit la source unique qui tranche la question.

## 2. État actuel

La modélisation du domaine est terminée, parce que les règles métier doivent
vivre dans le modèle et non dispersées dans des scripts.

- **Trois classes** : instrument, position, portefeuille
- **Validation à la construction** : aucune position invalide ne peut exister
- **Règles métier encodées** : prix de revient unitaire pondéré lors d'un achat
  complémentaire, unicité du titre dans un portefeuille
- **Valorisation** : montant investi, valeur de marché et plus-value latente,
  au niveau de la ligne comme du portefeuille
- **Persistance JSON** : sauvegarde et rechargement complet de l'état
- **Tests automatisés** : cinq tests pytest couvrant les calculs et les refus
- **Découpage en paquet** : une classe par module, dépendances à sens unique

## 3. Architecture

| Couche | Contenu | État |
|---|---|---|
| 00 | Modélisation du domaine | ✅ |
| 01 | Ingestion multi-sources → PostgreSQL | à venir |
| 02 | Transformations et indicateurs financiers | à venir |
| 03 | Entrepôt en étoile et contrôles qualité | à venir |
| 04 | Orchestration Airflow | à venir |
| 05 | Restitution BI | à venir |

## 4. Structure du dépôt

```
market_data_platform/
├── marketdata/
│   ├── __init__.py          façade du paquet : expose les trois classes
│   ├── instrument.py        class Instrument
│   ├── position.py          class Position
│   └── portefeuille.py      class PorteFeuille
├── test_portefeuille.py     suite pytest
├── demo.py                  scénario de démonstration
├── essai_chargement.py      preuve de la persistance
└── requirements.txt
```

Les dépendances entre modules vont dans un seul sens :

```
Instrument  ◄──  Position  ◄──  Portefeuille
```

Ce n'est pas une contrainte technique mais la traduction du métier :
un titre existe indépendamment de toute détention, une position n'a de sens
que rapportée à un titre. Un import en sens inverse signalerait une erreur
de modélisation.

## 5. Modèle de données

```
Portefeuille
├─ nom
└─ positions ──► Position
                 ├─ quantité
                 ├─ prix de revient
                 └─ instrument ──► Instrument
                                   ├─ symbole
                                   ├─ nom
                                   ├─ secteur
                                   └─ devise
```

`Instrument` décrit ce qu'est un titre, indépendamment de toute détention.
`Position` décrit la relation d'un investisseur à ce titre. `Portefeuille`
agrège sans recalculer.

Cette séparation prépare le schéma en étoile de la couche 03 : `Instrument`
deviendra une dimension, `Position` une table de faits.

## 6. Installation et exécution

Prérequis : Python 3.12 ou supérieur.

```bash
git clone https://github.com/BillAdams00/market-data-platform.git
cd market-data-platform

python -m venv .venv
.venv\Scripts\Activate.ps1        # Windows PowerShell
source .venv/bin/activate         # Linux / macOS

pip install -r requirements.txt
```

Le code métier ne dépend d'aucune bibliothèque externe ; `requirements.txt`
ne contient que les outils de développement, pytest en tête.

Lancer la démonstration :

```bash
python demo.py
```

Vérifier la persistance — le portefeuille est reconstruit depuis le fichier,
sans aucune donnée écrite dans le programme :

```bash
python essai_chargement.py
```

Lancer les tests :

```bash
pytest -v
```

## 7. Exemple de sortie

```
Portefeuille PEA Adams (2 positions)
Position(NVDA, 20 × 165.04000000000002)
4374.55
4415.5
Refusé : AAPL n'est pas détenu dans ce portefeuille
Refusé : Aucun cours fourni pour MSFT
```

## 8. Décisions techniques

**Le prix de revient est pondéré, pas moyenné.** Un achat complémentaire de
8 titres à 175,00 sur une ligne de 12 titres à 158,40 donne un PRU de 165,04,
et non 166,70. La moyenne simple traiterait les 8 titres comme s'ils pesaient
autant que les 12, et fausserait la plus-value affichée au client.

**Une donnée manquante n'est pas un zéro.** Si le cours d'un titre est absent,
la valorisation lève une erreur au lieu de retenir zéro. Un titre suspendu de
cotation ne vaut pas rien : on ignore sa valeur du jour. Écrire zéro
sous-estimerait le portefeuille dans un rapport client.

**La validation a lieu avant l'affectation.** Une quantité ou un prix négatif
interrompt la construction : l'objet invalide n'existe jamais. Refuser une
ligne à l'entrée coûte moins cher que de chercher l'origine d'un chiffre faux
trois jours plus tard.

**Le cours de marché est un paramètre, pas un attribut.** Le prix de revient
appartient à l'investisseur et ne bouge qu'aux transactions ; le cours
appartient au marché et change en continu. Les stocker ensemble imposerait de
mettre à jour chaque position à chaque variation.

**Les messages d'erreur nomment le titre et la valeur fautive.** Sur un
chargement de plusieurs milliers de lignes, un message générique oblige à
rouvrir le code ; un message précis permet de corriger la source.

**Les montants sont provisoirement des flottants.** Le PRU affiché
`165.04000000000002` le montre : la base 2 ne représente pas exactement les
décimales. Acceptable pour une démonstration, inacceptable pour un calcul de
performance qui doit se réconcilier au centime. La couche 01 introduira
`Decimal` côté Python et `NUMERIC` côté PostgreSQL.

## 9. Feuille de route

- Ingestion depuis Alpha Vantage, l'API de la BCE et FRED, avec chargement
  idempotent et journal d'exécution
- Indicateurs financiers : rendements, volatilité annualisée, maximum drawdown
- Schéma en étoile sur PostgreSQL et contrôles qualité automatisés
- Orchestration quotidienne avec Airflow
- Restitution décisionnelle

## 10. Auteur

Bill Adams — cycle ingénieur Data-IA, en recherche d'un stage de data engineer
en finance.