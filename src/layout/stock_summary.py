import dash_bootstrap_components as dbc
from dash import dcc, html

from data.data import StockData
from data.summary import SummaryData
from graphs.graphs import plot_index_chart


def summary_value(title: str, value: float) -> html.P:
    return html.P(
        [
            html.P(f"{title} Change: "),
            html.Span(
                f"{round(value,2)} %",
                className="number",
            ),
        ],
        className="card-text",
    )


def stock_summary(data: StockData, summary: SummaryData) -> dbc.Row:
    return dbc.Row(
        [
            dbc.Col(
                [
                    dbc.Card(
                        [
                            dbc.CardBody(
                                [
                                    html.H4(
                                        "Overall Index",
                                        style={
                                            "text-align": "left",
                                            "padding-bottom": 0,
                                        },
                                    ),
                                    dcc.Graph(figure=plot_index_chart(data)),
                                ]
                            ),
                        ]
                    ),
                ],
                width=8,
            ),
            dbc.Col(
                [
                    dbc.Card(
                        [
                            dbc.CardHeader(f"Current Index Value ({data.index_date})"),
                            dbc.CardBody(
                                [
                                    html.H4(
                                        f"{round(data.current_index_value,2)} ",
                                        className="card-title",
                                    ),
                                    summary_value("Daily", summary.daily_growth),
                                    summary_value("Weekly", summary.weekly_growth),
                                    summary_value("Monthly", summary.monthly_growth),
                                ]
                            ),
                        ],
                        style={"width": "18rem"},
                    ),
                ],
                width=4,
            ),
        ],
        align="center",
    )
