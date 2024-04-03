import argparse
import jsonlines
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit

def make_unix_filename(string):
     # Replace illegal characters with underscores
     legal_chars = '-_.'
     for char in string:
         if not char.isalnum() and char not in legal_chars:
             string = string.replace(char, '_')

     return string


def linear_fit(x, m, c):
    return m * x + c

def chi_squared(observed, expected, errors):
    residuals = (observed - expected) / errors
    return np.sum(residuals ** 2)

def create_2d_scatter_plot(input_filename, keys, title, xaxis, yaxis, xbins, xlo, xhi, ybins, ylo, yhi):

    filename = "plots/" + make_unix_filename(title)

    if len(keys) % 2 != 0:
        raise ValueError("Number of keys must be even for pairing")

    # Pair up keys
    pairs_of_keys = [(keys[i], keys[i+1]) for i in range(0, len(keys), 2)]

    plt.figure(figsize=(10, 8))

    x_values = []
    y_values = []


    for pair in pairs_of_keys:
        # Read data from the input JSONL file
        with jsonlines.open(input_filename, 'r') as reader:
            for line in reader:
                if pair[0] in line and pair[1] in line:
                    x_values.append(line[pair[0]])
                    y_values.append(line[pair[1]])

    # Convert lists to numpy arrays
    x_values = np.array(x_values)
    y_values = np.array(y_values)

    # Create 2D histogram
    heatmap, xedges, yedges = np.histogram2d(x_values, y_values, bins=20)

    # Create 2D histogram with specified bin edges
    x_bin_edges = np.linspace(xlo, xhi, xbins)
    y_bin_edges = np.linspace(ylo, yhi, ybins)
    heatmap, xedges, yedges = np.histogram2d(x_values, y_values, bins=[x_bin_edges, y_bin_edges])


    # Calculate average Y values in each X bin
    y_avg = []
    y_std = []
    y_err = []
    for i in range(len(xedges) - 1):
        mask = np.logical_and(x_values >= xedges[i], x_values < xedges[i + 1])
        y_avg.append(np.mean(y_values[mask]))
        y_std.append(np.std(y_values[mask]))
        y_err.append(np.std(y_values[mask]) / np.sqrt(np.sum(mask)))

    x_centers = 0.5 * (xedges[:-1] + xedges[1:])
#    popt, pcov = curve_fit(linear_fit, x_centers, y_avg)
    first_bin = 3
    popt, pcov = curve_fit(linear_fit, x_centers[first_bin:], y_avg[first_bin:], sigma = y_err[first_bin:])

    print(popt)
    chi_sq = chi_squared(y_avg[first_bin:], linear_fit(x_centers[first_bin:], *popt), y_err[first_bin:])
    print(f"Chi-squared for {pair[0]} vs {pair[1]}: {chi_sq}")
    print(pcov)

    # Plot the 2D scatter plot with average Y values
    plt.scatter(x_values, y_values, alpha=0.3, label=f'Data Points')
    plt.xlim(xlo,xhi)
    plt.ylim(ylo,yhi)


    # Plot the means, error bars, and line fit
    plt.plot(0.5 * (xedges[:-1] + xedges[1:]), y_avg, marker='o', linestyle='-')
    plt.errorbar(x_centers, y_avg, yerr=y_err, fmt='o', label=f'Data Averages')
    plt.plot(x_centers, linear_fit(x_centers, *popt), color='red', linestyle='-', label='Line Fit')

    plt.xlabel(xaxis)
    plt.ylabel(yaxis)
    plt.title(title)
    plt.legend()
    plt.grid(True)
    plt.savefig(filename)
    plt.close()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Create a 2D scatter plot with average Y values in each X bin')
    parser.add_argument('input_file', type=str, help='Input JSONL filename')
    parser.add_argument('xbins', type=int, help='Key for histogram')
    parser.add_argument('xlo', type=float, help='Key for histogram')
    parser.add_argument('xhi', type=float, help='Key for histogram')
    parser.add_argument('ybins', type=int, help='Key for histogram')
    parser.add_argument('ylo', type=float, help='Key for histogram')
    parser.add_argument('yhi', type=float, help='Key for histogram')
    parser.add_argument('title', type=str, help='Input JSONL filename')
    parser.add_argument('xaxis', type=str, help='Input JSONL filename')
    parser.add_argument('yaxis', type=str, help='Input JSONL filename')
    parser.add_argument('keys', nargs='+', type=str, help='List of keys to pair up (must be even number of keys)')
    args = parser.parse_args()

    input_filename = args.input_file
    keys = args.keys
    title = args.title
    xaxis = args.xaxis
    yaxis = args.yaxis

    xbins = args.xbins
    xlo = args.xlo
    xhi = args.xhi

    ybins = args.ybins
    ylo = args.ylo
    yhi = args.yhi


    create_2d_scatter_plot(input_filename, keys, title, xaxis, yaxis, xbins, xlo, xhi, ybins, ylo, yhi)
