
from datetime import datetime
import locale

import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import pandas as pd

import constants

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
def plot_tweets_per_hashtags(counts: pd.DataFrame) -> None:
    fig, ax  = plt.subplots()
    xdates = counts['date']
    for hashtag in list(counts.columns[1:]):
        ycount = counts[hashtag]
        ax.plot(xdates, ycount, label=f'#{hashtag}', linewidth='0.8')

    plot_timestamp(constants.VIDEO_PUBLISHED, 'Video publicado', 'indianred')

    ax.xaxis.set_major_formatter(mdates.DateFormatter('%d-%b'))
    ax.grid(True)
    ax.legend()

    fig.autofmt_xdate()

    plt.xlabel('Día')
    plt.ylabel('Tweets')
    plt.title('Cantidad de tweets por hashtag por día')
    plt.show()
