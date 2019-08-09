import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_table
import dash_table.FormatTemplate as FormatTemplate
import dash_bootstrap_components as dbc

layout = dbc.Container([
    dbc.Row([
        dbc.Col(
            [
                html.Img(
                    src="./assets/logo.png", className="three columns",
                    style={
                        'float': 'right',
                        'position': 'relative'
                    }),
            ]
        ),
        dbc.Col(
            [
                html.H1("Vacuum Processing Index",
                        style={'textAlign': 'Left'})
            ]
        ),
    ]),
    dbc.Row([
        dbc.Col([
             dcc.Graph(figure=index_chart)
        ]),
    ]),
])


html.Div(
    children=[
        # HEADER ROW
        html.Div([
            html.Img(
                src="./assets/logo.png", className="three columns",
                style={
                    'float': 'right',
                    'position': 'relative'
                }),
            html.Div(
                children=[html.H1("Vacuum Processing Index",
                                  style={'textAlign': 'Left'})], className="nine columns")
        ], className="row"),
        # ROW 1
        html.Div([
            html.Div(
                children=[
                    dcc.Graph(figure=index_chart)
                ], className="eight columns"),
            html.Div(
                children=[
                    html.Span(
                        f"Current index value: {round(data.current_index_value,1)}"),
                    html.Span(
                        f"Daily percentage change: {round(data.daily_index_pct_change,2)}%")
                ], className="four columns"),
        ], className="row"),
        # ROW 2
        html.Div(
            children=[
                dash_table.DataTable(
                    id='index-monthly-returns',
                    columns=[{"name": 'Year', "id": 'Year'}] + [{"name": i,
                                                                 "id": i,
                                                                 "type": 'numeric',
                                                                 "format": FormatTemplate.percentage(2)} for i in data.monthly_returns_table.columns[1:]],
                    data=data.monthly_returns_table.to_dict('records')
                )
            ], className="row"),
        # ROW 3
        html.Div(
            children=[html.H1("Individual Stocks", style={'textAlign': 'center'}),
                      dcc.Dropdown(id='my-dropdown',
                                   options=stock_list,
                                   multi=True,
                                   value=[x['value'] for x in stock_list],
                                   style={"display": "block", "margin-left": "auto", "margin-right": "auto", "width": "60%"}),
                      dcc.Graph(id='my-graph')
                      ], className="row")
    ], className="container")
