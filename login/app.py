from flask import Flask, render_template, request, redirect, url_for, session
from flask_mysqldb import MySQL
import MySQLdb.cursors
import re


app = Flask(__name__)


app.secret_key = 'rohit23'

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'pikachu2022#$'
app.config['MYSQL_DB'] = 'sauravlogin'

mysql = MySQL()
mysql.init_app(app)




@app.route('/')
@app.route('/home')
def home():
    return render_template('home.html')

@app.route('/login', methods=['GET', 'POST'])
def login():

    msg = ''
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        username = request.form['username']
        password = request.form['password']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute(
            'SELECT * FROM Account WHERE username = % s AND password = % s', (username, password, ))
        Account = cursor.fetchone()
        if Account:
            session['loggedin'] = True
            session['id'] = Account['id']
            session['username'] = Account['username']
            msg = 'Logged in successfully !'
            return render_template('index.html', msg=msg)
        else:
            msg = 'Incorrect username / password !'
    return render_template('login.html', msg=msg)


@app.route('/logout')
def logout():
    session.pop('loggedin', None)
    session.pop('id', None)
    session.pop('username', None)
    return redirect(url_for('home'))


@app.route('/register', methods=['GET', 'POST'])
def register():

    msg = ''
    if request.method == 'POST' and 'name' in request.form and 'username' in request.form and 'password' in request.form and 'email' in request.form and 'nickname' in request.form and 'hobby' in request.form :
        name = request.form['name']
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        nickname = request.form['nickname']
        hobby = request.form['hobby']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute(
            'SELECT * FROM Account WHERE name = % s and username= %s', (name, username))
        Account = cursor.fetchone()
        if Account:
            msg = 'Account already exists !'
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            msg = 'Invalid email address !'
        elif not re.match(r'[A-Za-z]+', name):
            msg = 'Enter your Name properly'
        elif not re.match(r'[A-Za-z0-9]+', username):
            msg = 'Username must contain only characters and numbers !'
        elif not name or not username or not password or not email or not nickname or not hobby :
            msg = 'Please fill out the form !'
        else:
            cursor.execute('INSERT INTO Account VALUES (NULL,%s, % s, % s, % s,%s,%s)',
                           (name, username, password, email, nickname, hobby))
            mysql.connection.commit()
            msg = 'You have successfully registered !'
    # elif request.method == 'POST':
    #     msg = 'Please fill out the form !'
    return render_template('register.html', msg=msg)


@app.route("/profile")
def profile():
    #global Account
    if 'loggedin' in session:

        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM Account WHERE id = % s',
                       (session['id'], ))
        Account = cursor.fetchone()

        return render_template("profile.html", Account=Account)
    return redirect(url_for('login'))


@app.route("/comment", methods=['GET', 'POST'])
def comment():
    msg=''
    if request.method=='POST' and 'Name' in request.form and 'message' in request.form :
        Name=request.form['Name']
        message=request.form['message']
        cursor=mysql.connection.cursor()
        cursor.execute('INSERT INTO comments VALUES(NULL,%s,%s)',(Name,message,))
        mysql.connection.commit()
        msg='Your comment is successfully posted!!'
        
    return render_template('add_comment.html',msg=msg)

@app.route("/read_comments")
def read_comments():
    if 'loggedin' in session:
        cursor=mysql.connection.cursor()
        cursor.execute('SELECT * FROM comments ')
        comments=cursor.fetchall()
        return render_template("comment.html",comments=comments)
    return redirect(url_for('login'))

@app.route("/index")
def index():
    if 'loggedin' in session:
        return render_template("index.html")
    return redirect(url_for('login'))


@app.route("/update", methods=['GET', 'POST'])
def update():

    msg = ''
    if 'loggedin' in session:
        if request.method == 'POST' and 'name' in request.form and 'username' in request.form and 'password' in request.form and 'email' in request.form and 'nickname' in request.form and 'hobby' in request.form:
            name = request.form['name']
            username = request.form['username']
            password = request.form['password']
            email = request.form['email']
            nickname = request.form['nickname']
            hobby = request.form['hobby']
            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            cursor.execute(
                'SELECT * FROM Account WHERE name= %s and username = % s', (name, username, ))
            Account = cursor.fetchone()
            if Account:
                msg = 'Account already exists !'
            elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
                msg = 'Invalid email address !'
            elif not re.match(r'[A-Za-z0-9]+', username):
                msg = 'name must contain only characters and numbers !'
            else:
                cursor.execute('UPDATE Account SET name=%s, username =% s, password =% s, email =% s, nickname=%s , hobby = %s WHERE id =% s', (
                    name, username, password, email, nickname, hobby, (session['id'], ), ))
                mysql.connection.commit()
                msg = 'You have successfully updated !'
        elif request.method == 'POST':
            msg = 'Please fill out the form !'
        return render_template("update.html", msg=msg)
    return redirect(url_for('login'))


@app.route('/search', methods=['GET', 'POST'])
def search():
    msg = ''
    if request.method == 'POST' and 'name' in request.form:
        name=request.form['name']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute(
        'SELECT * FROM Account WHERE name=%s', (name, ))
        Account = cursor.fetchone()
        if Account:
            session['loggedin']=True
            session['name']=Account['name']
            msg="User found :)"
            return render_template('profile2.html',msg=msg,Account=Account)
        else:
            msg="User not found :/"
    return render_template("search.html", msg=msg)
    
        
    



if __name__ == '__main__':
    app.run(debug=True)
