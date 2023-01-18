import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output
from dash.dash_table import DataTable
import dash_bootstrap_components as dbc
import plotly.graph_objs as go
import plotly.express as px
import pandas as pd


app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

colors = {
    'background': '#FFFFFF',
    'text': '#61CA21'
}

songs = pd.read_csv("./data/List of most-streamed songs on Spotify.csv")
songs['Streams (Billions)'].str.replace(',','.').astype(float)
playlist = pd.read_csv("./data/list.csv")
playlist1 = playlist.loc[playlist['Artist'].value_counts().head(15)]
otherPlaylist = pd.read_csv("./data/top50MusicFrom2010-2019.csv")

fig = px.bar(playlist, x="Song", y="Streams (Billions)", color="Streams (Billions)", barmode="group")
fig1 = px.bar(playlist1, x="Artist", y="Song", barmode="group")
fig3 = px.bar(otherPlaylist, x="artist", y="Popularity- The higher the value the more popular the song is", color="year", barmode="group")

fig.update_layout(
    plot_bgcolor=colors['background'],
    paper_bgcolor=colors['background'],
    font_color=colors['text']
)

row_summary_metrics = dbc.Row(
    [
        dbc.Col("", width=1),
        dbc.Col(dcc.Graph(figure=fig1)),
        dbc.Col(dcc.Graph(figure=fig3)),
        dbc.Col("", width=1),
    ],
)

app.layout = html.Div(style={'backgroundColor': colors['background']}, children=[
    html.H1(
        children='Top 100 spotify songs',
        style={
            'textAlign': 'center',
            'color': colors['text'],
            'fontSize': '40px'
        }
    ),

    html.Div(children='Project DASH by Indira Patricio Laura', style={
        'textAlign': 'center',
        'color': 'gray',
        'fontSize': '25px'
    }),
    row_summary_metrics,

    dcc.Graph(id='graph-with-slider'),
    dcc.Slider(
        otherPlaylist['year'].min(),
        otherPlaylist['year'].max(),
        step=None,
        value=otherPlaylist['year'].min(),
        marks={str(year): str(year) for year in otherPlaylist['year'].unique()},
        id='year-slider'
    )
])

@app.callback(
    Output('graph-with-slider', 'figure'),
    Input('year-slider', 'value'))
def update_figure(selected_year):
    filtered_df = otherPlaylist[otherPlaylist.year == selected_year]

    fig = px.scatter(filtered_df, x="Beats.Per.Minute -The tempo of the song", y="Popularity- The higher the value the more popular the song is",
                     size="Popularity- The higher the value the more popular the song is", color="the genre of the track", hover_name="artist",
                     log_x=True, size_max=55)

    fig.update_layout(transition_duration=500)

    return fig

if __name__ == '__main__':
    app.run_server(debug=True)
