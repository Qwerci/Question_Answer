import os
import json
import pandas as pd

corpus_folder = r"C:\Users\Theophilus\Documents\projects\nlp\Question_Answer\Corpus"
output_file = r"C:\Users\Theophilus\Documents\projects\nlp\Question_Answer\docs\passage_metadata.csv"

passages = []
metadata = []
chunks = []
chunk_size = 5
metadata_map = {}  # A dictionary to map metadata to technical.txt files

# Function to extract passages from one technical text file
def extract_passages(path):
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()

    section = content.split("__section__")
    for sec in section:
        paragraphs = sec.split("__paragraph__")
        for paragraph in paragraphs:
            # Remove any extra spaces
            cleaned_para = ' '.join(paragraph.split())
            if cleaned_para:
                passages.append(cleaned_para)

# Extract metadata separately and associate it with the technical.txt file
for filename in os.listdir(corpus_folder):
    if filename.endswith('_Technical.txt'):
        technical_file = os.path.join(corpus_folder, filename)
        metadata_filename = filename.replace('_Technical.txt', '_Metadata.json')
        metadata_file = os.path.join(corpus_folder, metadata_filename)

        # Check if the corresponding metadata file exists before extracting
        if metadata_filename in os.listdir(corpus_folder):
            extract_passages(technical_file)

            # Read contents of metadata file and map it to the technical.txt file
            with open(metadata_file, 'r', encoding='utf-8') as meta_file:
                meta_data = json.load(meta_file)
                metadata_map[technical_file] = meta_data

# Process chunks and associate each chunk with its corresponding metadata
for passage in passages:
    sentences = passage.split('.')
    for i in range(0, len(sentences), chunk_size):
        chunk = '. '.join(sentences[i:i + chunk_size])
        # Get the metadata for the corresponding technical.txt file
        metadata_for_chunk = metadata_map[technical_file]
        chunks.append(chunk)
        metadata.append(metadata_for_chunk)

# Let's create a DataFrame with Passage, their Metadata
df = pd.DataFrame({'Passage': chunks, 'Metadata': metadata})
df.to_csv(output_file, index=False)


# print(len(chunks), len(passages), len(metadata))


