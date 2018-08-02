from translate import Translator
from multiprocessing import pool
from multiprocessing.dummy import Pool as ThreadPool
import json
import time

def get_data(path):
	with open(path, 'r') as fh:
		data = json.load(fh)
		return data


def save_data(filename, data):
	with open(filename, 'w') as fh:
		json.dump(data, fh)

def handle(src_line):
    ts = Translator(to_lang="en", from_lang="zh")
    if len(src_line) == 0:
        return ""
    to_line = ts.translate(src_line).replace("&quot;","\"").replace("&#39;", "'")
    return to_line

def handle_dot(line):
    if len(line) == 0:
        return ""
    if line[-1] != '.' and line[-1] != '?' and line[-1] != '!':
        line = line + '.'
    return line

def trans_para(src_lines, src_lang, dst_lang, flag=True):
    threads = 35
    if len(src_lines) < 35:
        threads = len(src_lines)
    pool = ThreadPool(threads)
    to_lines = pool.map(handle, src_lines)
    pool.close()
    pool.join()
    if(flag):
        new_pool = ThreadPool(threads)
        to_lines = new_pool.map(handle_dot, to_lines)
        new_pool.close()
        new_pool.join()
    return to_lines

def trans_serial(line, src_lang, dst_lang):
    ts = Translator(to_lang=dst_lang, from_lang=src_lang)
    to_line = ts.translate(line).replace("&quot;","\"").replace("&#39;", "'")
    return to_line

def to_en(data):
    for j in range(0,len(data)):
        src_lines = data[j]['context_text'].split(u'\u3002')
        data[j]['context_text'] =''.join(trans_para(src_lines, "zh", "en"))
        data[j]['title'] = trans_serial(data[j]['title'], "zh", "en")
        qs = []
        ans = []
        for qa in data[j]['qas']:
            qs.append(qa['query_text'])
            for i in range(0, len(qa['answers'])):
                ans.append(qa['answers'][i])
        qs = trans_para(qs, "zh", "en")
        ans = trans_para(ans, "zh", "en", False)
        for k in range(len(data[j]['qas'])):
            data[j]['qas'][k]['query_text'] = qs[k]
            data[j]['qas'][k]['answers'] = [ans[k]] 
    return data

def get_start():
    pass

def format(src):
    version = "2.0.0"
    data = []
    for article in src:
        context = article['context_text']
        title = article['title']
        qas = []
        for qa in article['qas']:
             question = qa['query_text']
             answers = []
             id = qa['query_id']
             for answer in qa['answers']:
                 #todo
                 #get the start of the answer
                 answers.append({'text':answer, 'answer_start':0})
             qas.append({'question':question, 'id':id, 'answers':answers, 'is_impossible':False})
        paragraphs = []
        paragraphs.append({'qas': qas, 'context':context})
        data.append({'title':title, 'paragraphs':paragraphs})
    result = {'version':version, 'data':data}
    return result

def trans(config):
    train_data = get_data('cmrc2018_train.json')
    trial_data = get_data('cmrc2018_trial.json')
    dev_data = get_data('cmrc2018_dev.json')
    train_data = to_en(train_data)
    trial_data = to_en(trial_data)
    dev_data = to_en(dev_data)
    train_format = format(train_data)
    trial_format = format(trial_data)
    dev_format = format(dev_data)
    save_data(config.train_file, train_format)
    save_data(config.dev_file, dev_format)
    save_data(config.test_file, trial_format)