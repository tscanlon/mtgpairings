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

def connect_db():
    return sqlite3.connect(app.config['DATABASE'])

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = connect_db()
    return db

def query_db(query, args=(), one=False):
    cur = get_db().execute(query, args)
    rv = cur.fetchall()
    cur.close()
    return (rv[0] if rv else None) if one else rv

@app.route('/')
def show_event_form():
    query = 'select id, event_name, mtg_format from events order by id desc'
    events = [dict(event_id=row[0], event_name=row[1], mtg_format=row[2]) for row in query_db(query)]
    return render_template('events.html', events=events)

@app.route('/event/<int:event_id>', methods=['GET', 'POST'])
def show_event(event_id):
    if request.method == 'POST':
        query = 'insert into rounds (round_number, event_id, pairings) values (?, ?, ?)'
        args = [request.form['round_number'], request.form['event_id'], request.form['pairings']]
        query_db(query, args)
        flash('Added round %s' % request.form['round_number'])
    # query = 'select event_name, mtg_format from events where id=?'
    query = ('select events.name, events.format, '
             'rounds.id, rounds.number '
             'from events where events.id=? '
             'inner join rounds on events.id=rounds.event_id;')
    row = query_db(query, args=[event_id], one=True)
    event = dict(event_id=event_id, event_name=row[0], mtg_format=row[1])
    return render_template('show_event.html', event=event)

@app.route('/add_round', methods=['POST'])
def add_round():
    flash('added a round')
    return redirect(url_for('show_event_form'))

@app.route('/add_event', methods=['POST'])
def add_event():
    query = 'insert into events (event_name, mtg_format) values (?, ?)'
    args = [request.form['event_name'], request.form['mtg_format']]
    query_db(query, args)
    flash('New event was successfully created')
    return redirect(url_for('show_event_form'))

if __name__ == '__main__':
    app.run(host='0.0.0.0')
