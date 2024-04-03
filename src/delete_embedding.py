import argparse
import jsonlines

def remove_embedding_key(input_filename, output_filename):
    with jsonlines.open(input_filename, 'r') as reader:
        with jsonlines.open(output_filename, 'w') as writer:
            for line in reader:
                # Check if "embedding" key exists in the line
                if "embedding" in line:
                    del line["embedding"]  # Remove the "embedding" key
                writer.write(line)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Remove "embedding" key from input JSONL file and write to output JSONL file')
    parser.add_argument('input_file', type=str, help='Input JSONL filename')
    parser.add_argument('output_file', type=str, help='Output JSONL filename')
    args = parser.parse_args()

    input_filename = args.input_file
    output_filename = args.output_file

    remove_embedding_key(input_filename, output_filename)
