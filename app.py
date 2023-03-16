from flask import *
from flask_mysqldb import *
import mysql.connector
import tweepy 
import configparser

app = Flask(__name__)
app.secret_key = "mykey"

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = '123456'
app.config['MYSQL_DB'] = 'mbti'

# Twitter API credentials
consumer_key = ""
consumer_secret = ""
access_token = ""
access_token_secret = ""


mysql = MySQL(app)

@app.route("/signup", methods=['GET', 'POST'])
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

# # Twitter API credentials
# consumer_key = ""
# consumer_secret = ""
# access_token = ""
# access_token_secret = ""

# # Authenticate with Twitter API
# auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
# auth.set_access_token(access_token, access_token_secret)
# api = tweepy.API(auth)

# @app.route('/')
# def home():
#     return render_template('home.html')

# @app.route('/tweets', methods=['POST'])
# def tweets():
#     twitter_id = request.form['twitter_id']
#     tweets = api.user_timeline(screen_name=twitter_id, count=3200)
#     cursor = mysql.connection.cursor()
#     for tweet in tweets:
#         tweet_text = tweet.text.replace("'", "\\'")
#         cursor.execute("INSERT INTO tweets (twitter_id) VALUES ('{}', '{}')".format(twitter_id))
#         mysql.connection.commit()
    
#     return 'Tweets stored in MySQL'

if __name__ == "__main__":
    app.run(debug=True)
