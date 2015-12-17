import os
import requests as r

PROJECT_HOME = "/Users/Brian/workplace/galvanize/gdelt_project/"


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
    return symbols


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
        s = r.get("http://www.nasdaq.com/symbol/{}".format(ticker)).content
        regex = "<h2>Company Description (as filed with the SEC)</h2>"
        i = s.index(regex)
        return s[i+70:i+1000].replace('\n', ' ').replace('\t', ' ')
    except Exception:
        return None