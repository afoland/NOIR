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

def create_histogram(input_filename, keys, title, xaxis):
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
    plt.hist(data, bins=30, edgecolor='black')
    plt.title(title)
    plt.xlabel(xaxis)
    plt.ylabel('Frequency')
    plt.grid(True)
    plt.savefig(filename)
    plt.close()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Plot histogram of values for specified keys in a JSONL file')
    parser.add_argument('input_file', type=str, help='Input JSONL filename')
    parser.add_argument('title', type=str, help='Input JSONL filename')
    parser.add_argument('xaxis', type=str, help='Input JSONL filename')
    parser.add_argument('keys', nargs='+', type=str, help='Keys to histogram (at least one key)')
    args = parser.parse_args()

    input_filename = args.input_file
    keys = args.keys
    title = args.title
    xaxis = args.xaxis

    create_histogram(input_filename, keys, title, xaxis)
