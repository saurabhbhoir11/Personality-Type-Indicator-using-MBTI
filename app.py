from flask import *
from flask_mysqldb import *
import mysql.connector

app = Flask(__name__)
app.secret_key = "mykey"

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = '123456'
app.config['MYSQL_DB'] = 'mbti'

mysql = MySQL(app)

@app.route("/", methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        age = request.form['age']
        email = request.form['email']
        cursor = mysql.connection.cursor()
        cursor.execute('INSERT INTO users (username, password, age, email) VALUES(%s, %s, %s, %s)',
                       (username, password, age, email))
        mysql.connection.commit()
        cursor.close()
        return redirect(url_for('login'))
    return render_template("Signup.html")


@app.route("/login", methods=['GET', 'POST'])
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
            return redirect(url_for('signup'))
        else:
            return render_template('login.html', message='Invalid email or password', flag=1)
    return render_template("login.html", flag=0)


if __name__ == "__main__":
    app.run(debug=True)
