from modulefinder import EXTENDED_ARG
import os, sys
from dotenv import load_dotenv
import tweepy
import pandas as pd

load_dotenv()
api_key = os.getenv('twiter_api_key')
api_key_secret = os.getenv('twiter_api_key_secret')

access_token = os.getenv('twiter_access_token')
access_token_secret = os.getenv('twiter_access_token_secret')

# authentication
auth = tweepy.OAuthHandler(api_key, api_key_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)

def get_tweets(config):
    '''
    
    '''
    for query in config.queries[config.candidate]:
        
        print(f'Getting tweets with query = {query}')
        # getting tweets by query
        # multiple queries 
        # https://stackoverflow.com/questions/49027297/how-to-get-tweets-data-that-contain-multiple-keywords
        limit = config.queries.limit

        # TODO start and end date
        tweets = tweepy.Cursor(api.search_tweets, q=query, count=100, tweet_mode='extended', until=config.until).items(limit)
        # tweets= tweepy.Cursor(api.user_timeline, screen_name=user, rpp=200, tweet_mode='extended').items(limit)

        # create DataFrame
        columns = ['user', 'tweet', 'date', 'likes', 'geo', 'coordinates', 'place', 'user_loc']
        data = []

        # Possible data
        # https://developer.twitter.com/en/docs/twitter-api/v1/tweets/search/api-reference/get-search-tweets
        for tweet in tweets:
            data.append([tweet.user.screen_name, tweet.full_text, tweet.created_at, tweet.favorite_count, tweet.geo, tweet.coordinates, tweet.place, tweet.user.location])

        df = pd.DataFrame(data, columns=columns)
        df['query'] = query

        # save file
        q = query.replace('#', '').replace(' ', '')
        df.to_csv(f'{config.save_dir}/tweets_{q.lower()}.csv',encoding='utf-8', index=False)

    return
