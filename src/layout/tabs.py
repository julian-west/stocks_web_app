import dash_bootstrap_components as dbc
import pandas as pd
from dash import dcc, html

from data.summary import SummaryData
from graphs.graphs import plot_drawdown_chart, plot_yoy_growth


def company_names_tab(summary: SummaryData) -> dbc.Tab:
    return dbc.Tab(
        [
            dbc.Table.from_dataframe(
                pd.DataFrame(summary.data.input_dict),
                striped=True,
                bordered=True,
                hover=True,
                responsive=True,
            ),
        ],
        label="Stocks in index",
        style={
            "text-align": "left",
            "padding": 10,
        },
    )


def yoy_growth_tab(summary: SummaryData) -> dbc.Tab:
    return dbc.Tab(
        [
            dbc.Row(
                [
                    html.H4(
                        "Year over year index growth - 28 day MA",
                        style={"padding": 10},
                    ),
                    dcc.Graph(figure=plot_yoy_growth(summary)),
                ]
            ),
            dbc.Row(
                [
                    html.H4(
                        "Calendar Growth Map",
                        style={"padding": 10},
                    ),
                    html.Img(
                        src="assets/yoy_calmap.png",
                        style={"padding": 10},
                    ),
                ]
            ),
        ],
        label="YoY Growth",
    )


def monthy_returns_tab(summary: SummaryData) -> dbc.Tab:
    return dbc.Tab(
        dbc.Table.from_dataframe(
            summary.monthly_returns_table,
            striped=True,
            bordered=True,
            hover=True,
            responsive=True,
        ),
        label="Index Monthly Returns",
    )


def drawdown_tab(summary: SummaryData) -> dbc.Tab:
    return dbc.Tab(
        [
            dbc.Row(
                [
                    html.H4(
                        "'Under-water Plot' - Drawdown Periods",
                        style={"padding": 10},
                    ),
                    dcc.Graph(figure=plot_drawdown_chart(summary)),
                ]
            ),
        ],
        label="Drawdown",
    )


def tabs(summary: SummaryData) -> dbc.Row:
    return dbc.Row(
        [
            dbc.Col(
                [
                    dbc.Card(
                        [
                            dbc.CardBody(
                                [
                                    dbc.Tabs(
                                        [
                                            company_names_tab(summary),
                                            yoy_growth_tab(summary),
                                            monthy_returns_tab(summary),
                                            drawdown_tab(summary),
                                        ]
                                    ),
                                ]
                            ),
                        ]
                    ),
                ]
            ),
        ]
    )
