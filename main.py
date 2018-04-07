def generate_url(video_url):
    video_url_split = video_url.split("v=")
    if len(video_url_split) == 2:
        subtitle_id = video_url_split[1]
        return "http://video.google.com/timedtext?lang=en&v=" + subtitle_id
    else:
        return -1

def main():
    print(generate_url("https://www.youtube.com/watch?v=E8RrVitzI9I"))

if __name__ == "__main__":
    main()