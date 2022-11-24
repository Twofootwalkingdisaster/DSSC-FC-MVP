import datetime

import dash
from dash import html
from dash import dcc
from dash.dependencies import Input, Output
import plotly.express as px
import pandas as pd
from Storage import GetFile
import plotly.graph_objs as go

import pickle
import fbprobhet


company_name = ['Alphabet', 'Apple', 'BMO', 'Cisco', 'IBM', 'Meta', 'Microsoft',
                'Nvidia', 'Oracle', 'RBC', 'Scotia', 'TSM', 'TXN', 'VZ']

mid_date = datetime.datetime(2022, 10, 12).date()

data = GetFile.get_file("Alphabet")
data.rename(columns={"Unnamed: 0": "DateTime"}, inplace=True)
data[['Date', 'Time']] = data.DateTime.str.split(" ", expand=True)
data['Date'] = pd.to_datetime(data['Date'], format='%Y-%m-%d')

fig_past_1 = px.line(data,
                     x="Date",
                     y=["Open", "Close"],
                     title="Alphabet Data with Open & Close")

fig_past_1.update_layout(
    template="plotly_dark",
    xaxis_title="Date",
    yaxis_title="Open & Close"
)
fig_future_1 = px.line(data,
                         x="Date",
                         y=["Close"],
                         title="Data with Close")
fig_future_1.update_layout(
        template="plotly_dark",
        xaxis_title="Date",
        yaxis_title="Close"
)

fig_past_2 = px.line(data,
                     x="Date",
                     y=["High", "Low"],
                     title="Alphabet Data with High & Low")


fig_past_2.update_layout(
    template="plotly_dark",
    xaxis_title="Date",
    yaxis_title="High & Low"
)

fig_past_3 = go.Figure(data=go.Candlestick(
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
                    children="Company Stock Data"
                ),
                html.P(
                    id="header-description",
                    children="Data from 2021 to 22"
                )
            ]
        ),
        html.Div(
            id="menu-area",
            children=[
                html.Div(
                    id="menu-area-1",
                    children=[
                        html.Label(
                            className="menu-title-1",
                            children=["Company Name: ", dcc.Dropdown(
                                id="company-filter",
                                className="dropdown",
                                options=[{"label": item, "value": item} for item in company_name],
                                clearable=False,
                                value="Alphabet"
                            )]
                        )
                    ]
                ),
                html.Div(
                    id="menu-area-2",
                    children=[
                        html.Label(
                            className="menu-title-2",
                            children=["Date Range: ", dcc.DatePickerRange(
                                id="date-range",
                                min_date_allowed=data.Date.min().date(),
                                start_date=data.Date.min().date(),
                                end_date=data.Date.max().date()
                            )]
                        )
                    ]
                ),
            ],
        ),
        html.Div(
            id="graph-container-1",
            children=[dcc.Graph(
                id="price-chart-1",
                figure=fig_past_1,
                config={"displayModeBar": False}
            ),
                dcc.Graph(
                    id="price-chart-future-1",
                    figure=fig_future_1,
                    config={"displayModeBar": False}
                )]
        ),
        html.Div(
            id="graph-container-2",
            children=dcc.Graph(
                id="price-chart-2",
                figure=fig_past_2,
                config={"displayModeBar": False}
            )
        ),
        html.Div(
            id="graph-container-3",
            children=dcc.Graph(
                id="price-chart-3",
                figure=fig_past_3,
                config={"displayModeBar": False}
            )
        ),

    ]
)


@app.callback(
    Output("price-chart-1", "figure"),
    Output("price-chart-2", "figure"),
    Output("price-chart-3", "figure"),
    Output("price-chart-future-1", "figure"),
    Input("company-filter", "value"),
    Input("date-range", "start_date"),
    Input("date-range", "end_date"),
)
def update_chart(company_name, start_date, end_date):
    data = GetFile.get_file(company_name)
    data.rename(columns={"Unnamed: 0": "DateTime"}, inplace=True)
    data[['Date', 'Time']] = data.DateTime.str.split(" ", expand=True)
    data['Date'] = pd.to_datetime(data['Date'], format='%Y-%m-%d')

    filtered_past_data = data.loc[(data.Date >= start_date) & (data.Date <= end_date)]

    end_date = datetime.datetime.strptime(end_date,
                                          '%Y-%m-%d').date()
    future_days = end_date - mid_date
    future_days = future_days.days

    model = pickle.load(open('fbprophet.sav', 'rb'))

    future = model.make_future_dataframe(periods=future_days,
                                         freq='d',
                                         include_history=True)
    future_values = model.predict(future)

    f_v = future_values['ds'] >= '2022-10-13 09:30:00'
    f_v_1 = future_values[f_v]

    fig_past_1 = px.line(filtered_past_data,
                         x="Date",
                         y=["Open", "Close"],
                         title=company_name + " Data with Open & Close")
    fig_past_1.update_layout(
        template="plotly_dark",
        xaxis_title="Date",
        yaxis_title="Open & Close"
    )
    fig_future_1 = px.line(f_v_1,
                         x="ds",
                         y="yhat",
                         title=company_name + " Predicted Data with Close")
    fig_future_1.update_layout(
        template="plotly_dark",
        xaxis_title="Date",
        yaxis_title="Close"
    )

    fig_past_2 = px.line(filtered_past_data,
                         x="Date",
                         y=["High", "Low"],
                         title=company_name + " Data with High & Low")

    fig_past_2.update_layout(
        template="plotly_dark",
        xaxis_title="Date",
        yaxis_title="High & Low"
    )

    fig_past_3 = go.Figure(data=go.Candlestick(
        x=filtered_past_data['Date'],
        open=filtered_past_data['Open'],
        close=filtered_past_data['Close'],
        high=filtered_past_data['High'],
        low=filtered_past_data['Low']
    ))

    return fig_past_1, fig_past_2, fig_past_3, fig_future_1


if __name__ == "__main__":
    app.run_server(debug=True, port=8052)
