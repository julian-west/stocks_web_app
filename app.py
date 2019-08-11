import os

import pandas as pd

import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
import dash_table
import dash_table.FormatTemplate as FormatTemplate
from dash.dependencies import Input, Output, State

import plotly.graph_objs as go
import plotly

from flask import send_file
import io

from functions import PerformanceReport
from const import STOCKS, COMPANY_NAMES
import flask


server = flask.Flask(__name__)
app = dash.Dash(__name__,server=server)
app.title = "Stocks Summary"


########## DATA PREPARATION ###################

data = PerformanceReport()
index_chart = data.plot_performance_chart()
swarm_plot = data.plot_swarm_plot()
yoy_growth_chart = data.plot_yoy_growth()
drawdown_chart = data.plot_drawdown()


stock_list = []
for i, stock in enumerate(data.prices.columns):
    stock_list.append({'label': COMPANY_NAMES[i], 'value': stock})

############## LAYOUT ######################

app.layout = html.Main([

    dbc.Row(
        [
            html.H3("VACUUM PROCESSING INDEX",
                    style={'text-align': 'center'}),
            html.Div([
                html.Span([
                    html.A("Raw Data", href="/download_excel/",style={'margin-right':'10px'}),
                    html.I(className="fa fa-arrow-circle-down")],className="button")
                ])
        ],
        className='header', style={'display': 'grid'}),
    dbc.Container([
        dbc.Row([
            dbc.Col([
                dbc.Card([
                    dbc.CardBody([
                        html.H4("Overall Index", style={
                                'text-align': 'left', 'padding-bottom': 0}),
                        dcc.Graph(figure=index_chart)
                    ]),
                ]
                ),
            ], width=8),
            dbc.Col([
                dbc.Card(
                    [
                        dbc.CardHeader(
                            f"Current Index Value ({data.rebased_prices.index[-1].date()})"),
                        dbc.CardBody(
                            [
                                html.H4(
                                    f"{round(data.current_index_value,2)} ", className="card-title"),
                                html.P(f"Daily change {round(data.daily_index_pct_change,2)} %",
                                       className="card-text"),
                                html.P(f"Weekly change {round(data.weekly_index_pct_change,2)} %",
                                       className="card-text"),
                                html.P(f"Monthly change {round(data.monthly_index_pct_change,2)} %",
                                       className="card-text"),
                            ]
                        ),
                    ],
                    style={"width": "18rem"},
                ),
            ], width=4),
        ], align='center'),
        dbc.Row([
            dbc.Col([
                dbc.Card([
                    dbc.CardBody([
                        html.H4("Individual Stock Price Growth", style={
                                'text-align': 'left', 'padding-bottom': 0}),
                        dcc.Graph(figure=swarm_plot)
                    ]),
                ]
                ),
            ], width=12)
        ]),
        dbc.Row([
            dbc.Col([
                dbc.Card([
                    dbc.CardBody([
                        dbc.Tabs([
                            dbc.Tab(
                                [html.Li(x) for x in COMPANY_NAMES], label="Stocks in index", style={'text-align': 'left', 'padding': 10}
                            ),
                            dbc.Tab([
                                dbc.Row([
                                    html.H4(
                                        "Year over year index growth - 28 day MA", style={'padding': 10}),
                                    dcc.Graph(figure=yoy_growth_chart)
                                ]),
                                dbc.Row([
                                    html.H4("Calendar Growth Map",
                                            style={'padding': 10}),
                                    html.Img(src="assets/yoy_calmap.png",
                                             style={'padding': 10})
                                ])
                            ], label="YoY Growth"),
                            dbc.Tab(
                                dbc.Table.from_dataframe(
                                    data.monthly_returns_table, striped=True, bordered=True, hover=True, responsive=True), label="Index Monthly Returns"
                                    ),
                            dbc.Tab([
                                dbc.Row([
                                    html.H4("'Under-water Plot' - Drawdown Periods",style={'padding': 10}),
                                    dcc.Graph(figure=drawdown_chart)
                                ]),
                            ],label="Drawdown"),
                        ]),
                    ]),
                ]),
            ]),
        ]),

        dbc.Row([
            dbc.Col([
                dbc.Card([
                    dbc.CardBody([
                        html.H1("Individual Stocks", style={
                                'textAlign': 'center'}),
                        dcc.Dropdown(id='my-dropdown',
                                     options=stock_list,
                                     multi=True,
                                     value=[x['value'] for x in stock_list],
                                     style={"display": "block", "margin-left": "auto", "margin-right": "auto", "width": "60%"}),
                        dcc.Graph(id='my-graph')
                    ])
                ])

            ]),
        ]),
        dbc.Row([
            html.Footer(
                html.P("Julian West")
            )
        ], className="footer")
    ])
])


############## CALL BACK FUNCTIONS ######################

@app.callback(Output('my-graph', 'figure'),
              [Input('my-dropdown', 'value')])
def update_graph(selected_dropdown_value):

    equity_traces = []

    for stock in selected_dropdown_value:
        equity_traces.append(go.Scatter(
            x=data.rebased_prices.index.tolist(),
            y=data.rebased_prices[stock].values.tolist(),
            mode='lines',
            opacity=0.7,
            name=stock,
            textposition='bottom center'))

    # data = [val for sublist in traces for val in sublist]
    figure = {'data': equity_traces,
              'layout': go.Layout(
                  colorway=['#d53e4f', '#f46d43', '#fdae61', '#fee08b',
                            '#e6f598', '#abdda4', '#66c2a5', '#3288bd'],
                  height=600,
                  title=f"Stock prices for {', '.join(i for i in selected_dropdown_value)} rebased to '2018-12-28'",
                  xaxis=dict(title="Date",
                             rangeselector=dict(buttons=list([{'count': 1, 'label': '1M', 'step': 'month', 'stepmode': 'backward'},
                                                              {'count': 6, 'label': '6M',
                                                               'step': 'month', 'stepmode': 'backward'},
                                                              {'step': 'all'}])),
                             range=([data.rebased_prices.index.max() - pd.DateOffset(months=24),
                                     data.rebased_prices.index.max() + pd.DateOffset(months=6)]),
                             rangeslider={'visible': True},
                             type='date'),
                  yaxis=dict(title="Stock price (indexed at '2018-12-28')",
                             autorange=True,
                             fixedrange=False))}
    return figure


@app.server.route('/download_excel/')
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
    excel_data = strIO.getvalue()
    strIO.seek(0)

    return send_file(strIO,
                     attachment_filename='raw_data.xlsx',
                     as_attachment=True)


if __name__ == '__main__':

    app.run_server(port=2000, debug=True, threaded=True)
