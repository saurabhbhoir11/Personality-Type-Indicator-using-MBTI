from flask import *
from flask_mysqldb import *
import mysql.connector
import snscrape.modules.twitter as sntwitter
import pandas as pd
import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
import numpy as np
import pickle
nltk.download('stopwords')
nltk.download('wordnet')
nltk.download('omw-1.4')
from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer, TfidfVectorizer
import re
import joblib

'''import tweepy 
import configparser'''

app = Flask(__name__)
app.secret_key = "mykey"

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = '123456'
app.config['MYSQL_DB'] = 'mbti'

# Twitter API credentials
#consumer_key = ""
#consumer_secret = ""
#access_token = ""
#access_token_secret = ""

mysql = MySQL(app)

limit = 1000
# load models
#mod1 = joblib.load('IE1.sav')
#mod2 = joblib.load('NS1.sav')
#mod3 = joblib.load('TF1.sav')
#mod4 = joblib.load('JP1.sav')

with open('modelIE.pkl', 'rb') as f:
    loaded_modelIE = pickle.load(f)
with open('modelNS.pkl', 'rb') as f:
    loaded_modelNS = pickle.load(f)
with open('modelTF.pkl', 'rb') as f:
    loaded_modelTF = pickle.load(f)
with open('modelJP.pkl', 'rb') as f:
    loaded_modelJP = pickle.load(f)

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


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/getTweets', methods=['GET', 'POST'])
def getTweets():
    if request.method == 'POST':
        twitter = request.form['twitter_id']
        cursor = mysql.connection.cursor()
        cursor.execute('insert into tweets values (%s)', (twitter,))
        mysql.connection.commit()
        cursor.close()
        test = check_username(twitter)
        if test:
            query = '(from:' + twitter + ') lang:en'
            tweets = ''
            i = 0
            for tweet in sntwitter.TwitterSearchScraper(query=query).get_items():
                if i == limit:
                    break
                else:
                    tweets = tweets + ' ' + tweet.rawContent
                    i += 1
            tweets = preprocess(tweets)
            type = predict(tweets)
            # print(tweets)
            pr = '<h1>' + type + '</hi>'
            return pr
        return redirect(url_for('home'))

    return render_template('getTweets.html')


@app.route('/takeTest')
def takeTest():
    return render_template('index2.html')


def preprocess(tweets):
    # converting all text/posts to lower case
    tweets = tweets.lower()

    '''This function takes a list of texual data as input.
       It performs pre-processing and natural language processing on the data.
       It returns the processed textual data list as output.'''

    # remove url links
    pattern = re.compile(r'https?://[a-zA-Z0-9./-]*/[a-zA-Z0-9?=_.]*[_0-9.a-zA-Z/-]*')
    tweets = re.sub(pattern, ' ', tweets)

    pattern2 = re.compile(r'https?://[a-zA-Z0-9./-]*')
    tweets = re.sub(pattern, ' ', tweets)

    # removing special characters and numbers from texts.

    pattern = re.compile('\W+')
    tweets = re.sub(pattern, ' ', tweets)
    pattern = re.compile(r'[0-9]')
    tweets = re.sub(pattern, ' ', tweets)
    pattern = re.compile(r'[_+]')
    tweets = re.sub(pattern, ' ', tweets)

    # removing extra spaces from texts.

    pattern = re.compile('\s+')
    tweets = re.sub(pattern, ' ', tweets)

    # remove stop words
    remove_words = stopwords.words("english")
    tweets = " ".join([w for w in tweets.split(' ') if w not in remove_words])

    # remove mbti personality words from text
    mbti_words = ['infj', 'entp', 'intp', 'intj', 'entj', 'enfj', 'infp', 'enfp', 'isfp', 'istp', 'isfj', 'istj',
                  'estp', 'esfp', 'estj', 'esfj']

    tweets = " ".join([w for w in tweets.split(' ') if w not in mbti_words])

    # Lemmatization (grouping similar words)
    from nltk.stem import WordNetLemmatizer
    lemmatizer = WordNetLemmatizer()
    nltk.download('wordnet')
    tweets = " ".join([lemmatizer.lemmatize(w) for w in tweets.split(' ')])

    df = pd.read_csv('data.csv')
    tweets = [tweets]
    df.append(tweets)
    post_list = []
    for i, j in df.posts.iteritems():
        post_list.append(j)

    vector = CountVectorizer(stop_words='english', max_features=1500)
    features = vector.fit_transform(post_list)
    # print(finalfeatures.shape)

    # tf-idf to weigh the importance of words(features) across all posts and select more relevent features
    transform = TfidfTransformer()
    finalFeatures = transform.fit_transform(features).toarray()
    out = [finalFeatures[8673]]
    return out


def predict(tweets):
    ie = loaded_modelIE.predict(tweets)
    print(ie)
    ns = loaded_modelNS.predict(tweets)
    print(ns)
    tf = loaded_modelTF.predict(tweets)
    print(tf)
    jp = loaded_modelJP.predict(tweets)
    print(jp)
    type = ''
    if ie == 1:
        type = 'E'
    else:
        type = 'I'

    if ns == 1:
        type = type + 'S'
    else:
        type = type + 'N'

    if tf == 1:
        type = type + 'F'
    else:
        type = type + 'T'

    if jp == 1:
        type = type + 'P'
    else:
        type = type + 'J'
    return type


def check_username(username):
    # Format the username with the @ symbol if it doesn't already have it
    if username[0] != '@':
        username = '@' + username
    # Use snscrape to search for the Twitter user with the given username
    query = f'{username} since_id:1'
    tweets = sntwitter.TwitterSearchScraper(query).get_items()
    # Check if any tweets were returned
    return any(True for tweet in tweets)


if __name__ == "__main__":
    app.run(debug=True)
