
from datetime import datetime
from typing import Sequence, Union
from functools import reduce

import pandas as pd

def read_csv(filepath: str) -> pd.DataFrame:
    '''
    Reads useful columns from a CSV file into a pandas DataFrame.
    '''
    useful_columns = [0, 3, 6, 8, 22, 23, 24, 33]
    types = {
        'hashtags': str
    }
    dataframe = pd.read_csv(
        filepath,
        index_col=False,
        usecols=useful_columns,
        parse_dates=['date'],
        dtype=types
    )
    return dataframe

#%%
def prepare_tweets_df(tweets: pd.DataFrame, before: Union[datetime, str]) -> pd.DataFrame:
    '''
    Parses data types of 'date' to datetime and 'hashtags' to str,
    and selects data before given date.
    '''
    tweets.loc[:, 'date'] = pd.to_datetime(tweets['date'])
    tweets.loc[:, 'hashtags'] = tweets['hashtags'].astype(str)
    return tweets[
        tweets['date'] < before
    ]

#%%
def filter_tweets_by_hashtag(tweets: pd.DataFrame, hashtag: str) -> pd.DataFrame:
    '''
    Filters tweets that contain a hashtag.
    '''
    return tweets[
        tweets['hashtags'].str.contains(hashtag)
    ]

#%%
def count_tweets_by_date(tweets: pd.DataFrame) -> pd.DataFrame:
    '''
    Counts tweets by grouping them by unique dates.
    '''
    # add new column to hold tweets count
    tweets.insert(0, 'count', 0)
    grouped_tweets = (tweets
        .resample('D', on='date')
        .count()
        .drop(columns=['date'])
        .reset_index())[['date', 'count']]
    return grouped_tweets

#%%
def count_tweets_by_hashtags(tweets: pd.DataFrame, hashtags: Sequence[str]) -> pd.DataFrame:
    '''
    Counts tweets separately by specified hashtags.
    '''
    return (reduce(
        lambda g1, g2: pd.merge(g1, g2, how='outer'),
        [
            count_tweets_by_date(
                filter_tweets_by_hashtag(tweets, hashtag)
            # set column name as hashtag
            ).rename(columns={'count': hashtag})
            for hashtag in hashtags
        ] 
    )
    # there can be NaN's if dataframes don't have exactly the same dates
    .fillna(0)
    .sort_values('date')
    .reset_index(drop=True))

#%%
def sum_likes_by_date(tweets: pd.DataFrame) -> pd.DataFrame:
    likes = tweets[['date', 'nlikes']]
    likes.insert(0, 'only_date', likes['date'].dt.date)
    likes.insert(0, 'sum', likes.resample('D', on='date').transform('sum'))
    return likes.drop(columns=['date'])

#%%
def count_likes_sums_by_date(likes: pd.DataFrame) -> pd.DataFrame:
    return likes.groupby(['only_date', 'sum']).count().reset_index()
