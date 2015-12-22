import os

import requests as r
import pandas as pd
import numpy as np

from sklearn.feature_extraction.text import TfidfVectorizer

from code.CONSTANTS import PROJECT_HOME, TICKER_FILE_PATH, DESCRIPTION_FILE_PATH

# TODO: Factor both data_pipeline files into two files.
# First file mananges raw data, second file cleans the raw data.
# Currently we have raw data management mixed in with data cleaning


def get_nasdaq_tickers():
    '''
    Get a list of all the nasdaq ticker symbols in the dataset
    '''
    # TODO: Move the data into PROJECT_HOME/data/raw
    d = "/Users/Brian/Data/gdelt/raw/data/hourly/us/nasdaq stocks"
    g = os.walk(d)
    symbols = []

    for triple in g:
        for filename in triple[2]:
            try:
                symbol = filename.split('.')[0]
                symbols.append(symbol)
            except Exception:
                # It seems that this is rare.  Not part of MVP if important at all.
                # fuck it
                pass
    return sorted(symbols)


def write_nasdaq_ticker_file():
    '''
    Create a file with the list of all the nasdaq ticker symbols if it doesn't already
    exist.
    '''
    filename = PROJECT_HOME + "data/company/nasdaq_tickers"
    if not os.path.isfile(filename):
        print "No ticker name file found.  Creating ticker file at {}.".format(filename)
        tickers = get_nasdaq_tickers()
        with open(filename, 'w') as f:
            for t in tickers:
                f.write(t + '\n')
    else:
        print "ticker name file already exists at {}, doing nothing.".format(filename)


def get_nasdaq_desc(ticker):
    '''
    Given a ticker of a nasdaq stock fetches a company description from the web.
    This is a bit slow on account of having to wait for the page to load
    '''
    try:
        # Sometimes it's meaningful and sometimes it's just legalease.
        # TODO: There is a link on this page to a longer description.
        # We could try following this link to get a longer and perhaps more
        # meaningful company description
        s = r.get("http://www.nasdaq.com/symbol/{}".format(ticker)).content
        regex1 = "<h2>Company Description (as filed with the SEC)</h2>"
        i = s.index(regex1)
        s = s[i:]
        regex = "<p>"
        i = s.index(regex)
        s = s[i+3:]
        regex = "<"
        i = s.index(regex)
        return s[:i].replace('\n', ' ').replace('\t', ' ').replace('&nbsp;', ' ')
        #return '"' + s[i+70:i+1000].replace('\n', ' ').replace('\t', ' ') + '"'
    except Exception:
        # Something went wrong.  Probably network or the page doesn't exist
        # It's fine if we only get descriptions for 95% of companies.
        return ''


def write_company_description_file(limit=100):
    '''
    We want to create a csv file with ticker names and descriptions.
    Read in the ticker symbols from the file, look up their description on the web,
    write the description to the tsv file

    A known issue is if the file already exists but is malormed (eg. empty)
    this will not work.  In that case delete the file and start over
    '''
    tickers_full_path = PROJECT_HOME + TICKER_FILE_PATH
    descriptions_full_path = PROJECT_HOME + DESCRIPTION_FILE_PATH
    if not os.path.isfile(tickers_full_path):
        raise Exception("Couldn't find the file with ticker names at {}.").format(tickers_full_path)

    with open(tickers_full_path) as tf:
        tickers = tf.read().splitlines()

    # We may have already done work.  Find the index where we left off in
    # the ticker file
    if os.path.isfile(descriptions_full_path):
        with open(descriptions_full_path) as f:
            company_df = pd.read_csv(f,
                                     sep='\t',
                                     header=None)
        last_completed_ticker = company_df[0].iloc[-1]
        idx = tickers.index(last_completed_ticker)
    else:
        idx = 0

    with open(descriptions_full_path, 'a') as df:
        for t in tickers[ idx : min(len(tickers), idx + limit) ]:
            d = get_nasdaq_desc(t)
            # descriptions are not allowed to have \t or \n characters
            df.write(t + '\t' + d + '\n')


def get_company_df_from_file():
    '''
    :return: company_df - data frame with company info including tfidf of descriptsion,
                features, - the vocabulary for the tfidf column of company_df
    '''
    # TODO: Factor this into three functions.
    # it is doing three things, reading the data, cleaning it and tfidfing it.
    with open(PROJECT_HOME + DESCRIPTION_FILE_PATH) as f:
        company_df = pd.read_csv(f,
                             sep='\t',
                             header=None)
    company_df.columns = ['ticker', 'description']
    company_df = company_df.dropna().set_index('ticker')
    # Drop companies that don't have a good description
    company_df = company_df[company_df.description.apply(lambda x: len(x) > 100)]

    tv = TfidfVectorizer(stop_words='english')
    tfidf = tv.fit_transform(company_df.description)
    features = np.array(tv.get_feature_names())
    # Change the 2d array to a list of 1d arrays
    tfidf = map(lambda x: x.flatten(), np.vsplit(tfidf.toarray(), tfidf.shape[0]))
    company_df['tfidf'] = tfidf
    return company_df, features

if __name__ == "__main__":
    write_company_description_file(limit=5000)