import argparse
import jsonlines
import random

def randomize_lines(input_filename, output_filename):
    # Read input JSONL file
    lines = []
    with jsonlines.open(input_filename, 'r') as reader:
        for line in reader:
            # Delete keys starting with "similarity" or "M_"
            filtered_line = {key: value for key, value in line.items() if not key.startswith('similarity') and not key.startswith('M_')}
            lines.append(filtered_line)

    # Randomize the order of lines
    random.shuffle(lines)

    # Write randomized lines to the output JSONL file
    with jsonlines.open(output_filename, 'w') as writer:
        for line in lines:
            writer.write(line)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Randomize lines in a JSONL file and remove keys starting with "similarity" or "M_"')
    parser.add_argument('input_filename', type=str, help='Input JSONL filename')
    parser.add_argument('output_filename', type=str, help='Output JSONL filename')
    args = parser.parse_args()

    input_filename = args.input_filename
    output_filename = args.output_filename

    randomize_lines(input_filename, output_filename)
