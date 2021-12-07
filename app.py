import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.express as px
import pandas as pd

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
server = app.server

# dataframe path
fileName = ('treatments_2018_joined.csv')
df = pd.read_csv(fileName)

# round ndvi to two decimals
df['mean'] = round(df['mean'],2)

# get the list of seasons for the selection menu
crop_list = [item for item in df['crop'].unique().tolist()]
planting_density = [item for item in df['planting density'].unique().tolist()]


app.layout = html.Div([

    html.H4('AGRY 545 / CE 597 Remote Sensing of Land Resources'),
    html.H6('Final project'),

    html.Div((
        html.H3('NDVI values from The Yaqui Valey farmers fields with N-rich strip')
    ), style={'width': '60%', 'padding': '10px 40px 10px 20px'}),

    # show plot menu
    html.Div(["Select crop: ",
    dcc.Dropdown(
        id='crop',
        options=[{'label': i, 'value': i} for i in crop_list],
        value=crop_list[0])
    ],style={'width': '30%', 'display': 'inline-block', 'padding': '0px 20px 0px 50px'}),

    html.Div(["Crop variety: ",
    dcc.Dropdown(
        id='var'),
    ],style={'width': '30%', 'display': 'inline-block', 'padding': '0px 20px 0px 50px'}),

    html.Div(["Days after sowing: ",
    dcc.Dropdown(
        id='das'),
    ],style={'width': '30%', 'display': 'inline-block', 'padding': '0px 20px 0px 50px'}),

    dcc.Graph(id="line-chart")

    # show the seasons menu
])

# Output("cities_dropdown", "options"),
#    [ Input("countries_dropdown", "value") ],
#    )
# cultivar menu
@app.callback(
    Output("var", "options"),
    [Input("crop", "value")],
    )
def update_varieties_options(crop):

    cropDF = df[df['crop'] == crop]

    varieties = []

    varieties += [dict(label=var, value=var) for var in cropDF['crop varieties'].unique().tolist()]

    return varieties

# Days after sowing
@app.callback(
    Output("das", "options"),
    [Input("crop", "value")],
    [Input("var", "value")]
    )
def update_varieties_options(crop, var):

    # filter Rich strip
    trtDF = df[df['trt'] == 'N-Rich strip']

    cropDF = trtDF[trtDF['crop'] == crop]

    varDF = cropDF[cropDF['crop varieties'] == var]

    das = []

    das += [dict(label=das, value=das) for das in varDF['days after sowing']]

    return das



# line plot
@app.callback(
    Output('line-chart', 'figure'),
    Input('crop', 'value'),
    Input('var', 'value'),
    Input('das', 'value'))

def update_graph(crop, var, das):

    # filter Rich strip
    trtDF = df[df['trt'] == 'N-Rich strip']

    # filter crop
    cropDF = trtDF[trtDF['crop'] == crop]

    # filter variety
    varDF = cropDF[cropDF['crop varieties'] == var]

    dasDF = varDF[varDF['days after sowing'] == das]
    #plotDFtrt = plotDF[plotDF['trt']=='N-Rich strip']

    fig = px.line(varDF, x='days after sowing', y='mean', color='plot',
                  labels={"color": "Group"}
                  )

    # strip down the rest of the plot
    fig.update_layout(xaxis_title='Days after sowing',
                      yaxis_title='NDVI',
                      plot_bgcolor='lavender',
                      font_size=20,
                      font_color='#000000',
                      font_family='Old Standard TT')

    #fig.add_annotation(text="Text annotation with arrow",
    #                   showarrow=True,
    #                   arrowhead=1)

    for plot in dasDF['plot']:

        tempDF = dasDF[dasDF['plot'] == plot]

        # item() gets the value in a specific column of a dataframe
        fig.add_annotation(x=tempDF['days after sowing'].item(), y=tempDF['mean'].item(),
                           text=tempDF['mean'].item(), showarrow=False)


    #fig.update_traces(text=varDF['mean'], textposition='top center')

    return fig

app.run_server(debug=True)
