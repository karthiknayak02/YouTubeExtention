import numpy as np
import nltk
import pprint
from math import *

# pprint.pprint()

from collections import Counter


stopwords = {'<eol>-the', 'and-in', '<eol>-if', '<eol>-thou', '<eol>-that', '<eol>-where', '.-<eol>', 'is-not',
             '<eol>-as', '<eol>-and', '<eol>-to', '<eol>-in', '<eol>-who', 'thee-<eol>', '<eol>-we', 'of-the', 'to-the',
             'of-my', '<eol>-so', '<eol>-it', "'-<eol>", 'or-if', 'it-is', "i-'ll", '<eol>-or', '<eol>-which', 'that-i',
             '<eol>-why', 'night-<eol>', "'-the", '<eol>-with', 'time-<eol>', 'to-my', "'d-<eol>", '<eol>-is', 'in-the',
             '<eol>-a', '!-<eol>', 'i-have', '<eol>-for', 'no-more', '<eol>-but', 'the-<eol>', '<eol>-my', 'i-am',
             '<eol>-how', '<eol>-no', '<eol>-till', '?-<eol>', '<eol>-what', '<eol>-by', 'i-will',
             '<eol>-this', '<eol>-i', '<eol>-o'}


def text_to_frequencies(text_arr, freq):
    featureSet = freq.copy()


    for i in range(len(text_arr)-1):
        word = text_arr[i] + '-' + text_arr[i+1]
        # if word not in stopwords:
        featureSet[word] += 1.0

    return featureSet



def main():
    vocab = {}

    len_vocab = 0

    file1 = open("insert location", "r").read().split()


    text_arr = file1
    print(len(text_arr))

    # for i in range(len(text_arr)):
    #     text_arr[i] = ps.stem(text_arr[i])
    #
    # for i in range(len(file1)):
    #     file1[i] = ps.stem(file1[i])
    #
    # for i in range(len(file2)):
    #     file2[i] = ps.stem(file2[i])
    #
    # for i in range(len(file3)):
    #     file3[i] = ps.stem(file3[i])
    #
    # for i in range(len(file4)):
    #     file4[i] = ps.stem(file4[i])


    for i in range(len(text_arr)-1):
        word = text_arr[i] + '-' + text_arr[i+1]
        # if word not in stopwords and word not in vocab:
        if word not in vocab:
            vocab[word] = 0.0

    len_vocab = len(vocab)

    featureSet1 = text_to_frequencies(file1, vocab)
    n1 = sum(featureSet1.values())

    # newA = dict(Counter(featureSet4).most_common(30))
    # print(newA.keys())

    print(n1, n2, n3, n4)



    return


main()
