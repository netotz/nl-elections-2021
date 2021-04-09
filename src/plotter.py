
from datetime import datetime
import locale

import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import pandas as pd

import constants
from data_processing import count_likes_sums_by_date

locale.setlocale(locale.LC_TIME, 'es_MX')

#%%
def plot_timestamp(timestamp: datetime, label: str, color: str) -> None:
    video_date = timestamp.date()
    plt.axvline(
        video_date,
        ymin=0,
        color=color,
        label=label,
        linestyle='--',
        linewidth=0.5
    )

#%%
def format_date() -> None:
    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%d-%b'))
    plt.gcf().autofmt_xdate()

#%%
def plot_tweets_per_hashtags(counts: pd.DataFrame) -> None:
    fig, ax  = plt.subplots()
    xdates = counts['date']

    ax.grid(True)

    for hashtag in list(counts.columns[1:]):
        ycount = counts[hashtag]
        ax.plot(xdates, ycount, label=f'#{hashtag}', linewidth=0.8)
    plot_timestamp(constants.VIDEO_PUBLISHED, 'Video publicado', 'indianred')

    ax.legend()
    
    format_date()
    plt.xlabel('Día')
    plt.ylabel('Tweets')
    plt.title('Cantidad de tweets por hashtag por día')
    plt.show()

#%%
def plot_likes(tweets: pd.DataFrame) -> None:
    xdates = tweets['only_date']
    ylikes = tweets['nlikes']

    plt.grid(True)
    plt.scatter(
        xdates, ylikes,
        s=10, c=ylikes, cmap='YlOrRd',
        edgecolor='black', linewidth=0.3,
        alpha=0.8
    )
    
    likes = count_likes_sums_by_date(tweets)
    xdates = likes['only_date']
    ysum = likes['sum']
    plt.plot(xdates, ysum, label='Likes acumulados', linewidth=0.8)

    plot_timestamp(constants.VIDEO_PUBLISHED, 'Video publicado', 'indianred')
    format_date()

    plt.xlabel('Día')
    plt.ylabel('Likes')
    plt.colorbar()
    plt.legend()
    plt.show()


# %%
