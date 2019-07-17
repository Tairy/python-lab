# encoding:utf-8
from elasticsearch import Elasticsearch
import numpy as np
import tflearn
from tflearn.layers.core import input_data

MODEL_NAME = "log_classify"


def get_tagged_logs():
    query_json = {
        "bool": {
            "must": [
                {
                    "exists": {"field": "tags"}
                }
            ]
        }
    }

    sort_json = [
        {
            "dt": {
                "order": "desc"
            }
        }
    ]

    res = es.search(index="app-server-log-prod-*", body={"query": query_json, "sort": sort_json, "size": 200})

    hits = res['hits']['hits']
    total = res['hits']['total']

    return hits, total


def log_to_vec():
    logs, total = get_tagged_logs()
    dicts = [line.strip() for line in open("dict.txt", 'r')]
    dict_map = {}
    dict_len = len(dicts)
    for i, w in enumerate(dicts):
        dict_map[w] = i

    tags = [line.strip() for line in open("tags.txt", 'r')]
    tags_map = {}
    tags_len = len(tags)

    for i, t in enumerate(tags):
        tags_map[t] = i

    x_batch = np.zeros([total, dict_len])
    y_batch = np.zeros([total, tags_len])
    for idx, log in enumerate(logs):
        tag = log['_source']['tags'][0]
        if tag not in tags_map:
            continue
        tag_vec = np.zeros(tags_len)
        tag_vec[tags_map[tag]] = 1
        y_batch[idx, :] = tag_vec
        word_vec = np.zeros(dict_len)
        for word in log['_source']['em'].strip().split():
            word = word.lower()
            if word in dict_map:
                word_vec[dict_map[word]] = 1
        x_batch[idx, :] = word_vec

    return x_batch, y_batch, dict_len, tags_len, logs, tags


def cnn(dict_len, tags_len):
    network = input_data(shape=[None, dict_len], name='input')
    network = tflearn.fully_connected(network, 32)
    network = tflearn.fully_connected(network, 32)
    network = tflearn.fully_connected(network, tags_len, activation='softmax')
    network = tflearn.regression(network)
    return network


def train():
    x_batch, y_batch, dict_len, tags_len, _, _ = log_to_vec()
    model = tflearn.DNN(cnn(dict_len, tags_len))
    model.fit(x_batch, y_batch, n_epoch=10, batch_size=16, show_metric=True)
    model.save(MODEL_NAME)


def predict():
    x_batch, y_batch, dict_len, tags_len, logs, tags = log_to_vec()
    model_predict = tflearn.DNN(cnn(dict_len, tags_len))
    model_predict.load('/Users/tairy/Documents/Working/python-lab/log-classify/' + MODEL_NAME)
    result = model_predict.predict(x_batch)
    for i in range(result.shape[0]):
        print(logs[i]['_source']['em'])
        print(result[i])
        max_index = np.argmax(result[i])
        print('[+]预测结果:%s' % tags[max_index])
        print(">>>!<<<")


if __name__ == "__main__":
    # train()
    predict()
