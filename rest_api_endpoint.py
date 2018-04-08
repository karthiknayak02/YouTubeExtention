from flask import Flask, jsonify, request, abort, make_response
import re_structure
import spacy

nlp = spacy.load("en")

app = Flask(__name__)
result_payload = []

@app.errorhandler(404)
def not_found(error):
	return make_response(jsonify({'error': 'Not found'}), 404)


@app.route('/todo/api/v1.0/tasks/1', methods=['GET'])
def get_task():

	print("hi this is result payload", result_payload)
	print("hi this is result payload", result_payload[-1])
	return result_payload[-1]


# @app.route('/todo/api/v1.0/tasks/ready', methods=['GET'])
# def get_normal_task():
# 	return jsonify(ready_flag)

@app.route('/todo/api/v1.0/tasks', methods=['POST'])
def get_keywords_topic():
	print(request.method)

	yt_link = request.json
	print("youtube_link: ", yt_link['url'])
	result = re_structure.main(nlp, "no", yt_link['url'])
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
		


if __name__ == "__main__":
	app.run()
 
def main():
 
 
    app.run(debug=True)
 
    return
 
main()