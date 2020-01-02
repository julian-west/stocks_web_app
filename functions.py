
import pandas as pd
import ffn
import numpy as np

import plotly
import plotly.graph_objs as go
import seaborn as sns
import matplotlib.pyplot as plt
import calmap

from const import STOCKS, COMPANY_NAMES, WEIGHTS, START_DATE, INDEX_DATE


class PerformanceReport:

    def __init__(self):
        self.get_data()

    def get_data(self):

        print("Collecting data..")
        prices = ffn.get(STOCKS, start=START_DATE)
        print("Data collected!")
        self.prices = prices

        self.create_index()

        self.generate_monthly_returns_table()

        self.current_index_value = self.rebased_prices['index'].iloc[-1]

        self.daily_index_pct_change = (
            (self.current_index_value/self.rebased_prices['index'].iloc[-2])-1)*100

        # note these should be calculated properly in future...
        self.weekly_index_pct_change = (
            (self.current_index_value/self.rebased_prices['index'].iloc[-5])-1)*100
        self.monthly_index_pct_change = (
            (self.current_index_value/self.rebased_prices['index'].iloc[-28])-1)*100

        self.calc_year_over_year_growth()

    def create_index(self):

        def rebase_timeseries(prices, date):
            return prices / prices.loc[date, :] * 100

        rebased_prices = rebase_timeseries(
            self.prices, INDEX_DATE)  # normalize dataframe
        rebased_prices_index = rebased_prices.multiply(
            WEIGHTS, axis=1)  # apply weights
        rebased_prices['index'] = rebased_prices_index.sum(
            axis=1)  # sum up weights to get the overall index
        # rebased_prices['log_index'] = np.log(rebased_prices['index'])

        self.rebased_prices = rebased_prices
        self.index_stats = self.rebased_prices['index'].calc_stats()

    def generate_monthly_returns_table(self):

        monthly_rtns_df = pd.DataFrame.from_dict(
            dict(self.index_stats.monthly_returns), orient='index')

        monthly_rtns_df = monthly_rtns_df.groupby(
            by=[monthly_rtns_df.index.year, monthly_rtns_df.index.month]).sum().unstack().fillna(0)

        # format as % for final table
        monthly_rtns_df = monthly_rtns_df.apply(
            lambda x: (x*100).map('{:,.2f}%'.format), axis=1)

        monthly_rtns_df = monthly_rtns_df.reset_index()
        monthly_rtns_df.columns = ['Year', 'Jan', 'Feb', 'Mar', 'Apr',
                                   'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']

        self.monthly_returns_table = monthly_rtns_df

    def plot_performance_chart(self):
        """Plot index"""
        trace_equity = go.Scatter(
            x=self.rebased_prices.index.tolist(),
            y=self.rebased_prices['index'].values.tolist(),
            name='index',
            yaxis='y',
            line=dict(color='#2F80ED'),
            fill="tozeroy")

        layout = go.Layout(
            autosize=True,
            legend=dict(orientation="h"),
            yaxis=dict(
                title=f"Index (rebased {INDEX_DATE})",
                showgrid=True,
                linecolor='#dae4f5',
                rangemode='tozero'
            ),
            xaxis=dict(
                range=([self.rebased_prices.index.max() - pd.DateOffset(months=24),
                        self.rebased_prices.index.max() + pd.DateOffset(months=6)]),
                showgrid=False,
                linecolor='#dae4f5'
            ),
            hovermode='x',
            plot_bgcolor='#ffffff',
            margin={'t': 40, 'b': 50},
            height=350,
            shapes=[dict(type='line',
                         xref='x',
                         yref='y',
                         x0= INDEX_DATE,
                         y0=0,
                         x1= INDEX_DATE,
                         y1=140,
                         line=dict(color='#dae4f5',
                                   dash='dot')
                         )
                    ])

        perf_chart = go.Figure(dict(data=[trace_equity],
                                    layout=layout))
        return perf_chart

    def plot_swarm_plot(self):
        """Plot seaborn swarm plot to show growth of different stocks on a linear scale"""

        def get_swarm_coords(returns):
            """Get x,y coordinates for swarm plot from returns dictionary"""

            ax = sns.swarmplot(list(returns.values()))
            coords = ax.collections[0].get_offsets()
            x, y = coords[:, 0], coords[:, 1]

            names = []

            for coord in x:
                for k, v in returns.items():
                    if round(v, 4) == round(coord, 4):
                        names.append(k)

            return names, x, y

        returns = dict(self.rebased_prices.pct_change().iloc[-1, :])

        # coordinates and names for scatter plot
        names, x_coords, y_coords = get_swarm_coords(returns)

        descriptions = [names[i] + "<br>" +
                        str(round(coord*100, 2)) + "%" for i, coord in enumerate(x_coords)]
        colors = ['darksalmon' if x < 0 else 'seagreen' for x in x_coords]

        data = go.Scatter(
            x=x_coords,
            y=y_coords,
            mode='markers+text',
            marker=dict(color=colors),
            hovertext=descriptions,
            hoverinfo='text',
            text=[x if x == names[0] or x == names[-1] else "" for x in names],
            textposition='top center')

        layout = go.Layout(
            plot_bgcolor='#fff',
            yaxis=dict(
                showticklabels=False,
                showgrid=False,
                range=[-0.1, 0.1]),
            xaxis=dict(
                range=[-0.1, 0.1],
                tickformat="%",
                title="Stock Price Growth"),
            margin={'t': 5},
            height=200,
            shapes=[dict(type='line',
                         xref='x',
                         yref='y',
                         x0=0,
                         y0=-0.5,
                         x1=0,
                         y1=0.5,
                         line=dict(color='#56CCF2',
                                   dash='dot')
                         )])

        swarm_plot = go.Figure(dict(data=data, layout=layout))

        return swarm_plot

    def calc_year_over_year_growth(self):
        yoy_growth = self.rebased_prices.resample('D').sum()
        yoy_growth = yoy_growth.replace(0, method='ffill')
        yoy_growth = yoy_growth.groupby(
            [yoy_growth.index.day, yoy_growth.index.month]).pct_change()
        yoy_growth = yoy_growth.dropna(axis=0)
        yoy_growth['28dayMA'] = yoy_growth['index'].rolling(window=28).mean()

        self.yoy_growth = yoy_growth

    def plot_yoy_growth(self):

        # CALENDAR MAP IMAGE
        calmap.calendarplot(self.yoy_growth.iloc[self.yoy_growth.index.year > 2016]['index'], monthticks=1, daylabels='MTWTF',
                            dayticks=[0, 2, 4], cmap='RdYlGn',
                            linewidth=0.2,
                            yearascending=False,
                            yearlabel_kws=dict(color='#696969'),
                            fig_kws=dict(figsize=(12, 8)))

        plt.savefig('assets/yoy_calmap.png')

        # YOY GROWTH - show different colour for positive and negative yoy growth
        postive_growth = go.Scatter(
            y=[0 if x < 0 else x for x in self.yoy_growth['28dayMA']],
            x=self.yoy_growth.index,
            fill='tozeroy',
            line=dict(color='#2F80ED'))

        negative_growth = go.Scatter(
            y=[0 if x > 0 else x for x in self.yoy_growth['28dayMA']],
            x=self.yoy_growth.index,
            fill='tozeroy')

        baseline = go.Scatter(
            y=[0 for x in self.yoy_growth.index],
            x=self.yoy_growth.index,
            line=dict(color='black'))

        layout = go.Layout(
            plot_bgcolor='#ffffff',
            yaxis=dict(tickformat="%"),
            xaxis=dict(
                range=([self.yoy_growth.index.min(),
                        self.yoy_growth.index.max() + pd.DateOffset(months=6)])
            ),
            showlegend=False,
            hovermode='x')

        yoy_growth_chart = go.Figure(
            data=[postive_growth, negative_growth, baseline], layout=layout)

        return yoy_growth_chart

    def plot_drawdown(self):
        """Plot drawndown series of the index"""
        data = go.Scatter(
            y=self.index_stats.drawdown.values,
            x=self.index_stats.drawdown.index)

        layout = go.Layout(
            plot_bgcolor='#ffffff',
            margin={'t': 5},
            yaxis=dict(tickformat="%",
            title="% Drawdown from last peak"),
            xaxis=dict(
                range=([self.index_stats.drawdown.index.min(),
                        self.index_stats.drawdown.index.max() + pd.DateOffset(months=6)])
            ),
            showlegend=False,
            hovermode='x'
        )
        drawdown_chart=go.Figure(data = data,layout=layout)

        return drawdown_chart
