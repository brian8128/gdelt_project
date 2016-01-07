from CONSTANTS import PROJECT_HOME, TICKER_PICKLE_PATH

import datetime
import calendar
import os
from pickle_helper import pickle_, unpickle_

import pandas as pd


def get_timestamp(s):
    '''
    Translates a string that looks like "%Y-%m-%dT%H:%M:%S" and is already in gmt
    into a timestamp
    '''
    d = datetime.datetime.strptime(s, "%Y-%m-%dT%H:%M:%S")
    return calendar.timegm(d.timetuple())


def unzip():
    pass


def clean_series(s, min_timestamp=1433000000, min_mean_price_dollars=10, max_price_dollars=10000):
    '''
    :param s: the series to clean
    :param min_timestamp: cut off all values before this time
    :param min_mean_price_dollars: return none if the mean price is less than this
    :return: The cleaned series or None if the series is rejected
    '''
    if s.mean() < min_mean_price_dollars:
        return None

    if s.max() > max_price_dollars:
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


def create_ticker_price_df():
    '''
    Loads a dataframe of nasdaq ticker symbols from disk.
    '''
    # TODO: Decide one place to set the default limit.  Currently we have a default
    # limit in two places.
    s = get_series_list_from_files(limit=5000, min_mean_price_dollars=10)
    df = pd.DataFrame(data=s).T
    # Deal with missing values
    df = df.interpolate().fillna(method='bfill')
    return df


def pickle_ticker_price_df(ticker_price_df):
    """
    Convenience function for calling pickle_helper.pickle_()
    """
    return pickle_(ticker_price_df, TICKER_PICKLE_PATH)


def unpickle_ticker_price_df():
    """
    Convenience function for calling pickle_helper.unpickle_()
    """
    return unpickle_(TICKER_PICKLE_PATH)


def diff_df(df, variance_quantile_cutoff=0.97, max=2):
    '''
    Calculates a the percent change of each column of the data frame.
    Performs clipping and removes the columns with the most variance.

    variance_quantile_cutoff - Remove columns whose variance is higher than this.
    For example if there are 100 columns and variance_quantile_cutoff is set to 0.97
    this function will remove the 3 columns with the highest variance
    If set to None no columns will be removed.
    max - max percent change for any time interval.  We clip the data to be between -max and max
    If set to None no clipping will transpire
    '''

    dif_df = df.pct_change().fillna(0.)
    if max:
        dif_df = dif_df.clip(-max, max)
    if variance_quantile_cutoff:
        variance_cutoff = dif_df.var().quantile(variance_quantile_cutoff)
        c = dif_df.columns[dif_df.var() < variance_cutoff]
        dif_df = dif_df[c]
    return dif_df