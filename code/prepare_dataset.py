import file_management as fm
import event_description_generator as edg
import split_ground_truth as sgt

# === Paramètres ===
in_path = "../data/ground_truth.csv"
simple_out_path = "../data/simple_ground_truth.jsonl"
complex_out_path = "../data/complex_ground_truth.jsonl"
split_output_dir = "../data/"

# === Étape 1 : Lecture du fichier CSV de vérité terrain ===
# Le séparateur utilisé est la tabulation ('\t')
df = fm.read_csv_as_dataframe(in_path, separator='\t')

# === Étape 2 : Génération des descriptions d'événements ===
# Renvoie deux listes : une version simple et une version complexe
simple_event_desc, complex_event_desc = edg.create_event_descriptions(df)

# === Étape 3 : Écriture des fichiers JSONL ===
fm.write_jsonl(simple_event_desc, simple_out_path)
fm.write_jsonl(complex_event_desc, complex_out_path)

# === Étape 4 : Découpage en ensembles entraînement / validation / test ===
sgt.split_jsonl(complex_out_path, output_dir=split_output_dir, train_ratio=0.8, val_ratio=0.1, test_ratio=0.1)
sgt.split_jsonl(simple_out_path, output_dir=split_output_dir, train_ratio=0.8, val_ratio=0.1, test_ratio=0.1)
