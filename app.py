import dash
import dash_html_components as html
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.graph_objs as go

app = dash.Dash()

data = [go.Scatter(x=[1, 2, 3], y=[4, 5, 6])]

app.layout = html.Div([
    dcc.Graph(
        id='example-graph',
        figure={
            'data': data,
            'layout': go.Layout(
                title='Example Graph',
                xaxis={'title': 'x'},
                yaxis={'title': 'y'},
            )
        }
    )
])

if __name__ == '__main__':
    app.run_server(debug=True)
