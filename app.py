import os
from os.path import join, dirname
from dotenv import load_dotenv
dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

if os.environ.get('JAWSDB_URL'):
    sqlURL = os.environ.get('JAWSDB_URL')

if os.getenv('JAWSDB_URL'):
    sqlURL = os.getenv('JAWSDB_URL')

from flask import Flask, render_template, request, redirect

from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import requests

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = sqlURL

db = SQLAlchemy(app)

SQLALCHEMY_TRACK_MODIFICATIONS = False
class Grocery_DB(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False,
                           default=datetime.utcnow)

    def __repr__(self):
        return '<Grocery_DB %r>' % self.name


@app.route('/json',methods=['GET'])
def json():

    return requests.get('https://jsonplaceholder.typicode.com/todos/1').json()


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        name = request.form['name']
        new_stuff = Grocery_DB(name=name)

        try:
            db.session.add(new_stuff)
            db.session.commit()
            return redirect('/')
        except:
            return "There was a problem adding new stuff."

    else:
        groceries = Grocery_DB.query.order_by(Grocery_DB.created_at).all()
        return render_template('index.html', groceries=groceries)


@app.route('/delete/<int:id>')
def delete(id):
    grocery = Grocery_DB.query.get_or_404(id)

    try:
        db.session.delete(grocery)
        db.session.commit()
        return redirect('/')
    except:
        return "There was a problem deleting data."


@app.route('/update/<int:id>', methods=['GET', 'POST'])
def update(id):
    grocery = Grocery_DB.query.get_or_404(id)

    if request.method == 'POST':
        grocery.name = request.form['name']

        try:
            db.session.commit()
            return redirect('/')
        except:
            return "There was a problem updating data."

    else:
        title = "Update Data"
        return render_template('update.html', title=title, grocery=grocery)


if __name__ == '__main__':
    app.run(debug=True)
