
# 📘 Documentation de Traitement des Événements et Génération de Triplets

Ce document explique comment transformer un fichier CSV contenant des données d’événements historiques en une structure de triplets RDF-like. Le processus est entièrement automatisé via un pipeline Python.

---

## 📝 1. Données en Entrée

Le fichier d'entrée doit être un fichier **CSV** avec les colonnes suivantes :

| Colonne             | Description |
|---------------------|-------------|
| `event`             | ID unique de l'événement |
| `event_label`       | Description textuelle de l’événement |
| `time`              | Date de l’événement (peut être vide) |
| `line_id`           | ID de ligne (ex. `10343_historique`) |
| `landmark_label`    | Nom du repère concerné |
| `landmark_type`     | Type de repère (ex. `rue`, `boulevard`) |
| `relatum_label`     | Nom du repère en relation (s’il y a lieu) |
| `relatum_type`      | Type du relatum |
| `relation_type`     | Type de relation entre repères |
| `change_type`       | Type de changement (`transition`, `appearance`, `disappearance`) |
| `change_on`         | Élément sur lequel porte le changement (`attribute`, `landmark`, `relation`, etc.) |
| `attribute_type`    | Type d’attribut concerné (`geometry`, `name`, etc.) |
| `outdates`          | Ancienne valeur (pour un changement de type `transition`) |
| `makes_effective`   | Nouvelle valeur |

**Exemple d’entrée :**

```
event,event_label,time,line_id,landmark_label,landmark_type,relatum_label,relatum_type,relation_type,change_type,change_on,attribute_type,outdates,makes_effective
96,"rue eugène oudiné || Historique || Précédemment, rue Watt prolongée",,,10605_historique,Rue Eugène Oudiné,rue,,,transition,attribute,name,"rue Watt prolongée","rue de Rigny"
```

---

## 🔄 2. Traitement effectué

Chaque ligne du CSV est convertie en une structure appelée `EventData`, puis transformée en **triplets** sémantiques. Par exemple :

```
Rue Eugène Oudiné -- hasOldName --> rue Watt prolongée
Rue Eugène Oudiné -- hasNewName --> rue de Rigny
Rue Eugène Oudiné -- hasNameChangeOn --> noTime
```

---

## 📤 3. Données en Sortie

### ➤ Version simple (liste de triplets pour un seul événement)

```json
{
  "id": 96,
  "sent": "rue eugène oudiné || Historique || Précédemment, rue Watt prolongée",
  "triples": [
    {"sub": "Rue Eugène Oudiné", "rel": "hasOldName", "obj": "rue Watt prolongée"},
    {"sub": "Rue Eugène Oudiné", "rel": "hasNewName", "obj": "rue de Rigny"},
    {"sub": "Rue Eugène Oudiné", "rel": "hasNameChangeOn", "obj": "noTime"}
  ]
}
```

---

### ➤ Version complète (plusieurs événements)

```json
[
  {
    "id": 96,
    "sent": "rue eugène oudiné || Historique || Précédemment, rue Watt prolongée",
    "triples": [
      {"sub": "Rue Eugène Oudiné", "rel": "hasOldName", "obj": "rue Watt prolongée"},
      {"sub": "Rue Eugène Oudiné", "rel": "hasNewName", "obj": "rue de Rigny"},
      {"sub": "Rue Eugène Oudiné", "rel": "hasNameChangeOn", "obj": "noTime"}
    ]
  },
  {
    "id": 13,
    "sent": "boulevard de courcelles || Ouverture || Ordonnance du Bureau des finances du 16 janvier 1789",
    "triples": [
      {"sub": "Boulevard de Courcelles", "rel": "hasGeometryChangeOn", "obj": "1789-01-16"}
    ]
  }
]
```

---

## ✅ 4. Dédoublonnage

Les triplets sont automatiquement dédupliqués via leurs valeurs (même si plusieurs lignes du CSV produisent des doublons). Cela garantit que chaque fait est représenté **une seule fois**.

---

## 🚀 5. Utilisation dans un pipeline

Les fonctions principales du code sont :

- `extract_event_data()` : transforme une ligne du CSV en structure `EventData`
- `get_change_predicates()` : mappe les types de changement en relations RDF-like
- `create_event_description()` : génère les triplets pour un événement
- `create_event_descriptions()` : traite tout le DataFrame
- `deduplicate_dicts()` : supprime les doublons dans les listes de dictionnaires (personnalisable par clés)

---

## 🧪 Bonus : Dédoublonnage flexible

```python
deduplicate_dicts(triples, keys=("sub", "rel", "obj"))
```

---

© 2025 – Documentation générée automatiquement.
