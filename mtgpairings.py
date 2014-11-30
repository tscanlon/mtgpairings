import sqlite3
from flask import Flask, request, session, g, redirect, url_for, \
    abort, render_template, flash
from contextlib import closing

# config
DATABASE = 'pairings.db'
DEBUG = True
SECRET_KEY = 'herpderp'
USERNAME = 'admin'
PASSWORD = 'default'

app = Flask(__name__)
app.config.from_object(__name__)

def connect_db():
    return sqlite3.connect(app.config['DATABASE'])

def init_db():
    with closing(connect_db()) as db:
        with app.open_resource('schema.sql', mode='r') as f:
            db.cursor().executescript(f.read())
        db.commit()

@app.before_request
def before_request():
    g.db = connect_db()

@app.teardown_request
def teardown_request(exception):
    db = getattr(g, 'db', None)
    if db is not None:
        db.close()

@app.route('/')
def show_event_form():
    cur = g.db.execute('select id, event_name, mtg_format from events order by id desc')
    events = [dict(event_id=row[0], event_name=row[1], mtg_format=row[2]) for row in cur.fetchall()]
    return render_template('events.html', events=events)

@app.route('/event/<int:event_id>', methods=['GET'])
def show_event(event_id):
    cur = g.db.execute('select event_name, mtg_format from events where id=%d'%event_id)
    event = [dict(event_id=event_id, event_name=row[0], mtg_format=row[1]) for row in cur.fetchall()]
    return render_template('show_event.html', event=event)

@app.route('/add_round', methods=['POST'])
def add_round():
    flash('added a round')
    return redirect(url_for('show_event_form'))

@app.route('/add_event', methods=['POST'])
def add_event():
    g.db.execute('insert into events (event_name, mtg_format) values (?, ?)',
            [request.form['event_name'], request.form['mtg_format']])
    g.db.commit()
    flash('New event was successfully created')
    # url_for('method_name')
    return redirect(url_for('show_event_form'))

if __name__ == '__main__':
    app.run()
