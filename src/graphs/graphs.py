import pandas as pd
import plotly.graph_objs as go

from data.data import StockData


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

    perf_chart = go.Figure(dict(data=[trace_equity], layout=layout))
    return perf_chart
