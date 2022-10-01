import pandas as pd

from data.data import StockData


class SummaryData:
    def __init__(self, data: StockData):
        self.data = data
        self.current_index_value = self.data.rebased_prices["index"].iloc[-1]

    @property
    def daily_growth(self):
        return (
            (self.current_index_value / self.data.rebased_prices["index"].iloc[-2]) - 1
        ) * 100

    @property
    def weekly_growth(self):
        return (
            (self.current_index_value / self.data.rebased_prices["index"].iloc[-5]) - 1
        ) * 100

    @property
    def monthly_growth(self):
        """calculate monthly returns"""
        return (
            (self.current_index_value / self.data.rebased_prices["index"].iloc[-28]) - 1
        ) * 100

    @property
    def yoy_growth(self):
        """calculate yoy growth"""
        yoy_growth = self.data.rebased_prices.resample("D").sum()
        yoy_growth = yoy_growth.replace(0, method="ffill")
        yoy_growth = yoy_growth.groupby(
            [yoy_growth.index.day, yoy_growth.index.month]
        ).pct_change()
        yoy_growth = yoy_growth.dropna(axis=0)
        yoy_growth["28dayMA"] = yoy_growth["index"].rolling(window=28).mean()

        return yoy_growth

    @property
    def monthly_returns_table(self):
        """Gernerate table of monthly returns"""

        monthly_rtns_df = pd.DataFrame.from_dict(
            dict(self.data.stats.monthly_returns), orient="index"
        )

        monthly_rtns_df = (
            monthly_rtns_df.groupby(
                by=[monthly_rtns_df.index.year, monthly_rtns_df.index.month]
            )
            .sum()
            .unstack()
            .fillna(0)
        )

        # format as % for final table
        monthly_rtns_df = monthly_rtns_df.apply(
            lambda x: (x * 100).map("{:,.2f}%".format), axis=1
        )

        monthly_rtns_df = monthly_rtns_df.reset_index()
        monthly_rtns_df.columns = [
            "Year",
            "Jan",
            "Feb",
            "Mar",
            "Apr",
            "May",
            "Jun",
            "Jul",
            "Aug",
            "Sep",
            "Oct",
            "Nov",
            "Dec",
        ]

        return monthly_rtns_df
