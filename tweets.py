import tweepy

# Set your Twitter API credentials
consumer_key = 'dt1HAxCviNeXuuYjhbHZUR1XA'
consumer_secret = 'sAjT1h6Z4c3HvDOlFaZBnUXBxq2BL7hDYOUjS8UdwFpxjlXX1x'
access_token = '1180012555395325952-zjrHGesYkCLcIH7kGGugZZQDhkgr6N'
access_token_secret = 'EsWKP6BEwLsecG7FEcduCW19kYQwJPkB9QhDOJFNkekhF'

# Authenticate to Twitter
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

# Create API object
api = tweepy.API(auth)

# Define the username whose tweets you want to scrape
username = "elonmusk"

# Get user object
user = api.get_user(screen_name=username)

# Get tweets from user's timeline
tweets = api.user_timeline(screen_name=username, count=1, tweet_mode="extended")

# Loop through the tweets and access their attributes
for tweet in tweets:
    print("Username:", tweet.user.screen_name)
    print("Text:", tweet.full_text)
    print("Date:", tweet.created_at)
    print("Likes:", tweet.favorite_count)
    print("Retweets:", tweet.retweet_count)
    print("Replies:", tweet.reply_count)
    print("------------------")


# to save to csv
# df.to_csv('tweets.csv')
'''it = int(session.get('it', 0))
        ex = int(session.get('es', 0))
        nt = int(session.get('nt', 0))
        se = int(session.get('se', 0))
        th = int(session.get('th', 0))
        fe = int(session.get('fe', 0))
        ju = int(session.get('ju', 0))
        pe = int(session.get('pe', 0))
        if 
        for i in range(6):
            query = 'radio'+ str(i)
            data_temp = request.args.get(query)
            data.append(data_temp)
        for i in range(6):
            if flag == 0:
                if int(data[i]) > 0:
                    ex += int(data[i])
                    session['ex'] = ex
                else:
                    it += int(data[i])
                    session['it'] = it
            if flag == 1:
                if int(data[i]) > 0:
                    se  += int(data[i])
                    session['se'] = se
                else:
                    nt += int(data[i])
                    session['nt'] = nt
            if flag == 2:
                if int(data[i]) > 0:
                    fe += int(data[i])
                    session['th'] = fe
                else:
                    th += int(data[i])
                    session['th'] = th
            if flag == 3:
                if int(data[i]) > 0:
                    pe += int(data[i])
                    session['pe'] = pe
                else:
                    ju += int(data[i])
                    session['ju'] = ju
            n1 += 1
            if (n1 % 15) == 0:
                flag += 1
                session['flag'] = flag

                 it = int(session.get('it', 0))*(-1)
    ex = int(session.get('es', 0))
    nt = int(session.get('nt', 0))*(-1)
    se = int(session.get('se', 0))
    th = int(session.get('th', 0))*(-1)
    fe = int(session.get('fe', 0))
    ju = int(session.get('ju', 0))*(-1)
    pe = int(session.get('pe', 0))
    print(it)
    print(ex)
    print(nt)
    print(se)
    print(th)
    print(fe)
    print(ju)
    print(pe)'''