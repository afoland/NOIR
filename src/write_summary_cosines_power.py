import argparse
import jsonlines
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from embed_string_model import *
from api_openai_ooba import *
import pickle

def calculate_cosine_similarity(vector1, vector2):
    # Calculate cosine similarity between two vectors
    return cosine_similarity([vector1], [vector2])[0][0]

def calc_M(lratio,similarity,power):
    if (similarity <= 0):
        return 0
    else:
        return (np.log(lratio) / (-1*abs(np.log(similarity))**power))


def process_jsonl(input_filename, output_filename, power):
    do_PCA = False
    with open('pca_transform_matrix.pkl', 'rb') as f:
        pca_components = pickle.load(f)

    with jsonlines.open(input_filename, 'r') as reader:
        with jsonlines.open(output_filename, 'w') as writer:
            for line in reader:
                # Embed strings
                text_vector = embed_string(line.get('text', ''), do_PCA = do_PCA, PCA_import = pca_components)
                summary1_vector = embed_string(line.get('summary_1', ''), do_PCA = do_PCA, PCA_import = pca_components)
                summary2_vector = embed_string(line.get('summary_2', ''), do_PCA = do_PCA, PCA_import = pca_components)
                summary3_vector = embed_string(line.get('summary_3', ''), do_PCA = do_PCA, PCA_import = pca_components)

                # Calculate cosine similarities
                text_summary1_similarity = calculate_cosine_similarity(text_vector, summary1_vector)
                text_summary2_similarity = calculate_cosine_similarity(text_vector, summary2_vector)
                text_summary3_similarity = calculate_cosine_similarity(text_vector, summary3_vector)
                summary1_summary2_similarity = calculate_cosine_similarity(summary1_vector, summary2_vector)
                summary1_summary3_similarity = calculate_cosine_similarity(summary1_vector, summary3_vector)
                summary2_summary3_similarity = calculate_cosine_similarity(summary2_vector, summary3_vector)

                # Update the line with cosine similarities
                similarity_01 = text_summary1_similarity
                similarity_02 = text_summary2_similarity
                similarity_03 = text_summary3_similarity
                similarity_12 = summary1_summary2_similarity
                similarity_13 = summary1_summary3_similarity
                similarity_23 = summary2_summary3_similarity


                line['similarity_01'] = text_summary1_similarity
                line['similarity_02'] = text_summary2_similarity
                line['similarity_03'] = text_summary3_similarity
                line['similarity_12'] = summary1_summary2_similarity
                line['similarity_13'] = summary1_summary3_similarity
                line['similarity_23'] = summary2_summary3_similarity

                length_0 = count_tokens_tiktoken(line.get('text'))
                length_1 = count_tokens_tiktoken(line.get('summary_1'))
                length_2 = count_tokens_tiktoken(line.get('summary_2'))
                length_3 = count_tokens_tiktoken(line.get('summary_3'))

                line['length_0'] = length_0
                line['length_1'] = length_1
                line['length_2'] = length_2
                line['length_3'] = length_3

                lratio_01 = length_1 / length_0
                lratio_02 = length_2 / length_0
                lratio_03 = length_3 / length_0
                lratio_12 = length_2 / length_1
                lratio_13 = length_3 / length_1
                lratio_23 = length_3 / length_2

                line['lratio_01'] = length_1 / length_0
                line['lratio_02'] = length_2 / length_0
                line['lratio_03'] = length_3 / length_0
                line['lratio_12'] = length_2 / length_1
                line['lratio_13'] = length_3 / length_1
                line['lratio_23'] = length_3 / length_2

                line['M_01'] = calc_M(lratio_01,similarity_01, power)
                line['M_02'] = calc_M(lratio_02,similarity_02, power)
                line['M_03'] = calc_M(lratio_03,similarity_03, power)
                line['M_12'] = calc_M(lratio_12,similarity_12, power)
                line['M_13'] = calc_M(lratio_13,similarity_13, power)
                line['M_23'] = calc_M(lratio_23,similarity_23, power)

                # Write the updated line to the output file
                writer.write(line)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Process JSONL file and calculate cosine similarities')
    parser.add_argument('input_file', type=str, help='Input JSONL filename')
    parser.add_argument('output_file', type=str, help='Output JSONL filename')
    parser.add_argument('power', type=float, help='Output JSONL filename')
    args = parser.parse_args()

    input_filename = args.input_file
    output_filename = args.output_file
    power = args.power

    process_jsonl(input_filename, output_filename, power)
