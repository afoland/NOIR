import argparse
import jsonlines
import matplotlib.pyplot as plt
import numpy as np
from scipy.optimize import curve_fit

def make_unix_filename(string):
    # Replace illegal characters with underscores
    legal_chars = '-_.'
    for char in string:
        if not char.isalnum() and char not in legal_chars:
            string = string.replace(char, '_')

    return string

def gaussian(x, amplitude, mean, stddev):
    return amplitude * np.exp(-((x - mean) / stddev) ** 2 / 2)


def create_histogram(input_filename, keys, title, xaxis, nbins, xlo, xhi):
    data = []

    filename = "plots/" + make_unix_filename(title)

    # Read data from the input JSONL file
    with jsonlines.open(input_filename, 'r') as reader:
        for line in reader:
            # Aggregate values for specified keys
            for key in keys:
                if key in line:
                    value = line[key]
                    if isinstance(value, (int, float)):
                        data.append(value)  # If single value, append directly
                    else:
                        data.extend(value)  # If iterable, extend the list

    # Plot histogram
    bin_edges = np.linspace(xlo, xhi, nbins)
    plt.hist(data, bins=bin_edges, edgecolor='black', density = True)
    plt.title(title)
    plt.xlabel(xaxis)
    plt.ylabel('Frequency')

    # Get histogram values and bin edges
    hist_values, bin_edges = np.histogram(data, bins=bin_edges, density=True)
    bin_centers = 0.5 * (bin_edges[1:] + bin_edges[:-1])

    # Fit Gaussian function
    popt, pcov = curve_fit(gaussian, bin_centers, hist_values, p0=[1, 4.5, 0.4])

    print(popt)
    print(pcov)

    # Plot fitted Gaussian function
    plt.plot(bin_centers, gaussian(bin_centers, *popt), color='red', label='Gaussian fit')
    plt.legend()
    plt.grid(True)
    plt.savefig(filename)
    plt.close()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Plot histogram of values for specified keys in a JSONL file')
    parser.add_argument('input_file', type=str, help='Input JSONL filename')
    parser.add_argument('bins', type=int, help='Key for histogram')
    parser.add_argument('xlo', type=float, help='Key for histogram')
    parser.add_argument('xhi', type=float, help='Key for histogram')
    parser.add_argument('title', type=str, help='Input JSONL filename')
    parser.add_argument('xaxis', type=str, help='Input JSONL filename')
    parser.add_argument('keys', nargs='+', type=str, help='Keys to histogram (at least one key)')
    args = parser.parse_args()

    input_filename = args.input_file
    keys = args.keys
    title = args.title
    xaxis = args.xaxis
    bins = args.bins
    xlo = args.xlo
    xhi = args.xhi


    create_histogram(input_filename, keys, title, xaxis, bins, xlo, xhi)
