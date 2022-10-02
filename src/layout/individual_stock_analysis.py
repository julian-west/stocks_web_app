import dash_bootstrap_components as dbc
from dash import dcc, html

from data.summary import SummaryData
from graphs.graphs import plot_swarm_chart


def swarm_chart_layout(summary: SummaryData):
    style = {
        "text-align": "left",
        "padding-bottom": "10px",
    }
    return (
        html.H4("Stock Price Growth", style=style),
        dcc.Graph(figure=plot_swarm_chart(summary)),
        html.H4("Stock Prices - Rebased", style=style),
    )


def individual_stocks(summary: SummaryData) -> dbc.Row:

    # todo move somewhere else
    stock_list = [
        {"label": summary.data.company_names[i], "value": stock}
        for i, stock in enumerate(summary.data.data.columns)
    ]
    print(stock_list)

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
                                    *swarm_chart_layout(summary),
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
