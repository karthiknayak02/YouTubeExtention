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
            soup = BeautifulSoup(body, 'html.parser')
            print(soup.prettify())
        else:
            print("This link has no text in it.")
    else:
        print("response code error: ", response.status_code)

def main():
    noworks = "https://www.youtube.com/watch?v=E8RrVitzI9I"
    works = "https://www.youtube.com/watch?v=n3qA8DNc2Ss"

    transcript_url = generate_url(works)
    get_transcripts(transcript_url)



if __name__ == "__main__":
    main()