import requests
from bs4 import BeautifulSoup
import html
import spacy
import time
from pprint import pprint
from collections import Counter
import pycurl
from io import BytesIO

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
			  'until', 'up', 'very', 'was', "wasn't", 'we', "we'd", "we'll", 'we\'re', "we've", 'were', "weren't",
			  'what', "what's", 'when', "when's", 'where', "where's", 'which', 'while', 'who', "who's", 'whom', 'why',
			  "why's", 'with', "won't", 'would', "wouldn't", 'you', "you'd", "you'll", "you're", "you've", 'your',
			  'heh', 'um', 'em', 'like', 'yours', 'yourself', 'yourselves', '.', '!', '?', ','}

def generate_url(video_url):
	video_url_split = video_url.split("v=")
	if len(video_url_split) == 2:
		subtitle_id = video_url_split[1]
		return "http://video.google.com/timedtext?lang=en&v=" + subtitle_id + "&track=asr"
	else:
		return -1

def get_body(url):
	buffer = BytesIO()
	c = pycurl.Curl()
	c.setopt(c.URL, url)
	c.setopt(c.WRITEDATA, buffer)
	c.perform()
	c.close()

	body = buffer.getvalue()
	# Body is a byte string.
	# We have to know the encoding in order to print it to a text file
	# such as standard output.
	return body.decode('iso-8859-1')

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
	parsed = []
	counter = 0
	for i in transcript.find_all('text'):
		line = []
		line.append(counter)
		counter += 1
		line.append(float(i['start']))
		line.append(html.unescape(i.text))
		parsed.append(line)
	return parsed


def stop_word_removal(words):
	for word in words[:]:
		if word.lower() in stop_words or word.isnumeric():
			words.remove(word)
	return words


def top_bigrams(nlp, words, ngrams, count):
	weights = {'VERB': 0.6, 'PROPN': 0.8, 'NOUN': 0.3, 'ADP': 0.1, 'ADJ': 0.1}
	pprint(weights)
	bi_list = []
	for i in range(len(words) - ngrams + 1):
		together = ""
		for j in range(ngrams):
			together += words[i+j] + " "
		bi_list.append(together[:-1])

	start_time = time.time()
	d = Counter(bi_list).most_common(count*3)
	n_gram_frequencies = {i[0]: i[1] for i in d}
	for word in n_gram_frequencies.keys():
		tokens = nlp(word)
		n_gram_weight = 0.00001
		for single_token in tokens:
			pos_tag = single_token.pos_
			if pos_tag in weights:
				n_gram_weight += weights[pos_tag]

		n_gram_frequencies[word] *= n_gram_weight
		# print(word, freq)
		# input("buttttttttt")


	top_words =  Counter(n_gram_frequencies).most_common(count)
	print("ngram weight time:", time.time() - start_time)
	return top_words

def get_transcripts(transcript_url):

	headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
	response = requests.get(transcript_url, headers=headers)
	print(response.status_code)
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
		for i in range(len(each) - 1):
			single.append(each[i])
		dick = {}
		for word in each[len(each) - 1].split():
			if word.lower() in dick:
				dick[word.lower()] += 1
			else:
				dick[word.lower()] = 1
		single.append(dick)
		search_ready.append(single)
	return search_ready


def search_words(searchable, words):
	# print(searchable)
	contains = []
	for line in searchable:
		diction = {}
		both = True
		for word in words:
			if word.lower() in line[-1]:
				num = line[-1][word.lower()]
				diction[word] = num
			else:
				both = False
		if both:
			line[-1] = diction
			contains.append(line)
	return contains


def group(contains, tolerance, length):
	if len(contains) == 1:
		return [0]
	# tolerance = length *.01 * percent
	# print("Length:", length, "\tTolerance:", tolerance)
	current = 0
	start_point = [0]
	for i in range(1, len(contains)):
		if contains[i][1] - contains[current][1] > tolerance:
			start_point.append(i)
		current = i
	return start_point


def topics(parsed, topics):
	buttonz = []
	searchable = search_prep(parsed)
	for topic in topics:
		title = ""
		for word in topic:
			title += word + " "
		title = title[:-1]
		button = []
		occurances = search_words(searchable, topic)
		# print("occurances:", occurances)
		if occurances:
			matches = group(occurances, 75, searchable[len(searchable) - 1][0])  # edits sensitivity of clustering
			# print("matches:", matches)
			for i in range(len(matches) - 1):
				start = occurances[matches[i]][1]
				end = parsed[occurances[matches[i + 1] - 1][0] + 1][1]
				instances = matches[i + 1] - matches[i]
				name = [["Start", start], ["End", end], ["Instances", instances]]
				button.append(name)
			start = occurances[matches[len(matches) - 1]][1]
			parsed_index = occurances[len(occurances) - 1][0] + 1
			if len(parsed) == parsed_index:  # handles when last occurance appears in the last frame
				end = parsed[parsed_index - 1][1] + 2.37
			else:
				end = parsed[parsed_index][1]
			instances = len(occurances) - matches[len(matches) - 1]
			name = [["Start", start], ["End", end], ["Instances", instances]]
			button.append(name)
		else:
			print("we're fucked")
		# handle what to do if no matches
		buttonz.append([title, button])
	# print()
	return buttonz

def for_now(fuck_this):
	goddamnit = []
	for fuck in fuck_this:
		topic = fuck[0]
		for each in fuck[1]:
			new = [topic, each[0]]
			each[0] = new
			goddamnit.append(each)
	return goddamnit


def main(nlp, ret_type):

	# # SpaCy model loading <---------------- currently not using
	# start = time.time()
	# nlp = spacy.load("en")
	# print("Model Load time:", time.time() - start)

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
	txt_files = ["timedtext0.xml",
				 "timedtext1.xml",
				 "timedtext2.xml",
				 "timedtext3.xml",
				 "timedtext4.xml",
				 "timedtext5.xml",
				 "timedtext6.xml",
				 "timedtext7.xml",
				 "timedtext8.xml",
				 "timedtext9.xml",
				 "timedtext10.xml",
				 "timedtext11.xml",
				 "timedtext12.xml"]

	for link in works:
		n_start = time.time()

		# Takes in a youtube video link and generates a url link for the transcript api we are using.
		transcript_url = generate_url(link)
		# If the link is successfully generated
		if isinstance(transcript_url, str):

		# Gets the transcript and parses it from an XML to a 2-D list of [[time, duration, text], ...]
			text = get_body(transcript_url)

			final_keywords = []

		# with open(link) as file:
		# 	print("OPERATING ON:", link)
		# 	text = file.read()
			parsed_transcript = parse_xml(text)

			# Iterates through all lines in the video and makes a bag of words.
			words = []
			for line in parsed_transcript:
				new = line[-1].replace("<", " ").replace(">", "").replace("_", " ").replace(".", "").replace(",", "")\
					.replace(":", "").replace("\n", " ").replace("?", " ").replace("!", " ").replace("\"", "")\
					.replace("(", "'").replace(")", " ").replace("’", "'").replace("–", " ")
				# print(new)
				line[-1] = new
				words += line[-1].split()

			clean_words = stop_word_removal(words)

			top = top_bigrams(nlp, clean_words, 2, 10)

			keywords = []

			for bi in top:
				keywords.append(bi[0].split())

			# print(keywords)

			# print("parsed_transcript:", parsed_transcript)

			normal_keywords = topics(parsed_transcript, keywords)
			if ret_type == "normal":
				return_list = normal_keywords
			else:
				return_list = for_now(normal_keywords)

			print("Time: ", time.time() - n_start)
			print("\n\n\n\n\n\n\n")
			task = {}

			for topic in return_list:
				task[topic[0]] = {}
				counter = 0
				for cluster in topic[1]:
					task[topic[0]][counter] = {}
					for item in cluster:
						task[topic[0]][counter][item[0]] = item[1]
					counter += 1

			return task


		# input("~~~~~~~~~DONE WITH THAT LINK~~~~~~~~~~~~")

		# else:
		#     print("Failed to generate url for transcript api.")



if __name__ == "__main__":
	nlp = spacy.load("en")
	pprint(main(nlp, ret_type="normal"))
	# unique_words, word_counts = np.unique(bi_list, return_counts=True)
	# freq_matrix = np.array((unique_words, word_counts)).T
	# print(freq_matrix)
	# start_time = time.time()
	# for single_freq in freq_matrix:
	#     tokens = nlp(str(single_freq[0]))
	#     n_gram_weight = 0.00001
	#     for single_token in tokens:
	#         if single_token.pos_ in weights:
	#             word_weight = weights[single_token.pos_]
	#         else:
	#             word_weight = weights['rest']
	#         # try:
	#         #     word_weight = weights[single_token.pos_]
	#         # except KeyError:
	#         #     word_weight = weights['rest']
	#         n_gram_weight += word_weight
	#     #print(n_gram_weight)
	#     single_freq[1] = int(single_freq[1]) * n_gram_weight
	# freq_matrix.sort(axis=1)
	# print("Ngram weight scoring:", time.time() - start_time )
	# input("hi")
	# n_gram_frequencies = Counter({freq[0]: freq[1] for freq in freq_matrix})