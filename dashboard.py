# dashboard.py
import dash
from dash import dcc, html
import plotly.express as px
import pandas as pd
import requests

# Fetch data
url = "https://disease.sh/v3/covid-19/historical/all?lastdays=all"
response = requests.get(url)
data = response.json()

# Process data
df = pd.DataFrame({
    "Date": pd.to_datetime(list(data["cases"].keys())),
    "Cases": list(data["cases"].values()),
    "Deaths": list(data["deaths"].values()),
    "Recovered": list(data["recovered"].values())
})

# Create Dash app
app = dash.Dash(__name__)

app.layout = html.Div([
    html.H1("COVID-19 Data Dashboard"),

    dcc.Dropdown(
        id='metric-selector',
        options=[
            {'label': 'Cases', 'value': 'Cases'},
            {'label': 'Deaths', 'value': 'Deaths'},
            {'label': 'Recovered', 'value': 'Recovered'}
        ],
        value='Cases'
    ),

    dcc.Graph(id='time-series'),

    html.Div([
        html.H3("Latest Global Statistics"),
        html.Table([
            html.Tr([html.Td("Total Cases"), html.Td(f"{df['Cases'].iloc[-1]:,}")]),
            html.Tr([html.Td("Total Deaths"), html.Td(f"{df['Deaths'].iloc[-1]:,}")]),
            html.Tr([html.Td("Total Recovered"), html.Td(f"{df['Recovered'].iloc[-1]:,}")])
        ])
    ])
])


@app.callback(
    dash.dependencies.Output('time-series', 'figure'),
    [dash.dependencies.Input('metric-selector', 'value')]
)
def update_graph(selected_metric):
    fig = px.line(df, x="Date", y=selected_metric,
                  title=f"COVID-19 {selected_metric} Over Time")
    fig.update_layout(template="plotly_dark")
    return fig


if __name__ == '__main__':
    app.run_server(debug=True)