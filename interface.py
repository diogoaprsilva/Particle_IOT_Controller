from flask import Flask, render_template, request, redirect, Response
from functools import wraps
import psycopg2
import psycopg2.extras
import datetime
import os
from urllib.parse import urlencode
from urllib.request import Request, urlopen
import ssl
import urllib.request

app = Flask(__name__)

connection_string = os.environ['DATABASE_URL']

def check_auth(username, password):
    '''THIS IS FOR THE USERNAME AND PASSWORD VARIABLE'''
    return username == os.environ['USERNAME']; password == os.environ['PASSWORD'];

def authenticate():
    return Response(
    'Could not verify your access level for that URL.\n'
    'You have to login with proper credentials', 401,
    {'WWW-Authenticate': 'Basic realm="Login Required"'})

def requires_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth = request.authorization
        if not auth or not check_auth(auth.username, auth.password):
            return authenticate()
        return f(*args, **kwargs)
    return decorated

@app.route('/')
@requires_auth
def hello_world():
        conn = psycopg2.connect(connection_string)
        cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        cursor.execute("SELECT * FROM temperature ORDER BY reading_date DESC LIMIT 5")
        records = cursor.fetchall()

        cursor.execute("SELECT * FROM temperature ORDER BY temperature DESC LIMIT 1 ")
        highest = cursor.fetchall()
        max = highest[0]

        cursor.execute("SELECT * FROM temperature ORDER BY temperature ASC LIMIT 1")
        lowest = cursor.fetchall()
        low = lowest[0]

        return render_template('index.html', temperature=36, records=records, highest=max, lowest=low)



@app.route('/about')
@requires_auth
def about():
    return render_template("about_the_project.html")

@app.route('/members')
@requires_auth
def members():
    return render_template('item_used.html')

@app.route('/mainidea')
@requires_auth
def mainidea():
    return render_template('our_main_idea.html')

@app.route('/handle',methods=['POST'])
@requires_auth
def handle():
    conn = psycopg2.connect(connection_string)
    cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    temperature = float(request.form['temperature'])
    current_date = datetime.datetime.now()

    query = 'INSERT INTO temperature (reading_date, temperature)  VALUES (\'%s\', %s)' % (current_date, temperature)
    cursor.execute(query)

    conn.commit()
    conn.close()
    return redirect('/form')

@app.route('/deletedatabase',methods=['POST'])
@requires_auth
def deletedatabase():
    conn = psycopg2.connect(connection_string)
    cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    query = 'DELETE FROM temperature'
    cursor.execute(query)
    conn.commit()
    conn.close()
    return redirect('/form')


@app.template_filter('format_date')
def reverse_filter(record_date):
    return record_date.strftime('%Y-%m-%d %H:%M')

@app.route('/form')
@requires_auth
def form():
    return render_template('form.html')

@app.route('/led', methods=['POST'])
def led():
    url = "https://api.particle.io/v1/devices/%s/led?access_token=%s" % (os.environ['DEVICE_ID'], os.environ['ACCESS_TOKEN'])
    arg = request.form['arg']
    post_fields = {'arg': arg}
    gcontext = ssl.SSLContext(ssl.PROTOCOL_TLSv1)
    req = Request(url, urlencode(post_fields).encode())
    urlopen(req, context=gcontext)
    return arg

@app.route('/ledstate')
def ledstate():
    url = "https://api.particle.io/v1/devices/%s/ledstate?access_token=%s" % (os.environ['DEVICE_ID'], os.environ['ACCESS_TOKEN'])
    gcontext = ssl.SSLContext(ssl.PROTOCOL_TLSv1)
    return urlopen(url, context=gcontext).read()




if __name__ == '__main__':
    app.run()