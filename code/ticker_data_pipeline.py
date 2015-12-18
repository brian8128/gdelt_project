from code.CONSTANTS import PROJECT_HOME

import datetime
import calendar
import pandas as pd
import os


def get_timestamp(s):
    '''
    Translates a string that looks like "%Y-%m-%dT%H:%M:%S" and is already in gmt
    into a timestamp
    '''
    d = datetime.datetime.strptime(s, "%Y-%m-%dT%H:%M:%S")
    return calendar.timegm(d.timetuple())


def unzip():
    pass


def clean_series(s, min_timestamp=1433000000, min_mean_price_dollars=10):
    '''
    :param s: the series to clean
    :param min_timestamp: cut off all values before this time
    :param min_mean_price_dollars: return none if the mean price is less than this
    :return: The cleaned series or None if the series is rejected
    '''
    if s.mean() < min_mean_price_dollars:
        return None

    s = s[s.index > min_timestamp]
    return s


def get_series_list_from_files(limit=100,
                      download_month='201512',
                      freq='hourly',
                      region='us',
                      market='nasdaq stocks',
                      min_timestamp=1433000000,
                      min_mean_price_dollars=10
                      ):

    path = [PROJECT_HOME,
            'data/stooq',
            download_month,
            'data/',
            freq]
    if region is not None:
        path.append(region)

    if market is not None:
        path.append(market)

    g = os.walk('/'.join(path))
    count = 0
    series = []
    for triple in g:
        for filename in triple[2]:
            try:
                symbol = filename.split('.')[0]
                path = '/'.join([triple[0], filename])

                df = pd.read_csv(path)
                df['timestamp'] = (df['Date'] + 'T' + df['Time']).apply(get_timestamp)
                df = df.set_index(['timestamp'])
                # Add a new column with the correct name
                df[symbol] = df.Open
                s = clean_series(df[symbol],
                                 min_timestamp=min_timestamp,
                                 min_mean_price_dollars=min_mean_price_dollars)
                if s is not None:
                    series.append(s)
                    count += 1
            except Exception:
                # It seems that this is rare.  Not part of MVP if important at all.
                pass

            # TODO: Guido says I should refactor this.  But how?
            if count >= limit:
                break;
        if count >= limit:
            break;

    return series