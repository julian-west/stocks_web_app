from dataclasses import dataclass
from typing import Any

import ffn

from const import INDEX_DATE, START_DATE, STOCKS


@dataclass
class StockData:
    def __init__(
        self,
        start_date: str = START_DATE,
        index_date: str = INDEX_DATE,
        input_dict: list[dict[str, Any]] = STOCKS,
    ):

        self.start_date = start_date
        self.index_date = index_date
        self.input_dict = input_dict

        self.process_input()
        self.get_data()
        self.create_index()

    def process_input(self):
        self.company_names = [row["company_name"] for row in self.input_dict]
        self.tickers = [row["ticker"] for row in self.input_dict]
        self.weightings = [row["weighting"] for row in self.input_dict]

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
