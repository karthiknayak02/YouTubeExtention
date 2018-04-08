import requests
from bs4 import BeautifulSoup
import html
import spacy
import time
from pprint import pprint
from collections import Counter

stop_words = {'a', 'about', 'above', 'after', 'again', 'against', 'all', 'am', 'an', 'and', 'any', 'are', "aren't",
              'as', 'at', 'be', 'because', 'been', 'before', 'being', 'below', 'between', 'both', 'but', 'by', "can't",
              'cannot', 'could', "couldn't", 'did', "didn't", 'do', 'does', "doesn't", 'doing', "don't", 'down',
              'during', 'each', 'few', 'for', 'from', 'further', 'had', "hadn't", 'has', "hasn't", 'have', "haven't",
              'having', 'he', "he'd", "he'll", "he's", 'her', 'here', "here's", 'hers', 'herself', 'him', 'himself',
              'his', 'how', "how's", 'i', "i'd", "i'll", "i'm", "i've", 'if', 'in', 'into', 'is', "isn't", 'it', "it's",
              'its', 'itself', "let's", 'me', 'more', 'most', "mustn't", 'my', 'myself', 'no', 'nor', 'not', 'of',
              'off', 'on', 'once', 'only', 'or', 'other', 'ought', 'our', 'ours', 'ourselves', 'out', 'over', 'own',
              'same', "shan't", 'she', "she'd", "she'll", "she's", 'should', "shouldn't", 'so', 'some', 'such', 'than',
              'that', "that's", 'the', 'their', 'theirs', 'them', 'themselves', 'then', 'there', "there's", 'these',
              'they', "they'd", "they'll", "they're", "they've", 'this', 'those', 'through', 'to', 'too', 'under',
              'until', 'up', 'very', 'was', "wasn't", 'we', "we'd", "we'll", "we're", "we've", 'were', "weren't",
              'what', "what's", 'when', "when's", 'where', "where's", 'which', 'while', 'who', "who's", 'whom', 'why',
              "why's", 'with', "won't", 'would', "wouldn't", 'you', "you'd", "you'll", "you're", "you've", 'your',
              'yours', 'yourself', 'yourselves', '.', '!', '?', ','}


def generate_url(video_url):
    video_url_split = video_url.split("v=")
    if len(video_url_split) == 2:
        subtitle_id = video_url_split[1]
        return "http://video.google.com/timedtext?lang=en&v=" + subtitle_id

    else:
        return -1


def get_attributes(body):
    xml_text = BeautifulSoup(body, 'xml')
    transcript = xml_text.transcript
    attributes = []
    for attr in transcript.find('text').attrs:
        attributes.append(attr)
    return attributes


def parse_xml(body):
    xml_text = BeautifulSoup(body, 'xml')
    transcript = xml_text.transcript
    attributes = get_attributes(body)
    parsed = []
    for i in transcript.find_all('text'):
        line = []
        for at in attributes:
            line.append(i[at])
        line.append(html.unescape(i.text))
        parsed.append(line)
    return parsed


def stop_word_removal(words):
    [words.remove(word) for word in words[:] if word in stop_words]
    return words


def top_bigrams(words, ngrams, count):
    bi_list = []
    for i in range(len(words) - ngrams + 1):
        together = ""
        for j in range(ngrams):
            together += words[i+j] + " "
        bi_list.append(together[:-1])
    return Counter(bi_list).most_common(count)


def get_transcripts(transcript_url):
    response = requests.get(transcript_url)

    if response.status_code == 200:
        body = response.text
        if body:
            parse_xml(body)
        else:
            print("This link has no text in it.")
    else:
        print("response code error: ", response.status_code)


def search_prep(parse):
    search_ready = []
    for each in parse:
        single = []
        for i in range(len(each) -1):
            single.append(each[i])
        dick = {}
        for word in each[len(each)-1].split():
            if word.lower() in dick:
                dick[word.lower()] += 1
            else:
                dick[word.lower()] = 1
        single.append(dick)
        search_ready.append(single)
    # pprint(search_ready)


def search_word(searchable):
    contains = []
    # for line in searchable:
    #     for word in line[-1]:




def main():

    # SpaCy model loading <---------------- currently not using
    # start = time.time()
    # nlp = spacy.load("en")
    # print("Model Load time:", start - time.time())

    noworks = ["https://www.youtube.com/watch?v=E8RrVitzI9I"]
    works = ["https://www.youtube.com/watch?v=TUgBd-yK7-4",
                 "https://www.youtube.com/watch?v=TUgBd-yK7-4",
                 "https://www.youtube.com/watch?v=b4k-KPELNcc",
                 "https://www.youtube.com/watch?v=8UhqkX2VAmo",
                 "https://www.youtube.com/watch?v=6oLsJUH1cfU",
                 "https://www.youtube.com/watch?v=fWqKalpYgLo",
                 "https://www.youtube.com/watch?v=t8R_GKS-M2Y",
                 "https://www.youtube.com/watch?v=JrRRvqgYgT0",
                 "https://www.youtube.com/watch?v=g-ONUFFt2qM"]

    for link in works:
        n_start = time.time()

        # # Takes in a youtube video link and generates a url link for the transcript api we are using.
        # transcript_url = generate_url(link)
        # # If the link is successfully generated
        # if isinstance(transcript_url, str):
        #
        # # Gets the transcript and parses it from an XML to a 2-D list of [[time, duration, text], ...]
        # parsed_transcript = get_transcripts(transcript_url)

        with open("timedtext.xml") as file:
            text = file.read()
            parsed_transcript = parse_xml(text)

            # Iterates through all lines in the video and makes a bag of words.
            words = []
            for line in parsed_transcript:
                new = line[-1].replace(".", "").replace(",", "").replace(":", "").replace("\n", " ").replace("?", "")
                # print(new)
                line[-1] = new
                words += line[-1].split()
            # print(words)
            # pprint(parsed_transcript)
            # Keyword extractor. <------- Currently only removes stopwords and punctuation.
            clean_words = stop_word_removal(words)

            [print(i) for i in top_bigrams(clean_words, 2, 10)]

            searchable = search_prep(parsed_transcript)

            print("Time: ", time.time() - n_start)

        input("~~~~~~~~~DONE WITH THAT LINK~~~~~~~~~~~~")

        # else:
        #     print("Failed to generate url for transcript api.")



if __name__ == "__main__":
    main()