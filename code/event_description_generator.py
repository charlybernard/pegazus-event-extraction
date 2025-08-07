import pandas as pd
from collections import namedtuple
from typing import Optional, Dict, List
from uuid import uuid4

# Structure de données représentant une ligne d'événement
EventData = namedtuple("EventData", [
    "event_id", "event_label", "time", "line_id",
    "landmark_label", "landmark_type",
    "relatum_label", "relatum_type", "relation_type",
    "change_on", "change_type", "attribute_type",
    "outdates", "makes_effective"
])

def extract_event_data(row: pd.Series) -> EventData:
    """
    Convertit une ligne de DataFrame en EventData.
    """
    return EventData(*(row.get(col) for col in EventData._fields))

def create_dict_triple(*values: str, keys: List[str] = ["sub", "rel", "obj"]) -> Dict[str, str]:
    """
    Crée un dictionnaire triplet à partir de clés personnalisables.
    """
    return dict(zip(keys, values))

def deduplicate_triples(triples: List[Dict], keys: List[str] = ["sub", "rel", "obj"]) -> List[Dict]:
    """
    Supprime les doublons basés sur des clés données.
    """
    seen = set()
    unique = []
    for t in triples:
        key = tuple(t.get(k) for k in keys)
        if key not in seen:
            seen.add(key)
            unique.append(t)
    return unique

def get_change_predicates(change_type: str, change_on: str, attribute_type: Optional[str] = None) -> Optional[Dict[str, str]]:
    """
    Retourne les prédicats à utiliser pour un changement donné.
    """
    rules = [
        ({"changeType": "appearance", "changeOn": "landmark"}, {"change_time": "appearsOn"}),
        ({"changeType": "disappearance", "changeOn": "landmark"}, {"change_time": "disappearsOn"}),
        ({"changeType": "disappearance", "changeOn": "classement"}, {"change_time": "isClassifiedOn"}),
        ({"changeType": "disappearance", "changeOn": "numerotation"}, {"change_time": "isNumberedOn"}),
        ({"changeType": "appearance", "changeOn": "relation"}, {"change_time": "hasAppearedRelationOn"}),
        ({"changeType": "disappearance", "changeOn": "relation"}, {"change_time": "hasDisappearedRelationOn"}),
        ({"changeType": "transition", "changeOn": "attribute", "attribute_type": "name"},
         {"change_time": "hasNameChangeOn", "old_value": "hasOldName", "new_value": "hasNewName"}),
        ({"changeType": "transition", "changeOn": "attribute", "attribute_type": "geometry"},
         {"change_time": "hasGeometryChangeOn", "old_value": "hasOldGeometry", "new_value": "hasNewGeometry"}),
    ]

    for conditions, predicates in rules:
        if all(conditions.get(k) == v for k, v in {"changeType": change_type, "changeOn": change_on, "attribute_type": attribute_type}.items() if k in conditions):
            return predicates
    return None

def create_simple_event_description(event_data: pd.DataFrame) -> Dict[str, any]:
    """
    Génère une description d'événement simple (sans UUIDs).
    """
    triples = []
    event_id, event_label = None, None

    for _, row in event_data.iterrows():
        data = extract_event_data(row)

        event_id = event_id or data.event_id
        event_label = event_label or data.event_label

        if data.landmark_label:
            triples.append(create_dict_triple(data.landmark_label, "isLandmarkType", data.landmark_type))

        if data.relatum_label:
            triples.append(create_dict_triple(data.relatum_label, "isLandmarkType", data.relatum_type))
            if data.relation_type:
                triples.append(create_dict_triple(data.landmark_label, data.relation_type, data.relatum_label))

        time_value = data.time or "noTime"
        predicates = get_change_predicates(data.change_type, data.change_on, data.attribute_type)

        if predicates:
            triples.append(create_dict_triple(data.landmark_label, predicates["change_time"], time_value))
            if data.change_type == "transition" and data.attribute_type:
                if data.outdates and "old_value" in predicates:
                    triples.append(create_dict_triple(data.landmark_label, predicates["old_value"], data.outdates))
                if data.makes_effective and "new_value" in predicates:
                    triples.append(create_dict_triple(data.landmark_label, predicates["new_value"], data.makes_effective))

    return {
        "id": event_id,
        "sent": event_label,
        "triples": deduplicate_triples(triples)
    }

def create_complex_event_description(event_data: pd.DataFrame) -> Dict[str, any]:
    """
    Génère une description d'événement complexe avec UUIDs.
    """
    triples = []
    landmarks, relations = {}, {}
    event_id, event_label = None, None
    event_uuid = f"EV_{uuid4()}"

    for _, row in event_data.iterrows():
        data = extract_event_data(row)
        event_id = event_id or data.event_id
        event_label = event_label or data.event_label

        lm_uuid = landmarks.setdefault(data.landmark_label, f"LM_{uuid4()}")
        triples.append(create_dict_triple(lm_uuid, "isLandmarkType", data.landmark_type))
        triples.append(create_dict_triple(lm_uuid, "label", f'"{data.landmark_label}"@fr'))

        if data.relatum_label:
            rel_uuid = landmarks.setdefault(data.relatum_label, f"LM_{uuid4()}")
            triples.append(create_dict_triple(rel_uuid, "isLandmarkType", data.relatum_type))
            triples.append(create_dict_triple(rel_uuid, "label", f'"{data.relatum_label}"@fr'))

            lr_uuid = f"LR_{uuid4()}"
            triples.append(create_dict_triple(lr_uuid, "isLandmarkRelationType", data.relation_type))
            triples.append(create_dict_triple(lr_uuid, "locatum", lm_uuid))
            triples.append(create_dict_triple(lr_uuid, "relatum", rel_uuid))

        if data.change_type and data.change_on:
            cg_uuid = f"CG_{uuid4()}"
            triples.append(create_dict_triple(cg_uuid, "isChangeType", data.change_type))
            triples.append(create_dict_triple(cg_uuid, "dependsOn", event_uuid))

            if data.change_on == "landmark":
                triples.append(create_dict_triple(cg_uuid, "appliedOn", lm_uuid))
            elif data.change_on == "relation":
                triples.append(create_dict_triple(cg_uuid, "appliedOn", lr_uuid))
            elif data.change_on == "attribute":
                attr_uuid = f"ATTR_{uuid4()}"
                triples.append(create_dict_triple(attr_uuid, "isAttributeType", data.attribute_type))
                triples.append(create_dict_triple(cg_uuid, "appliedOn", attr_uuid))
                triples.append(create_dict_triple(lm_uuid, "hasAttribute", attr_uuid))
                if data.makes_effective:
                    av_uuid = f"AV_{uuid4()}"
                    triples.append(create_dict_triple(attr_uuid, "hasAttributeVersion", av_uuid))
                    triples.append(create_dict_triple(av_uuid, "versionValue", data.makes_effective))
                    triples.append(create_dict_triple(cg_uuid, "makes_effective", av_uuid))
                if data.outdates:
                    av_uuid = f"AV_{uuid4()}"
                    triples.append(create_dict_triple(attr_uuid, "hasAttributeVersion", av_uuid))
                    triples.append(create_dict_triple(av_uuid, "versionValue", data.outdates))
                    triples.append(create_dict_triple(cg_uuid, "outdates", av_uuid))

    return {
        "id": event_id,
        "sent": event_label,
        "triples": triples
    }

def create_event_descriptions(df: pd.DataFrame) -> List[Dict[str, any]]:
    """
    Génère les descriptions simples et complexes de tous les événements dans un DataFrame.

    Returns
    -------
    tuple: (List[Dict], List[Dict])
        Liste de descriptions simples, Liste de descriptions complexes
    """
    df = df.where(pd.notna(df), None)
    grouped = df.groupby("event")
    return [create_simple_event_description(group) for _, group in grouped], \
           [create_complex_event_description(group) for _, group in grouped]
