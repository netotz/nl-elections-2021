
from datetime import datetime
from typing import Sequence
import pandas as pd

import twint
import nest_asyncio

import constants
from models.candidate import Candidate

def configure_common(
        limit: int,
        since: datetime,
        until: datetime) -> twint.Config:
    '''
    Configures common properties to scrape Twitter.
    '''
    return twint.Config(
        Hide_output=True,
        Pandas=True,
        Pandas_clean=True,
        Stats=True,
        Limit=limit if limit >= 0 else None,
        Since=str(since.date()) if since else None,
        Until=str(until.date()) if until else None
    )

def configure_tweets_by_candidate(
        candidate: Candidate,
        limit: int = -1,
        since: datetime = None,
        until: datetime = None) -> twint.Config:
    '''
    Configures scrapper to get tweets made by a candidate.
    '''
    config = configure_common(limit, since, until)
    config.Username = candidate.twitter
    config.Filter_retweets = True

    return config

def configure_tweets_by_hashtags(
        hashtags: Sequence[str],
        limit: int = -1,
        since: datetime = None,
        until: datetime = None) -> twint.Config:
    '''
    Configures scrapper to get tweets that include any of the specified hashtags.
    '''
    config = configure_common(limit, since, until)
    query = ' OR '.join(hashtags)
    config.Custom_query = query

    return config

# when using IPython
nest_asyncio.apply()

#%%
def get_tweets_by_hashtags(hashtags: Sequence[str], since: datetime, save: bool = False) -> pd.DataFrame:
    config = configure_tweets_by_hashtags(
        hashtags,
        since=since
    )
    twint.run.Search(config)

    # save scrapped tweets as dataframe
    tweets_hashtags = twint.storage.panda.Tweets_df
    if save:
        tweets_hashtags.to_csv(f'..\\tweets_{hashtags}.csv')
    return tweets_hashtags

#%%
def get_tweets_by_candidate(candidate: Candidate, since: datetime, save: bool = False) -> pd.DataFrame:
    config = configure_tweets_by_candidate(
        candidate,
        since=since
    )
    twint.run.Search(config)

    tweets_candidate = twint.storage.panda.Tweets_df
    if save:
        tweets_candidate.to_csv(f'..\\tweets_{constants.CLARA_LUZ.twitter}.csv')
    return tweets_candidate

# # get useful columns by inspecting the dataframe
# columns_indexes = [0, 3, 22, 23, 24]
# # filter dataframe by useful columns
# tweets = tweets[[
#     c for i, c in enumerate(tweets.columns)
#     if i in columns_indexes
# ]]
