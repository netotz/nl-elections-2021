import twint

import nest_asyncio

import constants

# configure Twitter scrapper
config = twint.Config()
config.Username = constants.CLARA_LUZ.twitter
config.Limit = 500
config.Count = True
config.Stats = True
config.Pandas = True
config.Pandas_au = True
config.Hide_output = True
config.Filter_retweets = True

# when using IPython
nest_asyncio.apply()

twint.run.Search(config)

# save scrapped tweets as dataframe
tweets = twint.storage.panda.Tweets_df
# get useful columns by inspecting the dataframe
columns_indexes = [0, 3, 22, 23, 24]
# filter dataframe by useful columns
tweets = tweets[[
    c for i, c in enumerate(tweets.columns)
    if i in columns_indexes
]]
