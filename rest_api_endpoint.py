from flask import Flask, jsonify, request, abort, make_response
import re_structure
import spacy

nlp = spacy.load("en")

app = Flask(__name__)
result_payload = []
search_payload = []

@app.errorhandler(404)
def not_found(error):
	return make_response(jsonify({'error': 'Not found'}), 404)


@app.route('/todo/api/v1.0/tasks/1', methods=['GET'])
def get_task():

	print("hi this is result payload", result_payload)
	print("hi this is result payload", result_payload[-1])

	return result_payload[-1]


@app.route('/todo/api/v1.0/tasks/3', methods=['GET'])
def get_task_S():

	print("hi this is search payload", search_payload)
	print("hi this is search payload", search_payload[-1])

	return search_payload[-1]

# @app.route('/todo/api/v1.0/tasks/ready', methods=['GET'])
# def get_normal_task():
# 	return jsonify(ready_flag)

@app.route('/todo/api/v1.0/tasks', methods=['POST'])
def get_keywords_topic():
	print(request.method)
	result_payload.clear()
	yt_link = request.json
	print("youtube_link: ", yt_link['url'])
	result = re_structure.main(nlp, ["no"], yt_link['url'])
	# if len(result) == 0:
	# 	abort(404)

	result_payload.append(jsonify(result))
	print("hi this is result payload", result_payload)
	return jsonify({'task': "hi"}), 201

	# 	    # response = jsonify(data)
 #    		# response.status_code = 200 # or 400 or whatever
 #    		# return response

	# 	if len(result_payload) != 0:
	# 		print(jsonify(result_payload[0]))
	# 		return jsonify(result_payload[0])
	# 	else:
	# 		return jsonify({})
	# else:
@app.route('/todo/api/v1.0/tasks/2', methods=['POST'])
def get_keywords_topic_S():
	print(request.method)
	search_payload.clear()
	links = request.json
	print("search_terms: ", links['search'])
	result = re_structure.main(nlp, ["search", [links['search'].split(" ")]], links['url'])

	search_payload.append(jsonify(result))
	print("hi this is search payload", search_payload)
	return jsonify({'task': "hi"}), 201


if __name__ == "__main__":
	app.run()
 
def main():
 
 
    app.run(debug=True)
 
    return
 
main()