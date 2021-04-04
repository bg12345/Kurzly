from flask import Flask, request, redirect,jsonify
from flask_sqlalchemy import SQLAlchemy
import random
import string
from flask_cors import CORS
import os

app = Flask(__name__)
CORS(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///urls.db' #os.environ.get('DATABASE_URL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Urls(db.Model):
    id_ = db.Column("id_", db.Integer, primary_key=True)
    long = db.Column("long", db.String())
    short = db.Column("short", db.String(5))

    def __init__(self, long, short):
        self.long = long
        self.short = short

@app.before_first_request
def create_tables():
    db.create_all()

def shorten_url():
    letters = string.ascii_lowercase + string.ascii_uppercase
    while True:
        rand_letters = random.choices(letters, k=5)
        rand_letters = "".join(rand_letters)
        short_url = Urls.query.filter_by(short=rand_letters).first()
        if not short_url:
            return rand_letters

@app.route('/',methods=["POST"])
def main():
    if request.method=="POST":
        url = request.form["url"]
        found_url = Urls.query.filter_by(long=url).first()
        if found_url:
            return jsonify(shorturl="http://127.0.0.1:5000/"+found_url.short)
        else:
            short_url = shorten_url()
            new_url = Urls(url, short_url)
            db.session.add(new_url)
            db.session.commit()
            return jsonify(shorturl="http://127.0.0.1:5000/" + short_url)

@app.route('/<short_url>')
def redirection(short_url):
    long_url = Urls.query.filter_by(short=short_url).first()
    if long_url:
        return redirect(long_url.long)
    else:
        return '<h1>Url doesnt exist</h1>'

if __name__ == '__main__':
    app.run(port=5000, debug=True)
