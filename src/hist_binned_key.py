import argparse
import jsonlines
import matplotlib.pyplot as plt
import numpy as np

def make_unix_filename(string):
    # Replace illegal characters with underscores
    legal_chars = '-_.'
    for char in string:
        if not char.isalnum() and char not in legal_chars:
            string = string.replace(char, '_')

    return string

def plot_histogram(data, key, title, xaxis, nbins, xlo, xhi):
    filename = "plots/" + make_unix_filename(title)
    bin_edges = np.linspace(xlo, xhi, nbins)
    plt.hist(data, bins=bin_edges, edgecolor='black')
    plt.title(title)
    plt.xlabel(xaxis)
    plt.ylabel('Frequency')
    plt.grid(True)
    plt.savefig(filename)
    plt.close()

def main(input_filename, key, title = "Histogram", xaxis = "Value", bins = 30, xlo = 0.0, xhi = 1.0):
    values = []

    with jsonlines.open(input_filename, 'r') as reader:
        for line in reader:
            if key in line:
                value=line[key]
                if isinstance(value, (int, float)):
                    values.append(value)
                else:
                    values.extend(line[key])

    if values:
        plot_histogram(values, key, title, xaxis, bins, xlo, xhi)
        print(len(values))
    else:
        print(f"No data found for key '{key}' in the input file.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Create a histogram for a key in a JSONL file')
    parser.add_argument('input_file', type=str, help='Input JSONL filename')
    parser.add_argument('key', type=str, help='Key for histogram')
    parser.add_argument('bins', type=int, help='Key for histogram')
    parser.add_argument('xlo', type=float, help='Key for histogram')
    parser.add_argument('xhi', type=float, help='Key for histogram')
    parser.add_argument('title', nargs = "?", type=str, help='Title for histogram')
    parser.add_argument('xaxis', nargs = "?", type=str, help='Label for x-axis')
    args = parser.parse_args()

    input_filename = args.input_file
    key = args.key
    if (args.title):
        title = args.title
    else:
        title = f"Histogram of {key}"

    if (args.xaxis):
        xaxis = args.xaxis
    else:
        xaxis = f"{key}"

    bins = args.bins
    xlo = args.xlo
    xhi = args.xhi

    main(input_filename, key, title, xaxis, bins, xlo, xhi)
