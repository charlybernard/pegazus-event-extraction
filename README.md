# 🦄 Pegazus Event Extraction

Pipeline complet pour l'extraction d'événements à partir de descriptions textuelles, avec génération de triplets relationnels à partir de phrases.

---

## 🔁 Pipeline d’extraction d’événements

### 1. 🎯 Entrée
- **Fichier CSV** contenant des phrases décrivant des événements à extraire.
- Extrait typique :
```
event,event_label,time,line_id,landmark_label,landmark_type,relatum_label,relatum_type,relation_type,change_type,change_on,attribute_type,outdates,makes_effective
96,rue eugène oudiné || Historique || Précédemment, rue Watt prolongée,,10605_historique,Rue Eugène Oudiné,rue,,,,transition,attribute,name,rue Watt prolongée,rue de Rigny
```

---

### 2. 🛠️ Conversion vers JSON

Deux cas selon la méthode utilisée :

#### Pour **LLM** :
Format JSON avec une phrase associée à une liste de triplets :
```json
{
  "sentence" : "Ceci est un événement décrivant une évolution territoriale",
  "triples": [
    ["sub1", "rel1", "obj1"],
    ["sub2", "rel2", "obj2"]
  ]
}
```

#### Pour **BERT** :
Format JSON indiquant les entités et les relations :
```json
{
  "sentence": "Le texte de la phrase",
  "entities": [...],
  "relations": [...]
}
```

#### Utilisation

##### Conversion de la vérité terrain (ground truth) vers JSON

Pour générer les fichiers JSONL à partir de `ground_truth.csv`, il faut exécuter le script `main.py`.

Cela produira deux fichiers :

- `complex_ground_truth.jsonl` — une version **complexe** de la vérité terrain
- `simple_ground_truth.jsonl` — une version **simple** de la vérité terrain

Assurez-vous que le fichier `ground_truth.csv` est bien présent dans le répertoire attendu avant d’exécuter le script.

👉 Voir [ground_truth_conversion.md](doc/ground_truth_conversion.md) pour plus de détails sur la conversion.

---

### 3. 📂 Répartition des données

Les données converties sont réparties en trois ensembles :
- **Entraînement**
- **Validation**
- **Test**

---

## 🔀 Pipelines par méthode

### 🧠 Méthode LLM
1. **Création du prompt** : préparation du prompt + ajout des exemples d'entraînement.
2. **Inférence** sur le jeu de test.
3. **Résultats** : sortie au format JSON (liste de triplets par phrase).

### 🤖 Méthode BERT
1. **Fine-tuning** sur le jeu d'entraînement.
2. **Inférence** sur le jeu de test.
3. **Résultats** : sortie au format entités + relations.

---

### ✅ Évaluation

- Adaptation des résultats BERT vers le **format triplet** (identique à LLM).
- Comparaison des deux méthodes.
- **BERT** est utilisé comme **baseline** pour l’évaluation.
- Production de **scores d’évaluation** (précision, rappel, F1, etc.).

---

## 🗺️ Schéma (ASCII)

```
[CSV input]
     |
     v
[Conversion JSON]
     |
     v
[Split train / val / test]
     |
     +------------------------------+
     |                              |
     v                              v
[LLM pipeline]               [BERT pipeline]
  Prompt + exemples            Fine-tuning
        |                           |
        v                           v
[LLM inférence]              [BERT inférence]
        |                           |
        +------------+--------------+
                     |
                     v
             [Adaptation des formats]
                     |
                     v
             [Évaluation & scores]
```

---

## 📁 Structure du dépôt

- `data/` : fichiers CSV et JSON de travail
- `llm/` : gestion des prompts et inférence LLM
- `bert/` : entraînement et inférence avec BERT
- `utils/` : scripts utilitaires (prétraitement, conversion, etc.)
- `doc/` : documentation détaillée

---

## 📌 TODO

- [ ] Ajouter pipeline de post-traitement pour les erreurs LLM
- [ ] Ajouter visualisation interactive des triplets extraits
- [ ] Publier benchmark complet sur différents modèles

---
