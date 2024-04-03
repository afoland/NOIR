import argparse
import jsonlines

def filter_lines(input_filename, output_filename, low_limit, high_limit):
    filtered_lines = []

    # Read input JSONL file
    with jsonlines.open(input_filename, 'r') as reader:
        for line in reader:
            # Check if any of the lratio values are between the low and high limits
            for lratio_key, m_key in [('lratio_01', 'M_01'), ('lratio_12', 'M_12'), ('lratio_23', 'M_23')]:
                if lratio_key in line and low_limit <= line[lratio_key] <= high_limit:
                    filtered_lines.append((line, line[m_key], lratio_key))
                    break

    # Sort filtered lines based on the appropriate M key
    filtered_lines.sort(key=lambda x: x[1])

    # Calculate indices for nearest 10%, 50%, and 90%
    total_lines = len(filtered_lines)
    nearest_10_index = max(int(total_lines * 0.1), 1) - 1
    nearest_50_index = max(int(total_lines * 0.5), 1) - 1
    nearest_90_index = max(int(total_lines * 0.9), 1) - 1

    # Extract lines at the calculated indices
    nearest_10_line, _, nearest_10_key = filtered_lines[nearest_10_index]
    nearest_50_line, _, nearest_50_key = filtered_lines[nearest_50_index]
    nearest_90_line, _, nearest_90_key = filtered_lines[nearest_90_index]

    # Add the key information to the lines
    nearest_10_line['selected_key'] = nearest_10_key
    nearest_50_line['selected_key'] = nearest_50_key
    nearest_90_line['selected_key'] = nearest_90_key

    # Write the extracted lines to the output JSONL file
    with jsonlines.open(output_filename, 'w') as writer:
        writer.write(nearest_10_line)
        writer.write(nearest_50_line)
        writer.write(nearest_90_line)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Filter lines in a JSONL file based on lratio values and find nearest M lines')
    parser.add_argument('input_filename', type=str, help='Input JSONL filename')
    parser.add_argument('output_filename', type=str, help='Output JSONL filename')
    parser.add_argument('low_limit', type=float, help='Low limit for lratio values')
    parser.add_argument('high_limit', type=float, help='High limit for lratio values')
    args = parser.parse_args()

    input_filename = args.input_filename
    output_filename = args.output_filename
    low_limit = args.low_limit
    high_limit = args.high_limit

    filter_lines(input_filename, output_filename, low_limit, high_limit)
