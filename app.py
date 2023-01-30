import csv

from flask import Flask, jsonify
from flask import render_template
from flask import request
import datetime

app = Flask(__name__)


results = []

with open('C:/Users/Travis/PycharmProjects/HelloWorld/CSV/UserInformation.csv', 'rt', newline='') as file:
    reader = csv.reader(file)
    for row in reader:
        # process the row
        results.append({
            'firstname': row[1],
            'profession': row[4],
            'dateCreated': row[5],
        })


@app.route('/', methods=['GET', 'POST'])
def root():
    if request.method == 'GET':
        return render_template('home.html')
    elif request.method == 'POST':
        results = []

        user_csv = request.form.get('user_csv').split('\n')
        lines = [line for line in user_csv if line.strip()]
        headers = lines[0].split(',')
        rows = [row.split(',') for row in lines[1:]]

        for row in rows:
            result = {}
            for i, header in enumerate(headers):
                result[header] = row[i]
            results.append(result)

        return render_template('home.html', results=results)


def get_user_by_id(user_id):
    with open('C:/Users/Travis/PycharmProjects/HelloWorld/CSV/UserInformation.csv', 'r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            if row['id'] == str(user_id):
                return row
    return None


@app.route('/users/<int:user_id>', methods=['GET'])
def user(user_id):
    user = get_user_by_id(user_id)
    if not user:
        return jsonify({'error': 'user not found'}), 404
    return jsonify(user), 200


@app.route('/profession/<string:profession>', methods=['GET'])
def profession(profession):
    results = []

    with open('C:/Users/Travis/PycharmProjects/HelloWorld/CSV/UserInformation.csv', 'rt', newline='') as file:
        reader = csv.reader(file)
        header = next(reader)
        for row in reader:
            if row[4] == profession:
                results.append(row)

    return render_template('profession.html', header=header, results=results)


@app.route("/users/<start_date>/<end_date>")
def users(start_date, end_date):
    with open("C:/Users/Travis/PycharmProjects/HelloWorld/CSV/UserInformation.csv", "r") as f:
        reader = csv.DictReader(f)
        users = [row for row in reader if start_date <= row["dateCreated"] <= end_date]
    return render_template("users.html", users=users)


@app.route("/country/<country_name>")
def get_users_by_country(country_name):
    users = []
    with open("C:/Users/Travis/PycharmProjects/HelloWorld/CSV/UserInformation.csv", "r") as file:
        reader = csv.DictReader(file)
        for row in reader:
            if row["country"] == country_name:
                users.append(row)
    return render_template("users.html", users=users)


if __name__ == '__main__':
    app.run(debug=True)
