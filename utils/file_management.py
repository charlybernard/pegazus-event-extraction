import os
import json
import csv
from uuid import uuid4
import pandas as pd

def read_file(filename:str, split_lines=False):
    file = open(filename, "r")
    file_content = file.read()
    if split_lines:
        file_content = file_content.split("\n")
    file.close()
    return file_content

def read_json_file(filename:str):
    file = open(filename)
    data = json.load(file)
    file.close()
    return data

def write_file(content:str,filename:str):
    file = open(filename, "w")
    file.write(content)
    file.close()

def read_csv_as_dataframe(file_path, separator=','):
    """
    Lit un fichier CSV et retourne un DataFrame Pandas.

    Paramètres :
    ----------
    file_path : str
        Le chemin complet ou relatif vers le fichier CSV à lire.
    separator : str, optionnel (par défaut = ',')
        Le séparateur utilisé dans le fichier CSV (ex. ',' pour les fichiers CSV classiques, ';' pour les fichiers Excel exportés en CSV).

    Retourne :
    -------
    pd.DataFrame ou None
        Le DataFrame contenant les données du fichier CSV si la lecture réussit, sinon None en cas d'erreur.
    """

    try:
        # Lecture du fichier CSV avec le séparateur spécifié et l'encodage UTF-8
        df = pd.read_csv(file_path, sep=separator, encoding='utf-8')
        return df
    except Exception as e:
        # Affiche un message d'erreur si la lecture échoue
        print(f"Erreur lors de la lecture du fichier CSV : {e}")
        return None
    
def write_jsonl(data, filename):
    """
    Écrit une liste de dictionnaires dans un fichier JSONL.

    Args:
        data (list): Liste de dictionnaires à écrire.
        filename (str): Chemin du fichier de sortie (ex: 'output.jsonl').
    """
    with open(filename, 'w', encoding='utf-8') as f:
        for item in data:
            json.dump(item, f, ensure_ascii=False)
            f.write('\n')

def create_folder_if_not_exists(folder:str):
    if not os.path.exists(folder):
        os.makedirs(folder)

def remove_folder_if_exists(folder:str):
    if os.path.exists(folder):
        remove_folder(folder)

def remove_folder(folder:str):
    for e in os.listdir(folder):
        abspath_e = os.path.join(folder, e)
        print(abspath_e)
        if os.path.isfile(abspath_e):
            remove_file_if_exists(abspath_e)
        elif os.path.isdir(abspath_e):
            remove_folder(e)
        else:
            print(e)

    os.rmdir(folder)
        
def remove_file_if_exists(filename:str):
    if os.path.exists(filename):
        os.remove(filename)