import calmap
import matplotlib.pyplot as plt
import pandas as pd
import plotly.express as ex
import plotly.graph_objs as go

from data.data import StockData
from data.summary import SummaryData


def plot_index_chart(data: StockData):
    trace_equity = go.Scatter(
        x=data.rebased_prices.index.tolist(),
        y=data.rebased_prices["index"].values.tolist(),
        name="index",
        yaxis="y",
        line=dict(color="#2F80ED"),
        fill="tozeroy",
    )

    layout = go.Layout(
        autosize=True,
        legend=dict(orientation="h"),
        yaxis=dict(
            title=f"Index (rebased {data.index_date})",
            showgrid=True,
            linecolor="#dae4f5",
            rangemode="tozero",
        ),
        xaxis=dict(
            range=(
                [
                    data.rebased_prices.index.max() - pd.DateOffset(months=24),
                    data.rebased_prices.index.max() + pd.DateOffset(months=6),
                ]
            ),
            showgrid=False,
            linecolor="#dae4f5",
        ),
        hovermode="x",
        plot_bgcolor="#ffffff",
        margin={"t": 40, "b": 50},
        height=350,
        shapes=[
            dict(
                type="line",
                xref="x",
                yref="y",
                x0=data.index_date,
                y0=0,
                x1=data.index_date,
                y1=140,
                line=dict(color="#dae4f5", dash="dot"),
            )
        ],
    )

    return go.Figure(dict(data=[trace_equity], layout=layout))


def plot_yoy_growth(summary: SummaryData):

    # CALENDAR MAP IMAGE
    calmap.calendarplot(
        summary.yoy_growth.iloc[summary.yoy_growth.index.year > 2016]["index"],
        monthticks=1,
        daylabels="MTWTF",
        dayticks=[0, 2, 4],
        cmap="RdYlGn",
        linewidth=0.2,
        yearascending=False,
        yearlabel_kws=dict(color="#696969"),
        fig_kws=dict(figsize=(12, 8)),
    )

    plt.savefig("./src/assets/yoy_calmap.png")

    # YOY GROWTH - show different colour for positive and negative yoy growth
    postive_growth = go.Scatter(
        y=[max(x, 0) for x in summary.yoy_growth["28dayMA"]],
        x=summary.yoy_growth.index,
        fill="tozeroy",
        line=dict(color="#2F80ED"),
    )

    negative_growth = go.Scatter(
        y=[min(x, 0) for x in summary.yoy_growth["28dayMA"]],
        x=summary.yoy_growth.index,
        fill="tozeroy",
    )

    baseline = go.Scatter(
        y=[0 for _ in summary.yoy_growth.index],
        x=summary.yoy_growth.index,
        line=dict(color="black"),
    )

    layout = go.Layout(
        plot_bgcolor="#ffffff",
        yaxis=dict(tickformat=".0%"),
        xaxis=dict(
            range=(
                [
                    summary.yoy_growth.index.min(),
                    summary.yoy_growth.index.max() + pd.DateOffset(months=6),
                ]
            )
        ),
        showlegend=False,
        hovermode="x",
    )

    return go.Figure(data=[postive_growth, negative_growth, baseline], layout=layout)


def plot_drawdown_chart(summary: SummaryData):
    """Plot drawndown series of the index"""

    drawdown = summary.data.stats.drawdown
    data = go.Scatter(y=drawdown.values, x=drawdown.index)

    layout = go.Layout(
        plot_bgcolor="#ffffff",
        margin={"t": 5},
        yaxis=dict(tickformat=".0%", title="% Drawdown from last peak"),
        xaxis=dict(
            range=(
                [
                    drawdown.index.min(),
                    drawdown.index.max() + pd.DateOffset(months=6),
                ]
            )
        ),
        showlegend=False,
        hovermode="x",
    )
    return go.Figure(data=data, layout=layout)


def plot_swarm_chart(summary: SummaryData):
    """Plot seaborn swarm plot to show growth of different stocks on a linear scale"""

    # TODO: Fix formatting

    returns = summary.data.rebased_prices.pct_change().iloc[-1, :]

    # descriptions = [
    #     names[i] + "<br>" + str(round(coord * 100, 2)) + "%"
    #     for i, coord in enumerate(x_coords)
    # ]
    colors = ["darksalmon" if x < 0 else "seagreen" for x in returns]

    # data = go.Scatter(
    #     x=x_coords,
    #     y=y_coords,
    #     mode="markers+text",
    #     marker=dict(color=colors),
    #     hovertext=descriptions,
    #     hoverinfo="text",
    #     text=[x if x == names[0] or x == names[-1] else "" for x in names],
    #     textposition="top center",
    # )

    # swarm_plot = go.Figure(dict(data=data, layout=layout))

    swarm_plot = ex.strip(x=returns, color_discrete_sequence=colors)
    swarm_plot.update_layout(
        plot_bgcolor="#fff",
        yaxis=dict(showticklabels=False, showgrid=False, range=[-0.1, 0.1]),
        xaxis=dict(range=[-0.1, 0.1], tickformat=".2%", title="Stock Price Growth"),
        margin={"t": 5},
        height=200,
        shapes=[
            dict(
                type="line",
                xref="x",
                yref="y",
                x0=0,
                y0=-0.5,
                x1=0,
                y1=0.5,
                line=dict(color="#56CCF2", dash="dot"),
            )
        ],
    )

    return swarm_plot


def plot_individual_stock_prices(data: StockData, stocks):

    equity_traces = [
        go.Scatter(
            x=data.rebased_prices.index.tolist(),
            y=data.rebased_prices[stock].values.tolist(),
            mode="lines",
            opacity=0.7,
            name=stock,
            textposition="bottom center",
        )
        for stock in stocks
    ]

    return {
        "data": equity_traces,
        "layout": go.Layout(
            colorway=[
                "#d53e4f",
                "#f46d43",
                "#fdae61",
                "#fee08b",
                "#e6f598",
                "#abdda4",
                "#66c2a5",
                "#3288bd",
            ],
            height=600,
            title=f"Stock prices for {', '.join(stocks)} rebased to {data.index_date}",
            xaxis=dict(
                title="Date",
                rangeselector=dict(
                    buttons=[
                        {
                            "count": 1,
                            "label": "1M",
                            "step": "month",
                            "stepmode": "backward",
                        },
                        {
                            "count": 6,
                            "label": "6M",
                            "step": "month",
                            "stepmode": "backward",
                        },
                        {"step": "all"},
                    ]
                ),
                range=(
                    [
                        data.rebased_prices.index.max() - pd.DateOffset(months=24),
                        data.rebased_prices.index.max() + pd.DateOffset(months=6),
                    ]
                ),
                rangeslider={"visible": True},
                type="date",
            ),
            yaxis=dict(
                title=f"Stock price (indexed at {data.index_date})",
                autorange=True,
                fixedrange=False,
            ),
        ),
    }
