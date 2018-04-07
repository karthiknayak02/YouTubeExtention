import requests
from pprint import pprint
from bs4 import BeautifulSoup


def generate_url(video_url):
    video_url_split = video_url.split("v=")
    if len(video_url_split) == 2:
        subtitle_id = video_url_split[1]
        return "http://video.google.com/timedtext?lang=en&v=" + subtitle_id

    else:
        return -1


def get_transcripts(transcript_url):
    response = requests.get(transcript_url)

    if response.status_code == 200:
        body = response.text
        if body:
            xml_text = BeautifulSoup(body, 'html.parser')
            transcript = xml_text.transcript
            for i in transcript.find_all('text'):
                print(i)

        else:
            print("This link has no text in it.")
    else:
        print("response code error: ", response.status_code)

def main():
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
        transcript_url = generate_url(link)
        get_transcripts(transcript_url)
        input("~~~~~~~~~DONE WITH THAT LINK~~~~~~~~~~~~")



if __name__ == "__main__":
    main()