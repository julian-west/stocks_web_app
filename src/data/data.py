from dataclasses import dataclass

import ffn

from const import INDEX_DATE, START_DATE, STOCKS, WEIGHTS


@dataclass
class StockData:
    def __init__(self):
        self.index_date = INDEX_DATE
        self.start_date = START_DATE
        self.tickers = STOCKS
        self.weightings = WEIGHTS

        self.get_data()
        self.create_index()

    def get_data(self):
        print("Collecting data..")
        self.data = ffn.get(self.tickers, start=self.start_date)
        print("Data collected!")

    def create_index(self):
        def rebase_timeseries(prices, date):
            return prices / prices.loc[date, :] * 100

        rebased_prices = rebase_timeseries(self.data, self.index_date)
        rebased_prices_index = rebased_prices.multiply(self.weightings, axis=1)
        rebased_prices["index"] = rebased_prices_index.sum(axis=1)

        self.rebased_prices = rebased_prices

    @property
    def current_index_value(self):
        return self.rebased_prices["index"].iloc[-1]

    @property
    def stats(self):
        return self.rebased_prices["index"].calc_stats()
