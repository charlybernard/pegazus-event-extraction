import file_management as fm
import event_description_generator as edg
import json

# Example usage
in_path = "../data/ground_truth.csv"
simple_out_path = "../data/simple_ground_truth.jsonl"
out_path_complex = "../data/complex_ground_truth.jsonl"
df = fm.read_csv_as_dataframe(in_path, separator='\t')
simple_event_desc, complex_event_desc = edg.create_event_descriptions(df)
fm.write_jsonl(simple_event_desc, simple_out_path)
fm.write_jsonl(complex_event_desc, out_path_complex)