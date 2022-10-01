import dash_bootstrap_components as dbc
from dash import html

from data.data import StockData
from data.summary import SummaryData
from layout.individual_stock_analysis import individual_stocks
from layout.stock_summary import stock_summary
from layout.tabs import tabs


def header() -> dbc.Row:
    return dbc.Row(
        [
            html.H3("VACUUM PROCESSING INDEX", style={"text-align": "center"}),
            html.Div(
                [
                    html.Span(
                        [
                            html.A(
                                "Raw Data",
                                href="/download_excel/",
                                style={"margin-right": "10px"},
                            ),
                            html.I(className="fa fa-arrow-circle-down"),
                        ],
                        className="button",
                    )
                ]
            ),
        ],
        className="header",
        style={"display": "grid"},
    )


def footer():
    return dbc.Row([html.Footer(html.P("Julian West"))], className="footer")


def build_ui(data: StockData, summary: SummaryData):
    return html.Main(
        [
            header(),
            dbc.Container(
                [
                    stock_summary(data, summary),
                    tabs(summary),
                    individual_stocks(summary),
                    footer(),
                ]
            ),
        ]
    )
