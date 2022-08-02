import dash
import dash_auth
from dash import dcc
from dash import html
from dash import Input, Output
import plotly.express as px

# Keep this out of source code repository - save in a file or a database
VALID_USERNAME_PASSWORD_PAIRS = {
    'Life': 'Expectancy'
}

external_stylesheets = ['https://cdn.jsdelivr.net/npm/purecss@2.1.0/build/pure-min.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
server = app.server
app.title='Authorization Application'
auth = dash_auth.BasicAuth(
    app,
    VALID_USERNAME_PASSWORD_PAIRS
)

app.layout = html.Div([
    html.H1('Welcome!'),
    html.H3('You are successfully authorized'),
    html.H4('Life expentancy progression of countries per continents'),
    dcc.Checklist(
        id='checklist',
        options=["Asia", "Europe", "Africa","Americas","Oceania"],
        value="Americas"
    ),
    dcc.Graph(id='graph'),
    html.A('Code on Github', href='https://github.com/manueldelreal/208-authentication-example'),
    html.Br(),
    html.A("Data Source", href='https://www.gapminder.org/tag/life-expectancy/'),
], className='container')


@app.callback(
    Output("graph", "figure"), 
    Input("checklist", "value"))

def update_line_chart(value):
    df = px.data.gapminder() # replace with your own data source
    mask = df.continent.isin(value)
    fig = px.line(df[mask], 
        x="year", y="lifeExp", color='country')
    return fig


############ Deploy
if __name__ == '__main__':
    app.run_server(debug=True)