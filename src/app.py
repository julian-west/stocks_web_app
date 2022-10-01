import io

import dash
import flask
import pandas as pd
from dash.dependencies import Input, Output
from flask import send_file

from data.data import StockData
from data.summary import SummaryData
from graphs.graphs import plot_individual_stock_prices
from layout.layout import build_ui

server = flask.Flask(__name__)
app = dash.Dash(__name__, server=server)


@app.callback(Output("my-graph", "figure"), [Input("my-dropdown", "value")])
def update_inidividual_stock_graph(selected_dropdown_value):

    # TODO: don't reload data each time
    data = StockData()
    return plot_individual_stock_prices(data, selected_dropdown_value)


@app.server.route("/download_excel/")
def download_excel():

    # TODO: don't reload data each time
    data = StockData()

    # Create DF
    raw_prices = pd.DataFrame(data=data.data)
    rebased_prices = pd.DataFrame(data=data.rebased_prices)

    # Convert DF
    strIO = io.BytesIO()
    excel_writer = pd.ExcelWriter(strIO, engine="xlsxwriter")
    raw_prices.to_excel(excel_writer, sheet_name="raw_prices")
    rebased_prices.to_excel(excel_writer, sheet_name="rebased_prices")
    excel_writer.save()
    excel_data = strIO.getvalue()  # noqa: F841
    strIO.seek(0)

    return send_file(strIO, download_name="raw_data.xlsx", as_attachment=True)


if __name__ == "__main__":

    data = StockData()
    summary = SummaryData(data=data)
    app.title = "Stocks Summary"
    app.layout = build_ui(data, summary)

    app.run_server(port=2000, debug=True, threaded=True)
