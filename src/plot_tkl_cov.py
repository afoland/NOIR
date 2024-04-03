import json
import matplotlib.pyplot as plt
import sys
import numpy as np

def calc_corr(counts, vectors):
    # Assuming 'counts' and 'vectors' are your lists of counts and vectors respectively
    # Your list of counts
    # Your list of vectors, where each vector is a list of components
    # Convert lists to NumPy arrays for easier computation
    counts_array = np.array(counts)
    vectors_array = np.array(vectors)

    # Calculate the correlation between counts and each individual component of the vectors
    correlations = []

    for i in range(vectors_array.shape[1]):
        component = vectors_array[:, i]
        correlation = np.corrcoef(counts_array, component)[0, 1]
        correlations.append(correlation)

    # 'correlations' now contains the correlation between counts and each individual component of the vectors
    return correlations


def process_jsonl(jsonl_file):
    tkl_list = []
    cos_list = []
    vector_list = []
    with open(jsonl_file, 'r') as file:
        for line in file:
            data = json.loads(line)
            tkl_list.extend(data.get('normtokenlength', []))
            cos_list.extend(data.get('ecosine', []))
            vectors = data["embedding"]
    # Append each unpacked vector to the list
            for vector in vectors:
                vector_list.append(vector)
    return tkl_list, cos_list, vector_list


def plot_corr(correlations):
# Assuming 'correlations' is your list of correlations calculated previously

# Create an array of component indices
    component_indices = np.arange(len(correlations))

    # Plot the correlations
    plt.figure(figsize=(8, 6))
    plt.plot(component_indices, correlations, marker='o', linestyle='-')
    plt.xlabel('Component Index')
    plt.ylabel('Correlation')
    plt.title('Correlation between Counts and Vector Components')
    plt.grid(True)
    plt.savefig("plots/tkl_cov.png")
    plt.close()  # Close the plot window automatically

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python script.py <input_jsonl_file>")
        sys.exit(1)

    jsonl_file = sys.argv[1]
    tkl_list, cos_list, vector_list = process_jsonl(jsonl_file)
    corr_list = calc_corr(tkl_list, vector_list) 
#    plot_scatter(tkl_list, cos_list)
    plot_corr(corr_list)
