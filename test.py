# coding=utf-8
from util import f1_score
import nltk
import nltk.data


def find_context_index(question, answer, contexts):
    context_list = splitSentence(contexts)
    print(context_list)
    print("the len od list is "+len(context_list).__str__())
    sim = 0.0
    qas = answer+" "+question
    for i in range(len(context_list)):
        print("precessing the "+i.__str__()+" th ")
        if sim < f1_score(qas, context_list[i]):
            sim=f1_score(qas, context_list[i])
            index = i
            print("get the best index"+index.__str__())
    print("the best index is:" + index.__str__())
    print("the best context is"+context_list[index])
    return i+1


def splitSentence(paragraph):
    tokenizer = nltk.data.load('tokenizers/punkt/english.pickle')
    sentences = tokenizer.tokenize(paragraph)
    return sentences


if __name__ == "__main__":
    str = "Since I went to school, I have received the education that the new China didn't come easy. There were thousands of soldiers fought for the country's future. They sacrificed their lives. When the first army was built, the future had been seen. So August 1st is The Army Day today, which is to honor the work of the great soldiers."
    find_context_index("There", "thousands", str)
    # para = "this is \"the god's love.\". and we should thank god. am i right."
    # print(splitSentence(para))
