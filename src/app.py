# noqa: E501
import io

import dash
import flask
import pandas as pd
import plotly.graph_objs as go
from dash.dependencies import Input, Output
from flask import send_file

from const import INDEX_DATE
from layout.layout import build_ui

server = flask.Flask(__name__)
app = dash.Dash(__name__, server=server)
app.title = "Stocks Summary"
app.layout = build_ui()


@app.callback(Output("my-graph", "figure"), [Input("my-dropdown", "value")])
def update_inidividual_stock_graph(selected_dropdown_value, data):

    equity_traces = []

    for stock in selected_dropdown_value:
        equity_traces.append(
            go.Scatter(
                x=data.rebased_prices.index.tolist(),
                y=data.rebased_prices[stock].values.tolist(),
                mode="lines",
                opacity=0.7,
                name=stock,
                textposition="bottom center",
            )
        )

    # data = [val for sublist in traces for val in sublist]
    figure = {
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
            title=f"Stock prices for {', '.join(i for i in selected_dropdown_value)} rebased to {INDEX_DATE}",
            xaxis=dict(
                title="Date",
                rangeselector=dict(
                    buttons=list(
                        [
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
                    )
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
                title=f"Stock price (indexed at {INDEX_DATE})",
                autorange=True,
                fixedrange=False,
            ),
        ),
    }
    return figure


@app.server.route("/download_excel/")
def download_excel():
    # Create DF

    raw_prices = pd.DataFrame(data=data.prices)
    rebased_prices = pd.DataFrame(data=data.rebased_prices)

    # Convert DF
    strIO = io.BytesIO()
    excel_writer = pd.ExcelWriter(strIO, engine="xlsxwriter")
    raw_prices.to_excel(excel_writer, sheet_name="raw_prices")
    rebased_prices.to_excel(excel_writer, sheet_name="rebased_prices")
    excel_writer.save()
    excel_data = strIO.getvalue()  # noqa: F841
    strIO.seek(0)

    return send_file(strIO, attachment_filename="raw_data.xlsx", as_attachment=True)


if __name__ == "__main__":

    app.run_server(port=2000, debug=True, threaded=True)
