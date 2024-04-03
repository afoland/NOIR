import argparse
import jsonlines
import random

def process_lines(input_filename, output_filename):
    with jsonlines.open(input_filename, 'r') as reader, jsonlines.open(output_filename, 'w') as writer:
        lines = list(reader)

        for line in lines:
            # Keep the "text" value
            text = line.get("text", "")

            # Randomly select lines for "summary_1", "summary_2", and "summary_3"
            summary_1_line = random.choice([l for l in lines if l["summary_1"] != line["summary_1"]])
            summary_2_line = random.choice([l for l in lines if l["summary_2"] != line["summary_2"] and l["summary_1"] != summary_1_line["summary_1"]])
            summary_3_line = random.choice([l for l in lines if l["summary_3"] != line["summary_3"] and l["summary_1"] != summary_1_line["summary_1"] and l["summary_2"] != summary_2_line["summary_2"]])

            # Replace the values
            line["summary_1"] = summary_1_line["summary_1"]
            line["summary_2"] = summary_2_line["summary_2"]
            line["summary_3"] = summary_3_line["summary_3"]

            # Write the modified line to the output file
            writer.write(line)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Process lines in a JSONL file')
    parser.add_argument('input_file', type=str, help='Input JSONL filename')
    parser.add_argument('output_file', type=str, help='Output JSONL filename')
    args = parser.parse_args()

    input_filename = args.input_file
    output_filename = args.output_file

    process_lines(input_filename, output_filename)
