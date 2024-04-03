import sys
import torch
from transformers import AutoModel, AutoTokenizer
import jsonlines
from sklearn.decomposition import PCA

model_name = "facebook/all-MiniLM-L6-v2"
model_name = "sentence-transformers/all-MiniLM-L6-v2"
#model_name = "andersonbcdefg/bge-small-4096"
model = AutoModel.from_pretrained(model_name)
tokenizer = AutoTokenizer.from_pretrained(model_name)

import numpy as np

def vector_to_hateful_numpy_array_that_I_hate(vector_list):
    # Convert the list into a NumPy array, which I hate, if you hadn't noticed
    vector_array = np.array(vector_list)
    # Reshape the array into a 1D array
    reshaped_array = vector_array.reshape(1,-1)
    return reshaped_array

def embed_string(text, model = model, tokenizer = tokenizer, do_PCA = False, PCA_import = None):
#   PCA_import should be an sklearn.decomposition.PCA object
    input_ids = tokenizer.encode(text, return_tensors='pt', max_length=512, truncation=True)
    with torch.no_grad():
        embedding = model(input_ids).last_hidden_state.mean(dim=1).squeeze().tolist()
    if do_PCA:
        pre_PCA = vector_to_hateful_numpy_array_that_I_hate(embedding)
        post_PCA = PCA_import.transform(pre_PCA)
#       I don't know if I mentioned this but I hate converting back and forth to numpy arrays. 
        post_PCA = post_PCA.reshape(-1)
        embedding = post_PCA.tolist()
#    print(embedding)
    return embedding
