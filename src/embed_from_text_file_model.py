import sys
import torch
from transformers import AutoModel, AutoTokenizer
import jsonlines

def embed_text(text, model, tokenizer):
    input_ids = tokenizer.encode(text, return_tensors='pt', max_length=512, truncation=True)
    with torch.no_grad():
        embeddings = model(input_ids).last_hidden_state.mean(dim=1).squeeze().tolist()
    return embeddings

def process_file(input_file, output_file, model, tokenizer):
    with open(input_file, 'r', encoding='utf-8') as file:
        lines = file.readlines()

    results = []

    for line in lines:
        text = line.strip()
        embeddings = embed_text(text, model, tokenizer)

        result = {
            "text": text,
            "embedding": embeddings
        }

        results.append(result)

    with jsonlines.open(output_file, mode='w') as writer:
        writer.write_all(results)

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python script.py input_file_path output_file_path")
        sys.exit(1)

    input_file_path = sys.argv[1]
    output_file_path = sys.argv[2]

    model_name = "facebook/all-MiniLM-L6-v2"
    model_name = "sentence-transformers/all-MiniLM-L6-v2"
#    model_name = "andersonbcdefg/bge-small-4096"

    model = AutoModel.from_pretrained(model_name)
    tokenizer = AutoTokenizer.from_pretrained(model_name)

    process_file(input_file_path, output_file_path, model, tokenizer)

    print(f"Embeddings written to {output_file_path}")
