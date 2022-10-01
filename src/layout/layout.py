import dash_bootstrap_components as dbc
from dash import dcc, html

from const import COMPANY_NAMES
from data.data import StockData
from functions import PerformanceReport, SummaryBox
from graphs.graphs import plot_index_chart

data = PerformanceReport()
index_chart = data.plot_performance_chart()
swarm_plot = data.plot_swarm_plot()
yoy_growth_chart = data.plot_yoy_growth()
drawdown_chart = data.plot_drawdown()


new_data = StockData()
summary = SummaryBox(data=new_data)
print(summary.data.rebased_prices)

stock_list = []
for i, stock in enumerate(data.prices.columns):
    stock_list.append({"label": COMPANY_NAMES[i], "value": stock})


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


def stock_summary(data: StockData, summary: SummaryBox) -> dbc.Row:
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
                                    html.P(
                                        [
                                            html.P("Daily change: "),
                                            html.Span(
                                                f"{round(summary.daily_growth,2)} %",
                                                className="number",
                                            ),
                                        ],
                                        className="card-text",
                                    ),
                                    html.P(
                                        [
                                            html.P("Weekly change: "),
                                            html.Span(
                                                f"{round(summary.weekly_growth,2)} %",
                                                className="number",
                                            ),
                                        ],
                                        className="card-text",
                                    ),
                                    html.P(
                                        [
                                            html.P("Monthly change: "),
                                            html.Span(
                                                f"{round(summary.monthly_growth,2)} %",
                                                className="number",
                                            ),
                                        ],
                                        className="card-text",
                                    ),
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


def tabs() -> dbc.Row:
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
                                            dbc.Tab(
                                                [html.Li(x) for x in COMPANY_NAMES],
                                                label="Stocks in index",
                                                style={
                                                    "text-align": "left",
                                                    "padding": 10,
                                                },
                                            ),
                                            dbc.Tab(
                                                [
                                                    dbc.Row(
                                                        [
                                                            html.H4(
                                                                "Year over year index growth - 28 day MA",
                                                                style={"padding": 10},
                                                            ),
                                                            dcc.Graph(
                                                                figure=yoy_growth_chart
                                                            ),
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
                                            ),
                                            dbc.Tab(
                                                dbc.Table.from_dataframe(
                                                    data.monthly_returns_table,
                                                    striped=True,
                                                    bordered=True,
                                                    hover=True,
                                                    responsive=True,
                                                ),
                                                label="Index Monthly Returns",
                                            ),
                                            dbc.Tab(
                                                [
                                                    dbc.Row(
                                                        [
                                                            html.H4(
                                                                "'Under-water Plot' - Drawdown Periods",
                                                                style={"padding": 10},
                                                            ),
                                                            dcc.Graph(
                                                                figure=drawdown_chart
                                                            ),
                                                        ]
                                                    ),
                                                ],
                                                label="Drawdown",
                                            ),
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


def individual_stocks() -> dbc.Row:
    return dbc.Row(
        [
            dbc.Col(
                [
                    dbc.Card(
                        [
                            dbc.CardBody(
                                [
                                    html.H1(
                                        "Individual Stocks",
                                        style={
                                            "textAlign": "center",
                                            "padding-bottom": "20px",
                                        },
                                    ),
                                    html.H4(
                                        "Stock Price Growth",
                                        style={
                                            "text-align": "left",
                                            "padding-bottom": "10px",
                                        },
                                    ),
                                    dcc.Graph(figure=swarm_plot),
                                    html.H4(
                                        "Stock Prices - Rebased",
                                        style={
                                            "text-align": "left",
                                            "padding-bottom": "10px",
                                        },
                                    ),
                                    dcc.Dropdown(
                                        id="my-dropdown",
                                        options=stock_list,
                                        multi=True,
                                        value=[x["value"] for x in stock_list],
                                        style={
                                            "display": "block",
                                            "margin-left": "auto",
                                            "margin-right": "auto",
                                            "width": "60%",
                                        },
                                    ),
                                    dcc.Graph(id="my-graph"),
                                ]
                            )
                        ]
                    )
                ]
            ),
        ]
    )


def footer():
    return dbc.Row([html.Footer(html.P("Julian West"))], className="footer")


def build_ui():
    return html.Main(
        [
            header(),
            dbc.Container(
                [
                    stock_summary(new_data, summary),
                    tabs(),
                    individual_stocks(),
                    footer(),
                ]
            ),
        ]
    )
