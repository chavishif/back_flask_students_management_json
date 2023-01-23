import json
from flask import Flask, request, jsonify
from flask_cors import CORS
import os


app = Flask(__name__)
CORS(app)


# GET method to get all scores or get specific score by name of student
@app.route('/scores', methods=['GET'])
@app.route('/scores/<string:student_name>', methods=['GET'])
def get_scores(student_name=None):
    with open('scores.json', 'r') as f:
        scores = json.load(f)
    if student_name:
        student_scores = [score for score in scores if score['student_name'] == student_name]
        if student_scores:
            return jsonify(student_scores)
        else:
            return jsonify({'message': 'Student score not found'}), 404
    else:
        return jsonify(scores)


# POST method to add new student
@app.route('/students', methods=['POST'])
def add_student():
    try:
        with open('students.json', 'r') as f:
            students = json.load(f)
    except FileNotFoundError:
        students = []

    new_student = request.get_json()
    print(new_student)
    # validate the inputs
    if not new_student['sname'] or not new_student['email']:
        return jsonify({'status': 'error', 'message': 'name and email fields are required'}), 400
    if '@' not in new_student['email']:
        return jsonify({'status': 'error', 'message': 'invalid email format'}), 400
    if any(student['email'] == new_student['email'] for student in students):
        return jsonify({'status': 'error', 'message': 'email already exists'}), 400
    students.append(new_student)
    with open('students.json', 'w') as f:
        json.dump(students, f)
    return jsonify({'status': 'success'})

# POST method to add scores to specific student by student name

@app.route('/scores', methods=['POST'])
def add_score():
    with open('students.json', 'r') as f:
        students = json.load(f)
    try:
        with open('scores.json', 'r') as f:
            scores = json.load(f)
    except FileNotFoundError:
        scores = []
    student_name = request.get_json()['student_name']
    student_exists = False
    for s in students:
        if s['sname'] == student_name:
            student_exists = True
            break
    if student_exists:
        student_scores = None
        new_scores = request.get_json()
        for score in scores:
            if score['student_name'] == student_name:
                student_scores = score
                break
        if student_scores:
            student_scores['math'] = new_scores['math']
            student_scores['english'] = new_scores['english']
            student_scores['computer'] = new_scores['computer']
        else:
            scores.append(new_scores)
        with open('scores.json', 'w') as f:
            json.dump(scores, f)
    else:
        return jsonify({'status': 'error', 'message': 'student not found'}), 400
    return jsonify({'status': 'success'})



if __name__ == '__main__':
    with app.app_context():
         app.run(debug=True)
