
from datetime import datetime
from typing import Sequence

import twint
import nest_asyncio

import constants

def configure_common(limit, since) -> twint.Config:
    '''
    Configures common properties to scrape Twitter.
    '''
    config = twint.Config()
    config.Hide_output = True
    config.Pandas = True
    config.Pandas_clean = True
    config.Stats = True
    config.Limit = limit if limit >= 0 else None
    config.Since = str(since.date()) if since else None
    config.Store_csv = True

    return config

def configure_tweets_by_candidate(
        candidate: constants.Candidate,
        limit: int = -1,
        since: datetime = None) -> twint.Config:
    '''
    Configures scrapper to get tweets made by a candidate.
    '''
    config = configure_common(limit, since)
    config.Username = candidate.twitter
    config.Filter_retweets = True

    return config

def configure_tweets_by_hashtags(
        hashtags: Sequence[str],
        limit: int = -1,
        since: datetime = None) -> twint.Config:
    '''
    Configures scrapper to get tweets that include any of the specified hashtags.
    '''
    config = configure_common(limit, since)
    query = ' OR '.join(hashtags)
    config.Custom_query = query

    return config

# when using IPython
nest_asyncio.apply()

SINCE = datetime(2021, 3, 5)
HASHTAGS = ('#ladysecta', '#abelguerra')
config = configure_tweets_by_hashtags(HASHTAGS, since=SINCE)
twint.run.Search(config)

# save scrapped tweets as dataframe
tweets = twint.storage.panda.Tweets_df
# # get useful columns by inspecting the dataframe
# columns_indexes = [0, 3, 22, 23, 24]
# # filter dataframe by useful columns
# tweets = tweets[[
#     c for i, c in enumerate(tweets.columns)
#     if i in columns_indexes
# ]]
