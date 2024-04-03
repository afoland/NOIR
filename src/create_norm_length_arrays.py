from api_openai_ooba import *
import embed_string_model
import pickle
import math


def dot_product(vec1, vec2):
    return sum(x * y for x, y in zip(vec1, vec2))

def magnitude(vec):
    return math.sqrt(sum(x * x for x in vec))

def simple_cosine_similarity(vec1, vec2):
    skip_first = False
    if skip_first:
        vec1[1] = 0
        vec2[1] = 0
    dot_prod = dot_product(vec1, vec2)
    mag1 = magnitude(vec1)
    mag2 = magnitude(vec2)
    if mag1 == 0 or mag2 == 0:
        return 0  # to handle division by zero
    return dot_prod / (mag1 * mag2)

def skip_cosine_similarity(vec1, vec2):
    skip_first = True
    if skip_first:
        vec1[1] = 0
        vec2[1] = 0
    dot_prod = dot_product(vec1, vec2)
    mag1 = magnitude(vec1)
    mag2 = magnitude(vec2)
    if mag1 == 0 or mag2 == 0:
        return 0  # to handle division by zero
    return dot_prod / (mag1 * mag2)


def process_strings(strings, process_string):
    """
    Process a list of strings using a specified function.

    Args:
    strings (list): List of strings to process.
    process_string (function): Function to process each string.

    Returns:
    list: List containing the return values of the processed strings.
    """
    return [process_string(string) for string in strings]

# Example of how to use the function
def example_process_string(string):
    # Example process function that converts a string to uppercase
    return string.upper()

def process_length(string):
    return len(string)

def process_tokenlength(string):
    return count_tokens_tiktoken(string)

def process_embedding(string, do_pca = False, PCA_import = None):
    return embed_string_model.embed_string(string, do_PCA = do_pca, PCA_import = PCA_import)

import json
import sys

def process_jsonl(input_filename, output_filename):
    # Load the transformation matrix using pickle
    with open('pca_transform_matrix.pkl', 'rb') as f:
        pca_components = pickle.load(f)

    with open(input_filename, 'r') as input_file:
        with open(output_filename, 'w') as output_file:
            for line in input_file:
                data = json.loads(line)
                paraphrases = data.get('paraphrases', [])

                lengths = process_strings(paraphrases, process_length)
                data['charlength'] = lengths
                charnorm = int(lengths[-1])
                if (charnorm == 0):
                    charnorm = 1
                normcharlengths = [int(length) / charnorm for length in lengths]
                data['normcharlength'] = normcharlengths

                tkls = process_strings(paraphrases, process_tokenlength)
                data['tokenlength'] = tkls
                tokennorm = int(tkls[-1])
                if (tokennorm == 0):
                    tokennorm = 1
                normtokenlengths = [int(tkl) / tokennorm for tkl in tkls]
                data['normtokenlength'] = normtokenlengths

                embeddings = [process_embedding(paraphrase, False) for paraphrase in paraphrases]
                data['embedding'] = embeddings

                ecosines = [simple_cosine_similarity(embedding, embeddings[-1]) for embedding in embeddings]
                data["ecosine"] = ecosines

                mags = [magnitude(embedding) for embedding in embeddings]
                data["mag"] = mags

                embeddings = [process_embedding(paraphrase, True, pca_components) for paraphrase in paraphrases]
                data['pca_embedding'] = embeddings

                ecosines = [simple_cosine_similarity(embedding, embeddings[-1]) for embedding in embeddings]
                data["pca_ecosine"] = ecosines

                ecosines = [skip_cosine_similarity(embedding, embeddings[-1]) for embedding in embeddings]
                data["pca_skip_ecosine"] = ecosines

                mags = [magnitude(embedding) for embedding in embeddings]
                data["pca_mag"] = mags



                json.dump(data, output_file)
                output_file.write('\n')

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python script.py input_filename output_filename")
        sys.exit(1)
    
    input_filename = sys.argv[1]
    output_filename = sys.argv[2]
    
    process_jsonl(input_filename, output_filename)
