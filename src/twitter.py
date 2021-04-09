
from datetime import datetime

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
    # config.Location = True
    # config.Count = True

    return config

def configure_tweets_by_candidate(
        candidate: constants.Candidate,
        limit: int = -1,
        since: datetime = None) -> twint.Config:
    config = configure_common(limit, since)
    config.Username = candidate.twitter
    config.Filter_retweets = True

    return config

def configure_tweets_by_hashtag(
        hashtag: str,
        limit: int = -1,
        since: datetime = None) -> twint.Config:
    config = configure_common(limit, since)
    config.Search = hashtag
    # config.Near = 'monterrey'

    return config

# when using IPython
nest_asyncio.apply()

SINCE = datetime(2021, 3, 5)
config = configure_tweets_by_hashtag('#ladysecta', since=SINCE)
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
