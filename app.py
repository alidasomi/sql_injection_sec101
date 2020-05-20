import psycopg2
import psycopg2.extras
from flask import Flask
from flask import request
from flask import render_template


app = Flask(__name__)
conn = psycopg2.connect("host=localhost dbname=sql_injection user=sql_injection password=1234")
conn.autocommit = True
cur = conn.cursor()
cur.execute('''
    DROP SCHEMA public CASCADE;
    CREATE SCHEMA public;
    GRANT ALL ON SCHEMA public TO sql_injection;
    GRANT ALL ON SCHEMA public TO public;
    COMMENT ON SCHEMA public IS 'standard public schema';
''')
cur.execute('CREATE TABLE texts (id serial PRIMARY KEY, title varchar, text varchar, status varchar);')
cur.execute('CREATE TABLE users (id serial PRIMARY KEY, username varchar, password varchar);')
cur.execute("INSERT INTO texts (title,text,status) VALUES ('text1', 'text1','active'),('text2','text2','deactive');")
cur.execute("INSERT INTO users (username,password) VALUES ('username', 'password');")
cur.close()

@app.route('/texts', methods=['GET'])
def get_texts():
    status = request.args.get('status', None)
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    if status is not None:
        query = """
        SELECT title,text FROM texts
        WHERE status='%s'
        """ %status
        cur.execute(query)
        texts = cur.fetchall()
        print(texts)
        cur.close()
        data = dict()
        data['resp'] = list()
        for t in texts:
            data['resp'].append(dict(t))
        return data
    else:
        return ('send status!!', 400)


@app.route('/text', methods=['GET'])
def get_text():
    id = request.args.get('id', None)
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    if id is not None:
        query = """
        SELECT title,text FROM texts
        WHERE id=%s
        """ %id
        cur.execute(query)
        text = cur.fetchone()
        cur.close()
        data = dict()
        data['resp'] = text
        return data
    else:
        return ('send id!!', 400)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html', error='')
    else:
        username = request.form.get('username', None)
        password = request.form.get('password', None)
        cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        if username is not None and password is not None:
            query = """
            SELECT * FROM users
            WHERE username='%s' AND password='%s'
            """ % (username, password)
            cur.execute(query)
            user = cur.fetchone()
            cur.close()
            if user:
                return 'ok'
            else:
                return render_template('login.html', error='invalid login!')
        else:
            return ('send username and password!!', 400)
