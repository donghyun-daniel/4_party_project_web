# -*- coding: utf-8 -*-

import pandas as pd
import torch
from torch.nn import functional as F
from torch.utils.data import DataLoader, Dataset
from transformers import AutoTokenizer, ElectraForSequenceClassification, AdamW
import gc
from sklearn.model_selection import KFold
import numpy as np
import os
from tqdm import tqdm
if torch.cuda.is_available():
    device = torch.device("cuda:0")
else:
    device = torch.device("cpu")

MODEL_NAME = "monologg/koelectra-small-v3-discriminator"
pre_MODEL_NAME = "/home/ubuntu/4_party_project/nlp/test/model/sentiment_model/MODEL_KoELECTRA-small-v3-discriminator__3.pt"
#pre_MODEL_NAME = "model/sentiment_pre/MODEL_KoELECTRA-Small-v3-discriminator__3.pt"
DATA_PATH = "/home/ubuntu/4_party_project/nlp/test/model/keyword_save/"
OUTPUT_PATH = "/home/ubuntu/4_party_project/nlp/test/model/results/"
models_name = [['Final_FastText', 8], ['Final_FastText', 17]]

# naver movie, Hotel, shopping


class NHSDataset(Dataset):
    def __init__(self, csv_file):
        self.dataset = csv_file
        self.tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)

    def __len__(self):
        return len(self.dataset)

    def __getitem__(self, idx):
        row = self.dataset.iloc[idx]
        rawSentenceIdx = row[0]
        text = row[2]
        inputs = self.tokenizer(
            text,
            return_tensors='pt',
            truncation=True,
            max_length=256,
            pad_to_max_length=True,
            add_special_tokens=True
        )
        input_ids = inputs['input_ids'][0]
        attention_mask = inputs['attention_mask'][0]

        return input_ids, attention_mask, text, rawSentenceIdx


def sentimentAnalysis(total_data, categories):
    model = model_setting()
    results = []
    for idx, modelname in enumerate(models_name):
        data = pd.DataFrame(total_data[idx])

        print(data)
        test_dataset = data_load(data)
        category = categories[idx]
        gc.collect()
        torch.cuda.empty_cache()

        result = model_predict(model, test_dataset, category)
        results.append(result)
    return results


def output_save(results, modelname):
    df = pd.DataFrame(results)
    outFileName = OUTPUT_PATH + \
        modelname[0] + '_' + str(modelname[1]) + '_sentiment_results.txt'
    df.columns = ['text', 'category', 'sentiment', 'rawsentenceIdx']
    df.to_csv(outFileName, index=False)


def data_load(category):
    print(category.columns)
    categoryCnt = len(category[1].unique())

    test_dataset = []
    for i in range(categoryCnt):
        tmp = category.groupby(1).get_group(i)
        test_dataset.append(NHSDataset(tmp))
    return test_dataset


def category_name_load(categories):
    category = []
    for item in categories:
        category.append(item[0])
    return category


def model_setting():
    model = ElectraForSequenceClassification.from_pretrained(
        MODEL_NAME).to(device)
    # model.load_state_dict(torch.load(pre_MODEL_NAME))
    model.load_state_dict(torch.load(pre_MODEL_NAME, map_location=device))
    return model


def model_predict(model, test_dataset, category):
    print(category)
    model.eval()
    batch_size = 8
    full_result = []
    for cluster_idx, test_data in enumerate(test_dataset):
        test_loader = DataLoader(test_data, batch_size=batch_size)

        for input_ids_batch, attention_masks_batch, original_text, rawSentenceIdx in tqdm(test_loader):
            y_pred = model(input_ids_batch.to(device),
                           attention_mask=attention_masks_batch.to(device))[0]
            for idx in range(len(y_pred)):
                pred_tensor = F.sigmoid(y_pred[idx])
                flag = np.argmax([pred_tensor[0], pred_tensor[1]])

                tmp = [original_text[idx], category[cluster_idx],
                       flag, rawSentenceIdx[idx].item()]
                full_result.append(tmp)
    return full_result
