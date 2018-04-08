from flask import Flask, jsonify, request, abort, make_response
import re_structure
import spacy

nlp = spacy.load("en")

app = Flask(__name__)


tasks = [
	{
		'id': 1,
		'title': u'Buy groceries',
		'description': u'Milk, Cheese, Pizza, Fruit, Tylenol',
		'done': False
	},
	{
		'id': 2,
		'title': u'Learn Python',
		'description': u'Need to find a good Python tutorial on the web',
		'done': False
	}
]


@app.errorhandler(404)
def not_found(error):
	return make_response(jsonify({'error': 'Not found'}), 404)


@app.route('/todo/api/v1.0/tasks/normal/', methods=['GET'])
def get_task():
	yt_link = request.args.get('link')
	print(yt_link)
	result = re_structure.main(nlp, "no")
	if len(result) == 0:
		abort(404)
	return jsonify(result)


@app.route('/todo/api/v1.0/tasks/backup/', methods=['GET'])
def get_normal_task():
	yt_link = request.args.get('link')
	print(yt_link)
	result = re_structure.main(nlp, "backup")
	task = {i[0]: i[1] for i in result}
	if len(task) == 0:
		abort(404)
	return jsonify(task)


if __name__ == "__main__":
	app.run()