import snscrape.modules.twitter as sntwitter
import pandas as pd

query = "valorant"
tweets = []
limit = 100000


for tweet in sntwitter.TwitterSearchScraper(query=query).get_items():
    
    # print(vars(tweet))
    # break
    if len(tweets) == limit:
        break
    else:
        tweets.append([tweet.date, tweet.rawContent])
        
df = pd.DataFrame(tweets, columns=['Date', 'Tweet'])
print(df)

# to save to csv
# df.to_csv('tweets.csv')