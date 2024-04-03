#
# For a completely clear start, only texts_to_summarize.txt and texts_to_paraphrase.txt should be present, and no jsonl
#
# Realistically, summaries.jsonl and paraphrases.jsonl makes sense to put in the directory to start
#
# There a few prompt .txt files that make sense
#
# All input jsonl and txt files are in jsonls and txts directories
#
# The pca_transform_matrix.pkl should not be present
#
#
echo "Beginning Final Analysis"
#
#
echo "Cleaning and Restoring Working Directory"
#
./clean_dir.sh
#
# Copy everything into working directory
#
cp src/* .
cp txts/* .
cp jsonls/* .
#
# Generate summaries file 
#
python3 embed_from_text_file_model.py texts_to_summarize.txt texts_to_summarize_embedded.jsonl
python3 delete_embedding.py texts_to_summarize_embedded.jsonl texts_to_summarize.jsonl
#
# Uncomment and load Mixtral to generate summaries anew
#
# python3 generate_summaries_cli.py texts_to_summarize.jsonl summaries.jsonl
#
echo "Summaries complete, Doing PCA Analysis"
#
# Generate PCA analysis
#
python3 pca_vectors.py texts_to_summarize_embedded.jsonl
#
echo "Analyzing Summary Texts"
#
# Analyze summary texts
#
python3 write_summary_cosines.py summaries.jsonl summaries_SQUE.jsonl
#
echo "Generating Summary Text Plots"
#
python3 hist_key.py summaries_SQUE.jsonl similarity_01 'Histogram of First Summary Cosine Similarity' 'Cosine Similarity'
python3 hist_key.py summaries_SQUE.jsonl similarity_12 'Histogram of Second Summary Cosine Similarity' 'Cosine Similarity'
python3 hist_key.py summaries_SQUE.jsonl similarity_23 'Histogram of Third Summary Cosine Similarity' 'Cosine Similarity'

python3 hist_key.py summaries_SQUE.jsonl lratio_01 'Histogram of First Summary to Original Text Length Ratio' 'Token Compression Factor'
python3 hist_key.py summaries_SQUE.jsonl lratio_12 'Histogram of Second Summary to First Summary Length Ratio' 'Token Compression Factor'
python3 hist_key.py summaries_SQUE.jsonl lratio_23 'Histogram of Third Summary to Second Summary' 'Token Compression Factor'

python3 hist_key.py summaries_SQUE.jsonl M_01 'Histogram of First Summary SQUE Metric' 'SQUE Value'
python3 hist_key.py summaries_SQUE.jsonl M_12 'Histogram of Second Summary SQUE Metric' 'SQUE Value'
python3 hist_key.py summaries_SQUE.jsonl M_23 'Histogram of Third Summary SQUE Metric' 'SQUE Value'

python3 hist_key.py summaries_SQUE.jsonl length_0 'Histogram of Original Text Length' 'Token Count'
python3 hist_key.py summaries_SQUE.jsonl length_1 'Histogram of First Summary Length' 'Token Count'
python3 hist_key.py summaries_SQUE.jsonl length_2 'Histogram of Second Summary Length' 'Token Count'
python3 hist_key.py summaries_SQUE.jsonl length_3 'Histogram of Third Summary Length' 'Token Count'
#
echo "Generating Multikey Summary Plots"
#
python3 hist_multikey_title.py summaries_SQUE.jsonl "Histogram of All Summary SQUEs" 'SQUE' M_01 M_02 M_03 M_12 M_13 M_12
python3 hist_multikey_title.py summaries_SQUE.jsonl 'Histogram of All Summary Similarities' 'Cosine Similarity' similarity_01 similarity_02similarity_03 similarity_12 similarity_13 similarity_23 
python3 hist_multikey_title.py summaries_SQUE.jsonl 'Histogram of All Summary Lengths' 'Token Count' length_1 length_2 length_3
python3 hist_multikey_title.py summaries_SQUE.jsonl 'Histogram of All Summary Compressions' 'Compression Factor' lratio_01 lratio_02 lratio_03 lratio_12 lratio_23 lratio_13

python3 hist_multikey_fit_title.py summaries_SQUE.jsonl 'Histogram of All SQUE Values' 'SQUE' M_01 M_02 M_03 M_12 M_13 M_23 > fits/sque_dist_gaussian_fit.txt

python3 scatter_multikey_aggregated_title.py summaries_SQUE.jsonl 'Scatter of SQUE versus Input Length' 'Input Token Count' 'Summary SQUE' length_0 M_01 length_1 M_12 length_2 M_23

python3 trend_multikey_aggregated_title.py summaries_SQUE.jsonl 'Linear Fit of SQUE versus Input Length' 'Input Token Count' 'Summary SQUE' length_0 M_01 length_1 M_12 length_2 M_23 > fits/linear_fit_SQUE_trend.txt
#
echo "Creating Randomly-Paired Texts"
#
# Create and analyze randomly mixed summary sets
#
python3 randomize_summaries.py summaries.jsonl summaries_mixed.jsonl
#
echo "Analyzing Randomly-Paired Texts"
#
python3 write_summary_cosines.py summaries_mixed.jsonl summaries_mixed_SQUE.jsonl
#
echo "Creating Randomly-Paired Text Plots"
#
python3 hist_key.py summaries_mixed_SQUE.jsonl similarity_01 'Histogram of First Random Summary Cosine Similarity' 'Cosine Similarity'
python3 hist_key.py summaries_mixed_SQUE.jsonl similarity_12 'Histogram of Second Random Summary Cosine Similarity' 'Cosine Similarity'
python3 hist_key.py summaries_mixed_SQUE.jsonl similarity_23 'Histogram of Third Random Summary Cosine Similarity' 'Cosine Similarity'

python3 hist_key.py summaries_mixed_SQUE.jsonl M_01 'Histogram of First Random Summary SQUE Metric' 'SQUE Value'
python3 hist_key.py summaries_mixed_SQUE.jsonl M_12 'Histogram of Second Random Summary SQUE Metric' 'SQUE Value'
python3 hist_key.py summaries_mixed_SQUE.jsonl M_23 'Histogram of Third Random Summary SQUE Metric' 'SQUE Value'

python3 hist_multikey_fit_title.py summaries_mixed_SQUE.jsonl 'Histogram of All Random Summary SQUE Values' 'SQUE' M_01 M_02 M_03 M_12 M_13 M_23 > fits/sque_random_dist_gaussian_fit.txt
#
#
echo "Paraphrase data"
#
#
# Analyze paraphrase texts
#
#
echo "Analyzing Paraphrase Data"
#
python3 create_norm_length_arrays.py paraphrases.jsonl paraphrases_length.jsonl
#
echo "Creating Paraphrase Plots"
#
#
# Cosine verses normalized length
#
python3 plot_tkl_cos.py paraphrases_length.jsonl
python3 plot_tkl_cov.py paraphrases_length.jsonl
#
# Histogram of cosine.  "Not Last" because the last is identical.
#
python3 hist_key_notlast.py paraphrases_length.jsonl ecosine 'Histogram of Paraphrase Cosine Similarity' 'Cosine Similarity'
python3 hist_key_notlast.py paraphrases_length.jsonl tokenlength 'Histogram of Paraphrase Token Length' 'Token Length'
