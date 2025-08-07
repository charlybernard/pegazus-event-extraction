from typing import Dict, List
from datetime import datetime
import re

def date_to_french_natural(date_str):
    """
    Convertit une date ISO partielle ou complète en français naturel.
    Exemples :
    - '1909-01-03' -> '3 janvier 1909'
    - '2023-09' -> 'septembre 2023'
    - '2021' -> '2021'
    """

    date_pattern = r"^\d{4}(-\d{2}(-\d{2})?)?$"  # yyyy or yyyy-mm or yyyy-mm-dd
    if not isinstance(date_str, str) or not re.match(date_pattern, date_str):
        return date_str

    try:
        # Format complet avec jour
        dt = datetime.strptime(date_str, "%Y-%m-%d")
        return dt.strftime("%-d %B %Y")
    except ValueError:
        try:
            # Format année-mois
            dt = datetime.strptime(date_str, "%Y-%m")
            return dt.strftime("%B %Y")
        except ValueError:
            # Format année seule ou autre, on renvoie tel quel
            return date_str

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