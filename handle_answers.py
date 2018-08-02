import numpy as np
from multiprocessing import pool
from multiprocessing.dummy import Pool as ThreadPool
import json

def get_data_from_file(filename):
    with open(filename, "r") as fh:
        data = json.load(fh)
        return data


def get_quesition(uuid, test):
    for article in test:
        for item in article['paragraphs']:
            for qa in item['qas']:
                if qa['id']==uuid:
                    return qa['question']
    return ""

def prepare(test_eval, test, answer_dict):
    for item in answer_dict:
        data = test_eval[item]
        lines = data['context']
        qid = data['uuid']
        question = get_quesition(qid, test)
        return lines,question
