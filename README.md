INTRO:

The stock market rewards those who are able to add information to it.  If an investor knows that something will happen, is happening or did happen that will increase the value of a particular stock, he or she should, and often does, invest in that stock, increasing the price up to its proper value and inadvertently *adding information* to the market - informing the world that something good has happened for that company.  If we are correct in interpreting trades as adding information to the market then there is an entire multi billion dollar industry devoted to encoding information in the stock market.  This project will attempt to get the information out again and see what changes in the market can tell us about current events.  Can we report the news faster than the traditional media just by looking at the market?  Is it possible to ‘break stories’ that are not yet public knowledge by looking at market behavior?  

DATA:

  STOCK:

http://stooq.com/db/h/ has 5 minute stock data from all over the world available for free from the past 30 days and hourly data going back 1 year.  Daily data goes back even further.  Here’s a sample from 2014 for Tofutti Brands Inc.

Date,Time,Open,High,Low,Close,Volume,OpenInt

2014-11-14,16:00:00,5.87,6.06,5.75,6.06,2600,0

2014-11-14,17:00:00,6.16,6.18,6.16,6.18,1200,0

2014-11-14,22:00:00,6.0,6.0,5.93,5.93,450,0

  WORLD EVENTS:

The GDELT Project maintains an impressive database of world events which can be downloaded from http://data.gdeltproject.org/events/index.html.  The GDELT table contains over 50 columns including date, actors, type of event, severity, location and a link to a news
story about the event.  Here’s a small sample of just a few of the columns (eclipses mine).  

20041116,AFGINSTAL,TALIBAN,"Islamabad, Isla...",33.7,73.1667,http://dailystar.com.lb/N...
20041116,AFGINSTAL,TALIBAN,"Kabul, Kabol, A...",34.5167,69.1833,http://dailystar.com.lb/N...
20041116,AFGINSTAL,TALIBAN,"Islamabad, Isla...",33.7,73.1667,http://dailystar.com.lb/N...
20041116,AFGINSTAL,TALIBAN,"Kabul, Kabol, A...",34.5167,69.1833,http://dailystar.com.lb/N...
20041116,AFR,AFRICA,"Pretoria, Gaute...",-25.7069,28.2294,http://africanbrains.net/...

RESEARCH OUTLINE:

We will begin by analyzing stock market data using principle component analysis, analogous in many ways to a movie recommender system.  The ‘users’ are stocks and the ‘movies’ are time intervals.  A stocks ‘star rating’ of the time interval is its percent change during the time interval.  We will do this for various time intervals and various markets and find the principle components of stock market movements.  We will analyze the most important stocks in each of the top k principle components and find meaningful descriptions of these components.  We may focus on a specific market and a specific time interval.  We will report on how much of the movement of the market can be explained by these principle components.  For example: “Dell has gone up significantly more than other computer manufactures.” We will perform clustering on time intervals using the principle components as features.  This first part could be useful to investors wishing to diversify.  We will be able to say which stocks behave most differently to which other stocks.  

After we have a reasonable understanding of the principle components of the stock market we will attempt to find correlations between stock prices and world events.  We anticipate two major difficulties in this analysis.  First, GDELT only reports on the day an event occurred but the market may react on a significantly faster timescale.  Second many events take place within a single day.  To overcome these difficulties we will at first focus on events rated as most significant by GDELT.  The most severe events may happen less than once a day and will likely have the strongest signal in the market.  We will try various approaches to correlate these events with market data including attempting to match certain types of events with the clusters mentioned above.  We will attempt to predict more specific times of day when events occurred.  Time permitting, we may use NLP on links to news articles in clusters to predict what keywords may appear in forthcoming articles about recent/ongoing world events.  

DELIVERABLES:

We will deliver an app that helps users understand what we can learn from the behavior of the market over the past (five minutes/hour/day/week).  Users will be presented with a graph or graphs of the principle components of market over the most recent time interval.  These will be labeled with very brief summaries of the components.  Users may be able to find more information about the principle components by following a link.  We will report on how much and the nature of the change in the market not explained by the principle components, including a quantile rank.  This will give a measure of how unusual market behavior was over the time interval.  

Finally, we will predict what sort world events may have happened over the past time interval based on market behavior.  For example: “Trading over the past hour (weakly, strongly) suggests pessimism about the stability of the EU - perhaps some negative political event has taken place,” or perhaps “The price of corn has increased by an unusual amount. There may have been predictions of bad weather in the US midwest.”  In essence, we conjecture that information about world events is encoded and made publicly available in stock market data before the media is able to report on it.  We are hoping to give faster, albeit less precise, reporting of the news than the traditional media.  The presentation will depend on what type of predictions we’re able to make.  




