from flask import *
from flask_mysqldb import *
from sqlalchemy import *
import mysql.connector

#Flask app configuration
app = Flask(__name__)
app.secret_key="mykey"

#database Configuration
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = '123456'
app.config['MYSQL_DB'] = 'mbti'

# initialize MySQL
mysql = MySQL(app)

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        age = request.form['age']
        email = request.form['email']
        cursor = mysql.connection.cursor()
        # cur.execute("SELECT * FROM users WHERE username = %s", (username,))
        # user = cur.fetchone()
        # cur.close()
        # if user:
        #     flash('username already exists. Please choose another username.', 'error')
        #     return redirect('/signup')
        # cur = mysql.connection.cursor()
        cursor.execute('INSERT INTO users(username, password, age, email) VALUES(%s, %s, %d, %s)', (username, password, age, email))
        mysql.connection.commit()
        cursor.close()
        return redirect('/login')
    return render_template('signup.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        cursor = mysql.connection.cursor()
        cursor.execute('SELECT * FROM users WHERE username = %s AND password = %s', (username, password))
        user = cursor.fetchone()
        cursor.close()
        if user:
            session['username'] = username
            return redirect('/signup')
        else:
            return render_template('login.html', message='Invalid email or password')

    return render_template('login.html')

# Logout page
# @app.route('/logout')
# def logout():
#     session.pop('username', None)
#     return redirect(url_for('login'))


if __name__ == "__main__":
    app.run(debug=True, port=8080,use_reloader=False)