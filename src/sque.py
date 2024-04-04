import sys
import torch
from transformers import AutoModel, AutoTokenizer
import jsonlines
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity

def calculate_cosine_similarity(vector1, vector2):
    # Calculate cosine similarity between two vectors
    return cosine_similarity([vector1], [vector2])[0][0]

def embed_string(text, model, tokenizer):
    input_ids = tokenizer.encode(text, return_tensors='pt', max_length=512, truncation=True)
    with torch.no_grad():
        embedding = model(input_ids).last_hidden_state.mean(dim=1).squeeze().tolist()
    return embedding

def sque(text, summary, embedding_model = "sentence-transformers/all-MiniLM-L6-v2"):
    model = AutoModel.from_pretrained(embedding_model)
    tokenizer = AutoTokenizer.from_pretrained(embedding_model)

    text_embedding = embed_string(text, model, tokenizer)
    summary_embedding = embed_string(summary, model, tokenizer)
    D = calculate_cosine_similarity(text_embedding, summary_embedding)

    text_length = len(tokenizer.encode(text))
    summary_length = len(tokenizer.encode(summary))
    k = summary_length / text_length

    sque_metric = np.log(k) / np.log(D)
    return sque_metric

if __name__ == "__main__":
    # Test the code
    text = "Recently, Malaysia has been making global headlines due to the unexplained disappearance of a passenger jet. Prior to this incident, the nation hadn't experienced such widespread media attention since gaining independence from British rule. Unlike some of its Southeast Asian counterparts, such as Indonesia and the Philippines, Malaysia has avoided significant international scrutiny, partly due to its lack of exposure to large-scale natural disasters. The sudden disappearance of Malaysia Airlines Flight 370 has placed immense pressure on the Malaysian government, revealing potential shortcomings in their response strategy. Criticism has arisen both domestically and internationally, notably from China and Vietnam—countries heavily involved in the ongoing search mission. Furthermore, family members of the passengers have expressed frustration and concern regarding the handling of the situation. Various conflicting statements issued by Malaysian authorities have contributed to the growing dissatisfaction. As most of the plane's passengers were Chinese, mounting tensions between China and Malaysia have resulted from Kuala Lumpur's management of the search operation, particularly after announcing that the aircraft may have veered off course towards the Indian Ocean instead of its previously suspected location in the South China Sea. This revelation led to accusations that valuable time searching the South China Sea had been squandered needlessly, potentially decreasing chances of locating survivors."
    summary = "Malaysia's handling of the mysterious disappearance of a passenger jet faces criticism, revealing possible weaknesses in their response strategy. Family members, China, and Vietnam express concerns over conflicting statements and delayed information. Tension rises as Malaysia revises flight path, suggesting the plane might have deviated towards the Indian Ocean, causing controversy about wasted search efforts in the South China Sea."

    sque_metric = sque(text, summary)

    print(f"The SQUE metric calculated for this text-summary pair is {sque_metric:.2f}")
