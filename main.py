import requests
from pprint import pprint
from bs4 import BeautifulSoup
import html
import spacy
import time
import Naive_bayes


def generate_url(video_url):
    video_url_split = video_url.split("v=")
    if len(video_url_split) == 2:
        subtitle_id = video_url_split[1]
        return "http://video.google.com/timedtext?lang=en&v=" + subtitle_id

    else:
        return -1


def parse_xml(body):
    xml_text = BeautifulSoup(body, 'xml')
    transcript = xml_text.transcript
    parsed = []
    for i in transcript.find_all('text'):
        line = [float(i['start']), float(i['dur']), html.unescape(i.text)]
        parsed.append(line)
    return parsed


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


def normalize_lines(nlp, transcript_text):

    for line in transcript_text:
        #print("Before:", line[2])
        tokens = nlp(line[2])
        split_line = []
        for token in tokens:
            if (not token.is_stop) and (not token.is_punct):
                split_line.append(token.text)
        line[2] = split_line
        #print("After:", line[2])

    return transcript_text


def keyword_extraction(transcript_text):
    transcript_string = ""
    for line in transcript_text:
        for word in line[2]:
            transcript_string += word+" "

    transcript_string.strip()

    Naive_bayes.main(transcript_string)

    #print(transcript_string)

def main():
    start = time.time()
    nlp = spacy.load("en")
    print("Model Load time:", start - time.time())
    for word in nlp.Defaults.stop_words:
        lex = nlp.vocab[word]
        lex.is_stop = True

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
        # transcript_url = generate_url(link)
        # parsed_transcript = get_transcripts(transcript_url)

        with open("timedtext.xml") as file:
            text = file.read()
            parsed_transcript = parse_xml(text)
            transcript_text = normalize_lines(nlp, parsed_transcript)
            keyword_extraction(transcript_text)
            print("Time: ", time.time() - n_start)


        input("~~~~~~~~~DONE WITH THAT LINK~~~~~~~~~~~~")



if __name__ == "__main__":
    main()