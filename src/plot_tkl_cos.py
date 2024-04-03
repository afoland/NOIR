import json
import matplotlib.pyplot as plt
import sys

def process_jsonl(jsonl_file):
    tkl_list = []
    cos_list = []
    with open(jsonl_file, 'r') as file:
        for line in file:
            data = json.loads(line)
            tkl_list.extend(data.get('normtokenlength', []))
            cos_list.extend(data.get('ecosine', []))
    return tkl_list, cos_list

def plot_scatter(tkl_list, cos_list):
    plt.scatter(tkl_list, cos_list,s=3,linewidth=0,marker="o")
    plt.xlabel('TKL')
    plt.ylabel('Cos')
    plt.title('TKL vs. Cos Scatter Plot')
    plt.savefig("plots/tkl_cos.png")
    plt.close()  # Close the plot window automatically

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python script.py <input_jsonl_file>")
        sys.exit(1)

    jsonl_file = sys.argv[1]
    tkl_list, cos_list = process_jsonl(jsonl_file)
    plot_scatter(tkl_list, cos_list)
