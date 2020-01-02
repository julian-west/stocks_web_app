import pandas as pd


START_DATE = '2012-01-01'
INDEX_DATE = '2019-12-27'


df = pd.read_csv("assets/data/stocks.csv")
STOCKS = list(df['ticker'].values)
COMPANY_NAMES = list(df['company name'].values)
WEIGHTS = list(df['weighting'].values)

STOCK_LIST = []
for i,stock in enumerate(STOCKS):
    STOCK_LIST.append({'label':COMPANY_NAMES[i],'value':STOCKS[i]})
