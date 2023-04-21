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
it = int(session.get('it', 0))
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
    print(pe)