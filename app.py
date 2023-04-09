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
# consumer_key = ""
# consumer_secret = ""
# access_token = ""
# access_token_secret = ""

mysql = MySQL(app)

limit = 300
# load models
# mod1 = joblib.load('IE1.sav')
# mod2 = joblib.load('NS1.sav')
# mod3 = joblib.load('TF1.sav')
# mod4 = joblib.load('JP1.sav')

with open('log_modelIE.pkl', 'rb') as f:
    loaded_modelIE = pickle.load(f)
with open('log_modelNS.pkl', 'rb') as f:
    loaded_modelNS = pickle.load(f)
with open('log_modelTF.pkl', 'rb') as f:
    loaded_modelTF = pickle.load(f)
with open('log_modelJP.pkl', 'rb') as f:
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
            adv, disadv = getAdvantages_Disadvantages(type)
            # print(tweets)
            pr = '<h1>' + type + '</hi> <br> <h1>' + twitter + '</h1> ' '''<br> <h1>' + adv + '<br>' + disadv + '</hi>' '''
            #return render_template('result.html', type, adv, disadv)
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
    print(df.shape)
    print(df.tail(1))
    new_row = pd.DataFrame({'posts': [tweets]})
    df = pd.concat([df, new_row], ignore_index=True)
    print(df.shape)
    print(df.tail(1))
    post_list = []
    for i, j in df.posts.iteritems():
        post_list.append(j)
    # tweets = [tweets]
    vector = CountVectorizer(stop_words='english', max_features=1500)
    features = vector.fit_transform(post_list)
    # print(finalfeatures.shape)

    # tf-idf to weigh the importance of words(features) across all posts and select more relevent features
    transform = TfidfTransformer()
    finalFeatures = transform.fit_transform(features).toarray()
    out = [finalFeatures[8674]]
    # out = finalFeatures
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
    typee = ''
    if ie == 0:
        typee = 'E'
    else:
        typee = 'I'

    if ns == 0:
        typee = typee + 'S'
    else:
        typee = typee + 'N'

    if tf == 0:
        typee = typee + 'F'
    else:
        typee = typee + 'T'

    if jp == 0:
        typee = typee + 'P'
    else:
        typee = typee + 'J'
    return typee


def getAdvantages_Disadvantages(type):
    advanteges = dict(ISTJ=['Responsible and dependable', 'Good at following established procedures and guidelines',
                            'Highly organized and detail-oriented',
                            'Strong work ethic and dedication to their responsibilities',
                            'Capable of handling complex and difficult tasks',
                            'Able to remain calm and level-headed in stressful situations'],
                      ISFJ=['Loyal and dedicated to their relationships and responsibilities',
                            'Good at organizing and maintaining order',
                            'Attentive to the needs of others and skilled at providing practical support',
                            'Detail-oriented and conscientious',
                            'Reliable and trustworthy',
                            'Often have strong memories and recall details well'],
                      INFJ=['Empathetic and insightful, able to understand and connect with others on a deep level',
                            'Idealistic and committed to making the world a better place',
                            'Highly creative and imaginative',
                            'Good at planning and executing long-term projects',
                            'Often have a strong sense of intuition or "gut feeling" that guides their decision-making',
                            'Capable of seeing the big picture and understanding complex systems'],
                      INTJ=['Highly analytical and strategic thinkers',
                            'Able to see the big picture and make connections between seemingly unrelated concepts',
                            'Independent and self-motivated',
                            'Often have a strong vision and clear goals for the future',
                            'Skilled at planning and executing complex projects',
                            'Able to remain calm and rational in high-pressure situations'],
                      ISTP=['Good problem solvers who enjoy working with their hands and figuring out how things work',
                            'Calm and collected in high-pressure situations',
                            'Pragmatic and logical, able to make tough decisions quickly',
                            'Often have a good sense of humor and enjoy having fun',
                            'Independent and self-sufficient',
                            'Good at improvising and adapting to unexpected situations'],
                      ISFP=['Creative and artistic',
                            'Sensitive to beauty and aesthetics',
                            'Tend to be easy-going and flexible',
                            'Good at adapting to new or changing situations',
                            'Warm and supportive towards loved ones',
                            'Appreciative of sensory experiences and pleasures'],
                      INFP=['Highly analytical and logical',
                            'Creative and innovative problem-solvers',
                            'Independent and self-motivated',
                            'Open-minded and curious',
                            'Adept at understanding complex systems and theories',
                            'Can be objective and impartial'],
                      INTP=["Analytical and logical thinkers",
                            "Innovative problem solvers",
                            "Independent and self-directed",
                            "Tolerant of diverse perspectives and ideas",
                            "Objective and impartial decision makers",
                            "Excellent at strategic planning and big-picture thinking"],
                      ESTP=['Confident and charismatic',
                            'Skilled at adapting to new or changing situations',
                            'Enjoy taking risks and trying new things',
                            'Excellent at problem-solving in the moment',
                            'Highly observant and able to pick up on subtle cues',
                            'Tend to be action-oriented and hands-on'],
                      ESFP=['Energetic and enthusiastic',
                            'Friendly and outgoing',
                            'Good at connecting with others and building relationships',
                            'Flexible and adaptable',
                            'Enjoy living in the moment and trying new things',
                            'Skilled at improvisation and spontaneity'],
                      ENFP=['Energetic and enthusiastic',
                            'Creative and imaginative',
                            'Good at generating new ideas and possibilities',
                            'Empathetic and attuned to the emotions of others',
                            'Skilled at inspiring and motivating others',
                            'Open-minded and adaptable'],
                      ENTP=["Quick and ingenious problem solvers",
                            "Energetic and enthusiastic",
                            "Great at generating new ideas and possibilities",
                            "Good at debate and argumentation",
                            "Excellent at strategic thinking and planning",
                            "Confident and assertive in their communication"],
                      ESTJ=['Efficient and highly organized',
                            'Good at developing and implementing systems and procedures',
                            'Strong leadership skills',
                            'Confident and assertive',
                            'Excellent at making decisions based on objective facts and data',
                            'Good at managing and delegating tasks to others'],
                      ESFJ=['Warm and friendly towards others',
                            'Skilled at building and maintaining relationships',
                            'Very social and outgoing',
                            'Good at creating and maintaining a sense of community',
                            'Highly reliable and responsible',
                            'Often have strong organizational skills'],
                      ENFJ=['Charismatic and persuasive',
                            'Empathetic and caring towards others',
                            'Skilled at building and maintaining relationships',
                            'Effective communicators and natural leaders',
                            'Good at motivating and inspiring others',
                            'In tune with their own emotions and the emotions of others'],
                      ENTJ=['Confident and decisive',
                            'Good at seeing the big picture and setting long-term goals',
                            'Strong leadership skills and ability to motivate others',
                            'Excellent at problem-solving and strategic thinking',
                            'Often highly organized and efficient',
                            'Capable of taking on complex and challenging tasks'])
    disadvantages = dict(ISTJ=['Can be inflexible and resistant to change',
                               'Tendency to focus too much on the details and lose sight of the big picture',
                               'May struggle with expressing their emotions or understanding the emotions of others',
                               'Can be overly critical or judgmental of others',
                               'May have a hard time adapting to new or unexpected situations',
                               'May struggle with taking risks or trying new things'],
                         ISFJ=['Loyal and dedicated to their relationships and responsibilities',
                               'Good at organizing and maintaining order',
                               'Attentive to the needs of others and skilled at providing practical support',
                               'Detail-oriented and conscientious',
                               'Reliable and trustworthy',
                               'Often have strong memories and recall details well'],
                         INFJ=['May become overwhelmed by the emotions and needs of others',
                               'Can be overly self-critical and perfectionistic',
                               'Tendency to focus too much on the big picture and neglect the details',
                               'May struggle with making decisions when their intuition isn\'t clear',
                               'Can be overly sensitive to criticism or rejection',
                               'May have difficulty asserting their own needs and boundaries'],
                         INTJ=['Tendency to be dismissive or critical of others who don\'t share their vision or goals',
                               'May struggle with expressing their emotions or understanding the emotions of others',
                               'Can be overly confident in their own abilities and ideas',
                               'May become impatient or frustrated with those who don\'t understand or agree with their vision',
                               'May have difficulty delegating tasks or working collaboratively with others',
                               'May struggle with social skills or building personal relationships'],
                         ISTP=['May struggle with expressing their emotions or understanding the emotions of others',
                               'Can be insensitive or dismissive of others\' feelings',
                               'May have difficulty committing to long-term relationships or plans',
                               'Tendency to take risks or pursue thrill-seeking activities without considering potential consequences',
                               'May be seen as overly reserved or detached by others',
                               'May struggle with adhering to rules or guidelines they see as unnecessary'],
                         ISFP=['May have difficulty making decisions or committing to long-term plans',
                               'Tendency to avoid conflict or difficult conversations',
                               'May be easily overwhelmed by stress or emotional situations',
                               'Can be overly sensitive or take things personally',
                               'May struggle with following strict rules or guidelines',
                               'May have difficulty expressing their emotions or needs'],
                         INFP=['May struggle with emotional expression or connecting with others on an emotional level',
                               'May come across as overly critical or dismissive of others\' opinions',
                               'Tendency to overanalyze and get lost in their thoughts',
                               'May have difficulty following through with projects or commitments',
                               'May struggle with routine or mundane tasks',
                               'Can be seen as cold or aloof in social situations'],
                         INTP=["May struggle with emotional expression or sensitivity",
                               "Can be overly critical or dismissive of others' ideas",
                               "May become overly focused on theories and ideas, ignoring practical considerations",
                               "May have difficulty with routine tasks or following established procedures",
                               "May struggle with interpersonal relationships or social situations",
                               "May be perceived as aloof or unemotional"],
                         ESTP=['Can be impulsive and act without thinking through consequences',
                               'May struggle with long-term planning or following through on commitments',
                               'May become bored or restless with routine tasks',
                               'Can be insensitive to the emotions of others',
                               'May have a tendency to engage in reckless or dangerous behaviors',
                               'May struggle with authority and rules'],
                         ESFP=['May struggle with long-term planning and following through on commitments',
                               'Can be impulsive and make decisions without considering all the consequences',
                               'May have difficulty with abstract or theoretical concepts',
                               'May become bored or restless with routine or repetitive tasks',
                               'May prioritize their own enjoyment over responsibilities or obligations',
                               'May struggle with setting boundaries or saying "no" to others'],
                         ENFP=['Tendency to be easily distracted or lose focus',
                               'May struggle with following through on commitments or completing tasks',
                               'Can be overly sensitive or take criticism personally',
                               'May have difficulty making tough decisions or sticking to one path',
                               'May struggle with routine or repetitive tasks',
                               'May become overwhelmed or anxious when faced with too many responsibilities'],
                         ENTP=["May become argumentative or contrarian for its own sake",
                               "Can have difficulty following through on long-term commitments",
                               "May not always consider the feelings or perspectives of others",
                               "May struggle with routine or mundane tasks",
                               "May have difficulty with authority or rigid rules",
                               "Can be seen as unpredictable or unreliable"],
                         ESTJ=['Can be rigid and inflexible',
                               'May struggle with considering or valuing others’ feelings or perspectives',
                               'May become overly focused on rules or guidelines',
                               'May struggle with adapting to new or unexpected situations',
                               'May be intolerant of others’ mistakes or shortcomings',
                               'May struggle with expressing or recognizing their own emotions'],
                         ESFJ=['Can be overly concerned with the opinions of others',
                               'May struggle with taking criticism or negative feedback',
                               'May become overly involved in the problems or issues of others',
                               'Tendency to avoid conflict or difficult conversations',
                               'May have difficulty setting and asserting personal boundaries',
                               'May struggle with making tough decisions'],
                         ENFJ=['May prioritize the needs of others over their own needs',
                               'Can become overbearing or controlling in their relationships',
                               'May struggle with making difficult decisions that may hurt others',
                               'May have a tendency to avoid conflict or difficult conversations',
                               'Can become overly emotional or reactive in stressful situations',
                               'May struggle with setting and enforcing personal boundaries'],
                         ENTJ=['Can be seen as overly controlling or domineering',
                               'May struggle with understanding the emotions of others',
                               'Tendency to focus more on logic than on emotions',
                               'May become impatient or frustrated with those who don’t share their work ethic or commitment',
                               'May overlook important details in pursuit of their goals',
                               'Can be overly competitive or aggressive in pursuing their objectives'])
    type_advantage = advanteges[type]
    type_disadvantage = disadvantages[type]
    return type_advantage, type_disadvantage


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
