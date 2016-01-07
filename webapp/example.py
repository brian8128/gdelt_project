from flask import Flask, render_template
from bokeh import embed
from bokeh.charts import Bar
import pandas as pd
import requests
app = Flask(__name__)

big_4_tickers=['GOOG', 'AMZN', 'AAPL', 'FB', 'MSFT']


def get_change(ticker):
    url = 'http://www.google.com/finance/getprices?i=3600&p=1d&f=d,o,h,l,c,v&df=cpct&q={}'.format(ticker)
    r = requests.get(url)
    # Most recent stock price
    new_price = float(r.content.split("\n")[7].split(',')[1])
    # Price an hour before that
    old_price = float(r.content.split("\n")[8].split(',')[1])

    return (new_price - old_price) / old_price * 100.


def get_big_4_change():
    changes = []
    for t in big_4_tickers:
        changes.append(get_change(t))
    return changes


def create_barchart():
    changes = get_big_4_change()
    df = pd.DataFrame()
    df['percent_change'] = changes
    df['tickers'] = big_4_tickers
    p = Bar(df, label='tickers', values='percent_change',
        title="Ticker Prices of Big 4 Tech Companies over the Past Hour",
        ylabel='% Change')
    return p


# home page
@app.route('/')
def index():
    chart = create_barchart()
    script, div = embed.components(chart)
    return render_template('index.html', script=script, div=div)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)



