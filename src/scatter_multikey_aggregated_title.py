import argparse
import jsonlines
import matplotlib.pyplot as plt

def make_unix_filename(string):
    # Replace illegal characters with underscores
    legal_chars = '-_.'
    for char in string:
        if not char.isalnum() and char not in legal_chars:
            string = string.replace(char, '_')

    return string


def create_scatter_plots(input_filename, keys, title, xaxis, yaxis):

    filename = "plots/" + make_unix_filename(title)

    # Pair up keys
    pairs_of_keys = [(keys[i], keys[i+1]) for i in range(0, len(keys), 2)]

    # Initialize empty lists to store values for each pair of keys
    values = {'x': [], 'y': []}

    # Read data from the input JSONL file
    with jsonlines.open(input_filename, 'r') as reader:
        for line in reader:
            for pair in pairs_of_keys:
                x_key, y_key = pair
                if x_key in line and y_key in line:
                    x_value = line[x_key]
                    y_value = line[y_key]
                    values['x'].append(x_value)
                    values['y'].append(y_value)

    # Create scatter plots for each pair of keys
    x_values = values['x']
    y_values = values['y']
    plt.scatter(x_values, y_values, label=f'{pair[0]} vs {pair[1]}')

    # Add labels and title
    plt.xlabel(xaxis)
    plt.ylabel(yaxis)
    plt.title(title)
    plt.legend()
    plt.grid(True)
    plt.savefig(filename)
    plt.close()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Create scatter plots for pairs of keys in a JSONL file')
    parser.add_argument('input_file', type=str, help='Input JSONL filename')
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

    print(len(keys))

    create_scatter_plots(input_filename, keys, title, xaxis, yaxis)
