
stopwords0 = {'which', 'y', 'them', "that'll", 'o', "didn't", 'while', 'further', "hadn't", 'above', "she's", 'or',
              'am', 'doesn', 'this', 'out', 'haven', 'if', 'does', "isn't", 'themselves', 'yours', 'by', "weren't",
              'no', 'shan', 'her', 'himself', 'me', 'up', 'such', 'i', 'mightn', 'be', 'myself', 'those', 'so', 'on',
              'yourself', 'having', 'because', 's', 'into', 'your', 'again', "should've", 'from', 'under', 'that',
              'him', 've', "won't", 'will', 'most', 'each', 'wouldn', 'its', 'have', 'the', 'of', 'until', 'about',
              'here', 'few', 'is', "shan't", 'whom', 'off', 'any', 'not', 'what', 'same', 'you', 'too', "wasn't",
              'were', "you'd", 'below', 'needn', 'to', 'and', 'his', 'with', "needn't", 'yourselves', 'itself',
              'wasn', 'theirs', 'do', 're', 'my', 'aren', 'other', 'our', 'hers', 'through', 'than', 't', 'should',
              'won', 'd', 'nor', 'why', 'there', 'been', 'can', 'm', "couldn't", 'we', 'it', 'only', 'before', 'isn',
              'ain', 'she', 'ourselves', 'during', 'had', 'don', 'herself', "mightn't", 'doing', "you're", "wouldn't",
              'just', "hasn't", 'but', 'more', 'where', 'did', "aren't", 'now', 'has', "mustn't", 'how', 'didn', 'ma',
              'between', 'hasn', "you'll", 'mustn', 'once', 'he', 'll', 'an', 'these', "don't", 'at', "you've",
              'against', 'some', 'who', 'being', 'over', 'their', 'hadn', 'for', 'after', "haven't", 'in', 'when',
              'own', 'a', "doesn't", 'shouldn', 'weren', 'down', 'was', 'very', 'all', 'as', 'are', 'then', "it's",
              'couldn', 'they', 'both', "shouldn't", 'ours'}


def text_to_frequencies(text_arr, freq):
    featureSet = freq.copy()

    for i in range(len(text_arr)-1):
        word = text_arr[i] + '-' + text_arr[i+1]
        # if word not in stopwords:
        featureSet[word] += 1.0

    return featureSet


def main(text):
    vocab = {}

    text_arr = text.split()
    print("Length of text array:", len(text_arr))

    clean_text_array = []

    for i in range(len(text_arr)):
        if text_arr[i] not in stopwords0:
            clean_text_array.append(text_arr[i])

    for i in range(len(clean_text_array)-1):
        word = text_arr[i] + '-' + text_arr[i+1]
        # if word not in stopwords and word not in vocab:
        if word not in vocab:
            vocab[word] = 0.0

    len_vocab = len(vocab)

    featureSet1 = text_to_frequencies(text, vocab)
    n1 = sum(featureSet1.values())

    # newA = dict(Counter(featureSet4).most_common(30))
    # print(newA.keys())

    print(n1)
