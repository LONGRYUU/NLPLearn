import json
import numpy as np
def main():
    with open('cmrc2018_train.json', "r") as fh:
        data = json.load(fh)
        counter = np.zeros(40)
        for article in data:
            lines = article['context_text'].split(u'\u3002')
            counter[len(lines)] = counter[len(lines)] + 1
        print(counter)
        
def save_data(data):
    with open('../test.json',"w") as fh:
        json.dump(data, fh)


def cut_file():
    with open('../test_eval.json', "r") as fh:
        data = json.load(fh)
        print(data['1'])
        save_data(data['1'])

def printer():
    with open('test.json', "r") as fh:
        data = json.load(fh)
        print(data[0])

def test_traverse():
    a = [1, 2 ,3]
    b = [4, 5, 6]
    c = [7, 8, 9]
    for i, j, k in a, b, c:
        print(i + j + k)


if __name__ == '__main__':
    test_traverse()