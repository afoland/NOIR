import json
import sys
from process_jsonl_compress3 import process_jsonl

def readwrite_jsonl(input_filename, output_filename):
    with open(input_filename, 'r') as input_file:
        input_data = input_file.readlines()
    
    processed_data = process_jsonl(input_data)
    
    with open(output_filename, 'w') as output_file:
        for item in processed_data:
            output_file.write(json.dumps(item) + '\n')


def process_cli(args):
    if len(args) < 3:
        print("Usage: python script.py input_jsonl_filename output_jsonl_filename")
        return
    
    input_jsonl_filename = args[1]
    output_jsonl_filename = args[2]
    
    readwrite_jsonl(input_jsonl_filename, output_jsonl_filename)


if __name__ == "__main__":
    process_cli(sys.argv)
