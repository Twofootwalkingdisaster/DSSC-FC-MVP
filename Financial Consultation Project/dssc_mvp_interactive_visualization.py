import dash
from dash import html
from dash import dcc
from dash.dependencies import Input, Output
import plotly.express as px
import pandas as pd
# from Storage import GetFile
import plotly.graph_objs as go

company_name = ['Alphabet', 'Apple', 'BMO', 'Cisco', 'IBM', 'Meta', 'Microsoft', 'Nvidia', 'Oracle', 'RBC', 'Scotia',
                'TSM', 'TXN', 'VZ']

data = pd.read_csv("temp_files\\Alphabet_data.csv")
#data.rename(columns={"Unnamed: 0": "DateTime"}, inplace=True)
data[['Date', 'Time']] = data.DateTime.str.split(" ", expand=True)
data['Date'] = pd.to_datetime(data['Date'], format='%Y-%m-%d')


fig1 = px.line(data,
              x="Date",
              y=["Open", "Close"],
              title="Alphabet Data with Open & Close")

fig1.update_layout(
    template="plotly_dark",
    xaxis_title="Date",
    yaxis_title="Open & Close"
)

fig2 = px.line(data,
              x="Date",
              y=["High", "Low"],
              title="Alphabet Data with High & Low")

fig2.update_layout(
    template="plotly_dark",
    xaxis_title="Date",
    yaxis_title="High & Low"
)

fig3 = go.Figure(data=go.Candlestick(
        x=data['Date'],
        open=data['Open'],
        close=data['Close'],
        high=data['High'],
        low=data['Low']
    ))


app = dash.Dash(__name__)

app.layout = html.Div(
    id="app-container",
    children=[
        html.Div(
            id="header-area",
            children=[
                html.H1(
                    id="header-title",
                    style={'textAlign': 'center'},
                    children="Company Stock Data"
                ),
                html.P(
                    id="header-description",
                    style={'textAlign': 'center'},
                    children="Data from 2021 to 22"
                )
            ]
        ),
        html.Div(
            id="menu-area",
            children=[
                html.Div(
                    style={
                        'paddingLeft': '40%',
                        'paddingRight': '40%',
                        'textAlign': 'center'
                    },
                    children=[
                        html.Div(
                            className="menu-title",
                            style={'fontWeight': 'bold'},
                            children="Company Name"
                        ),
                        dcc.Dropdown(
                            id="company-filter",
                            className="dropdown",
                            options=[{"label": item, "value": item} for item in company_name],
                            clearable=False,
                            value="Alphabet"
                        )]),
                html.Div(
                    style={
                        'paddingLeft': '31%',
                        'paddingRight': '31%',
                        'textAlign': 'center',
                        'paddingTop': '1%'
                    },
                    children=[
                        html.Div(
                            className="menu-title",
                            style={'fontWeight': 'bold'},
                            children="Date Range"
                        ),
                        dcc.DatePickerRange(
                            id="date-range",
                            min_date_allowed=data.Date.min().date(),
                            max_date_allowed=data.Date.max().date(),
                            start_date=data.Date.min().date(),
                            end_date=data.Date.max().date()
                        )
                    ]
                ),
            ],
        ),
        html.Div(
            style={
                'paddingLeft': '10%',
                'paddingRight': '10%',
                'paddingTop': '1%'
            },
            id="graph-container-1",
            children=dcc.Graph(
                id="price-chart-1",
                figure=fig1,
                config={"displayModeBar": False}
            )
        ),
        html.Div(
            style={
                'paddingLeft': '10%',
                'paddingRight': '10%',
                'paddingTop': '1%'
            },
            id="graph-container-2",
            children=dcc.Graph(
                id="price-chart-2",
                figure=fig2,
                config={"displayModeBar": False}
            )
        ),
        html.Div(
            style={
                'paddingLeft': '10%',
                'paddingRight': '10%',
                'paddingTop': '1%'
            },
            id="graph-container-3",
            children=dcc.Graph(
                id="price-chart-3",
                figure=fig3,
                config={"displayModeBar": False}
            )
        ),

    ]
)


@app.callback(
    Output("price-chart-1", "figure"),
    Output("price-chart-2", "figure"),
    Output("price-chart-3", "figure"),
    Input("company-filter", "value"),
    Input("date-range", "start_date"),
    Input("date-range", "end_date"),
)
def update_chart(company_name, start_date, end_date):
    data = GetFile.get_file(company_name)
    data.rename(columns={"Unnamed: 0": "DateTime"}, inplace=True)
    data[['Date', 'Time']] = data.DateTime.str.split(" ", expand=True)
    data['Date'] = pd.to_datetime(data['Date'], format='%Y-%m-%d')

    filtered_data = data.loc[(data.Date >= start_date) & (data.Date <= end_date)]

    fig1 = px.line(filtered_data,
                   x="Date",
                   y=["Open", "Close"],
                   title=company_name + " Data with Open & Close")
    fig1.update_layout(
        template="plotly_dark",
        xaxis_title="Date",
        yaxis_title="Open & Close"
    )

    fig2 = px.line(filtered_data,
                   x="Date",
                   y=["High", "Low"],
                   title=company_name + " Data with High & Low")

    fig2.update_layout(
        template="plotly_dark",
        xaxis_title="Date",
        yaxis_title="High & Low"
    )

    fig3 = go.Figure(data=go.Candlestick(
        x=filtered_data['Date'],
        open=filtered_data['Open'],
        close=filtered_data['Close'],
        high=filtered_data['High'],
        low=filtered_data['Low']
    ))

    return fig1, fig2, fig3


if __name__ == "__main__":
    app.run_server(debug=True)
