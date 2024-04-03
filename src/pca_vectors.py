import pickle
import sys
import json
import numpy as np
import matplotlib.pyplot as plt
from sklearn.decomposition import PCA

def perform_pca(vectors):
    """Perform Principal Component Analysis (PCA) on the input vectors."""
    pca = PCA()
    pca.fit(vectors)
    principal_components = pca.transform(vectors)
    with open('pca_transform_matrix.pkl', 'wb') as f:
        pickle.dump(pca, f)
    return principal_components, pca.explained_variance_ratio_

def read_jsonl_file(jsonl_file):
    """Read the JSONL file and extract embeddings."""
    embeddings = []

    with open(jsonl_file, 'r') as file:
        for line in file:
            data = json.loads(line)
            embedding = data.get('embedding')
            if embedding:
                embeddings.append(embedding)

    return embeddings

def write_new_jsonl_with_pca(jsonl_file, pca_embeddings):
    """Write a new JSONL file with PCA embeddings."""
    output_file = jsonl_file.replace('.jsonl', '_pca.jsonl')

    with open(output_file, 'w') as file:
        with open(jsonl_file, 'r') as infile:
            for idx, line in enumerate(infile):
                data = json.loads(line)
                data['pca_embedding'] = pca_embeddings[idx].tolist()
                file.write(json.dumps(data) + '\n')

def plot_spectrum(variance_ratio):
    """Plot the spectrum of principal values."""
#    plt.plot(np.cumsum(variance_ratio))
    plt.plot((variance_ratio))
    plt.title('Spectrum of Principal Values')
    plt.xlabel('Number of Principal Components')
    plt.ylabel('Cumulative Variance Ratio')
    plt.grid(True)
    plt.savefig("plots/pca_spectrum.png")
    plt.close()  # Close the plot window automatically

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python script.py <input_jsonl_file>")
        sys.exit(1)

    jsonl_file = sys.argv[1]

    # Read embeddings from JSONL file
    embeddings = read_jsonl_file(jsonl_file)

    # Perform PCA
    pca_embeddings, variance_ratio = perform_pca(embeddings)

    # Write new JSONL file with PCA embeddings
    write_new_jsonl_with_pca(jsonl_file, pca_embeddings)

    # Plot the spectrum of principal values
    plot_spectrum(variance_ratio)

