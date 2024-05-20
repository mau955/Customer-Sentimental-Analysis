# ==================================
# SPAN-Report Dashboard
# ==================================


# Import Modules
import pandas as pd

import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Output, Input

import plotly.graph_objs as go
import flask


# Functions
def score(pv, values=['Achieved', 'Benchmark']):
    pv['Score'] = pd.Series(pv[values[0]] / pv[values[1]] * 100).round(decimals=2)

    return pv


def datasets():
    # Import Data Sets
    original = pd.read_excel('Dashboard.xlsx', sheet_name='Original', index_col=None)
    department = pd.read_excel('Dashboard.xlsx', sheet_name='Department', index_col=0)
    questions = pd.read_excel('Dashboard.xlsx', sheet_name='Questions', index_col=0)

    # Separate Indicators
    df = original.drop(['Department Id.', 'Question Id.', 'Exceeded', 'Met', 'Fell Below'], axis=1)
    df['Achieved'] = original['Exceeded'] + original['Met'] + original['Fell Below']

    # Lookup Department Id.
    dpm = []
    for did in original.loc[:,'Department Id.']:
        dpm.append(department['Department'].loc[did])
    df['Department'] = dpm

    # Lookup Question Id.
    qst = []
    for qs in original.loc[:, 'Question Id.']:
        qst.append(questions['Question'].loc[qs])
    df['Question'] = qst

    # Add Calculated Field
    df = score(df)

    return df


def initialize_app():
    server = flask.Flask(__name__)
    app = dash.Dash(__name__, server=server)

    return app


def dashboard(df, app):
    dments = df['Department'].unique()

    app.layout = html.Div([
        html.H2('Performance Score Funnel Report'),

        html.Div(
            [
                dcc.Dropdown(
                    id='department',
                    options=[{
                        'label': dptm,
                        'value': dptm
                    } for dptm in dments],
                    value='All departments')
            ],
            style={'width': '25%',
                   'display': 'inline-block'}),

        dcc.Graph(id='bar_graph')
    ])
                    # figure={'data': traces,
                    #         'layout': go.Layout(title='Performance Score Per Year', barmode='stack')}



    @app.callback(
        Output('bar_graph', 'figure'),
        [Input('department', 'value')])

    def update_graph(department):
        # Filter
        if department == 'All departments':
            df_plot = df.copy()
        else:
            df_plot = df[df['Department'] == department]

        # Pivot Table
        pv = pd.pivot_table(
            df_plot,
            index=['Department'],
            columns=['Year'],
            values=['Score']
        )

        # Traces
        yrStr = df['Year'].sort_values().unique()
        traces = []

        for year in yrStr:
            trc = go.Bar(x=pv.index, y=pv[('Score', year)], name=year)
            traces.append(trc)

        return {'data': traces,
                'layout': go.Layout(title=f'{department} Performance Score', barmode='group')
                }


def launch(app):
    app.run_server(debug=True)


# Run program
if __name__ == '__main__':
    # Data Sets
    df = datasets()

    # Initialize app
    app = initialize_app()

    # Dashboard
    dashboard(df, app)

    # # Filter Dashboard
    # update(df, app)

    # Launch app
    launch(app)