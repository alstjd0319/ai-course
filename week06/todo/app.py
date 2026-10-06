import sqlite3
import os
from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)
DATABASE = 'database.db'

def get_db():
    db = sqlite3.connect(DATABASE)
    db.row_factory = sqlite3.Row
    return db

def init_db():
    if not os.path.exists(DATABASE):
        with app.app_context():
            db = get_db()
            with app.open_resource('schema.sql', mode='r') as f:
                db.executescript(f.read())
            db.commit()

@app.route('/')
def index():
    db = get_db()
    # Show latest first as per Spec #7
    todos = db.execute('SELECT * FROM todo ORDER BY created_at DESC').fetchall()
    return render_template('index.html', todos=todos)

@app.route('/add', methods=['POST'])
def add():
    title = request.form.get('title', '').strip()
    if title:
        db = get_db()
        db.execute('INSERT INTO todo (title) VALUES (?)', (title,))
        db.commit()
    return redirect(url_for('index'))

if __name__ == '__main__':
    init_db()
    app.run(debug=True)
