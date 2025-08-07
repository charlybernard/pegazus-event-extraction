import random
import os

def split_jsonl(file_path, output_dir, train_ratio=0.8, val_ratio=0.1, test_ratio=0.1, seed=42):
    """
    Divise un fichier .jsonl en trois sous-ensembles : entraînement, validation, test.

    Args:
        file_path (str): Chemin du fichier .jsonl d'entrée.
        output_dir (str): Dossier de sortie pour les fichiers divisés.
        train_ratio (float): Ratio pour l'ensemble d'entraînement.
        val_ratio (float): Ratio pour l'ensemble de validation.
        test_ratio (float): Ratio pour l'ensemble de test.
        seed (int): Graine pour le mélange aléatoire.
    """
    assert abs(train_ratio + val_ratio + test_ratio - 1.0) < 1e-6, "Les ratios doivent totaliser 1.0"
    
    with open(file_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    random.seed(seed)
    random.shuffle(lines)

    total = len(lines)
    train_end = int(train_ratio * total)
    val_end = train_end + int(val_ratio * total)

    train_lines = lines[:train_end]
    val_lines = lines[train_end:val_end]
    test_lines = lines[val_end:]

    # Préparer les noms des fichiers de sortie
    base_name = os.path.splitext(os.path.basename(file_path))[0]
    train_file = os.path.join(output_dir, f"{base_name}_train.jsonl")
    val_file = os.path.join(output_dir, f"{base_name}_val.jsonl")
    test_file = os.path.join(output_dir, f"{base_name}_test.jsonl")

    # Écriture des fichiers
    for split_lines, split_file in zip([train_lines, val_lines, test_lines], [train_file, val_file, test_file]):
        with open(split_file, 'w', encoding='utf-8') as f:
            f.writelines(split_lines)

    print(f"Fichier divisé en :\n- {train_file}\n- {val_file}\n- {test_file}")
