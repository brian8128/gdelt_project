Data download.  

GDELT:

http://data.gdeltproject.org/events/index.html

Stock Data:

curl "http://www.google.com/finance/getprices?i=60&p=100d&f=d,o,h,l,c,v&df=cpct&q=IBM" > ibm.csv
http://www.quantshare.com/sa-426-6-ways-to-download-free-intraday-and-tick-data-for-the-us-stock-market
http://www.networkerror.org/component/content/article/1-technical-wootness/44-googles-undocumented-finance-api.html

http://www.google.com/finance/getprices?i=3600&p=1d&f=d,o,h,l,c,v&df=cpct&q=IBM

EXCHANGE%3DNYSE
MARKET_OPEN_MINUTE=570
MARKET_CLOSE_MINUTE=960
INTERVAL=3600
COLUMNS=DATE,CLOSE,HIGH,LOW,OPEN,VOLUME
DATA=
TIMEZONE_OFFSET=-300
a1449673200,138.46,138.68,137.3,137.38,504042
1,139.53,139.84,138.42,138.43,560077
2,137.8,139.57,137.62,139.54,460836
3,136.4244,137.92,136.26,137.79,486304
4,136.84,137.05,136.23,136.405,428124
5,136.57,136.94,136.51,136.86,314205
6,136.64,137.13,136.54,136.58,917250

a1449673200 is 'a' + {unix_time}


