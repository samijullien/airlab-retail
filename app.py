import os

import dash
from dash.dependencies import Input, Output, State
import dash_html_components as html
import dash_core_components as dcc

import torch
import torch.distributions as d
import torch.nn.functional as F

import numpy as np
import pandas as pd
import plotly.express as px

from flask_caching import Cache

from retail.retail import StoreEnv
from retail.utility import CustomUtility


name_df = pd.read_csv('Grocery_UPC_Database.csv')
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

app.config.suppress_callback_exceptions = True

app.layout = html.Div(
    [html.Div([
        html.Div([html.H1(children='RetaiL Store Generator and Management'),
                  html.Img(src=app.get_asset_url('grocery-beta.png'), style={'height': '70%', 'width': '70%'})],
                 style={'columnCount': 2}),

        dcc.Markdown('''
    ### Manage your own store and see how it performs! 
    The idea behind this web application is for you to customise your own store! But will you be able to avoid wasting?
    Once you've opened your brand new store, it is time to define your scoring metric - will it help you in understanding the underlying dynamics? 
    Will you be able to order the right amount of items, to reduce the ecological footprint of your store?
    #### Store creation
    The first step is to create your store. Enter below the characteristics to define your store. 
    This will also generate an item assortment, which can be replicated by entering a seed.
        '''),
        html.Label('Store characteristics'),

        html.Div([
            html.Div([
                html.Span('Customers: '),
              dcc.Input(
                  id="n_customers", type="number", value=500,
                  min=0, max=2000, step=1,
                )]),
            html.Div([
                html.Span('Items: '),
                dcc.Input(
                    id="n_items", type="number", value=30,
                    min=5, max=100, step=1,
                )]),
            html.Div([
                html.Span('Stock size: '),
                dcc.Input(
                    id="max_stock", type="number", value=600,
                    min=0, max=2000, step=1,
                )]),
            html.Div([
                html.Span('Horizon: '),
                dcc.Input(
                    id="horizon", type="number", value=91,
                    min=40, max=1000, step=1,
                )]),
            html.Div([
                html.Span('Bias: '),
                dcc.Input(
                    id="bias", type="number", value=0.0,
                    min=-1, max=1, step=.01,
                )]),
            html.Div([
                html.Span('Variance: '),
                dcc.Input(
                    id="variance", type="number", value=0.0,
                    min=0, max=1, step=.01,
                )]),
            html.Div([
                html.Span('ON Leadtime: '),
                dcc.Input(
                    id="leadtime_fast", type="number", value=0,
                    min=0, max=10, step=1,
                )]),
            html.Div([
                html.Span('ID Leadtime: '),
                dcc.Input(
                    id="leadtime_long", type="number", value=1,
                    min=1, max=10, step=1,
                )]),
            html.Div([
                html.Span('Buckets: '),
                dcc.Input(
                    id="daily_buckets", type="number", value=4,
                    min=1, max=12, step=1,
                )]),
            html.Div([
                html.Span('Seed: '),
                dcc.Input(
                    id="seed", type="number", placeholder="seed",
                    min=1, max=100000, step=1,
                )])], style={'columnCount': 5}),
        dcc.Markdown('''
    #### Success metric
    Now, it is time to define your success metric. You can pick one and specify weights, or select "Custom" and enter your own metric - containing the letters "a" for availability, "s" for sales, and  "w" for waste.
        '''),
        html.Label('Utility function'),
        dcc.Dropdown(id='utility_fun',
                     options=[
                         {'label': 'Cobb-Douglas', 'value': 'cobbdouglas'},
                         {'label': 'Log-linear', 'value': 'loglinear'},
                         {'label': 'Linear', 'value': 'linear'},
                         {'label': 'Custom', 'value': 'custom'}
                     ],
                     value='cobbdouglas'
                     ),
        dcc.Input(
            id="weight_waste", type="number", placeholder="Waste weight",
            min=0, max=3, step=.01, value=0.5,
        ),
        dcc.Input(
            id="weight_sales", type="number", placeholder="Sales weight",
            min=0, max=3, step=.01, value=0.5,
        ),
        dcc.Input(
            id="weight_availability", type="number", placeholder="Availability",
            min=0, max=3, step=.01, value=0.5,
        ),
        html.Label('Custom utility'),
        dcc.Input(type='text', id='utility', placeholder="Contains a,w and s"),

        html.Label('Create store'),
        html.Button('Create store', id='create'),
        dcc.Markdown('''
    #### Items
    Below, you can see the items present in your store, with their price and cost. 
    The color indicates how long you can keep them for.
        '''),
        dcc.Graph(id='output')], style={'width': '50%', 'float': 'left'}),

        html.Div([dcc.Markdown('''
    #### Freshness level
    Freshness represents how long your items can be stored before the expiration date. The fresher the item, the shorter the time it can be stored! Overall, you can see this as the difficulty level. Try moving the slider! 
        '''),
                  html.Label('Freshness level'),
                  dcc.Slider('freshness', min=1, max=100, value=1,
                             marks={1: 'Standard',
                                    10: 'Fresher items',
                                    25: 'Very fresh',
                                    50: 'Very very fresh',
                                    75: 'Too fresh',
                                    100: 'Bakery mode'}),

                  dcc.Markdown('''
    ### Order algorithm
    The main goal is to adjust the number of each item you order for your store. To do so, you can build an expression around the following:
    - n_customers, the number of customers expected
    - forecast, the purchase probability of each of those customers
    - stock, the current stock (or inventory position) of items.
        '''),
                  html.Label('Order input'),
                  dcc.Input(value='forecast*n_customers - stock',
                            type='text', id='order'),
                  html.Label('Use your ordering policy'),
                  html.Button('Order!', id='order_button'),
                  dcc.Graph(id='output2')
                  ], style={'marginLeft': '50%'})

     ])


@app.callback(
    Output('output', 'figure'),
    [Input('create', 'n_clicks')],
    state=[State('n_customers', 'value'),
           State('n_items', 'value'),
           State('max_stock', 'value'),
           State('horizon', 'value'),
           State('freshness', 'value'),
           State('seed', 'value'),
           State('utility_fun', 'value'),
           State('utility', 'value'),
           State('weight_waste', 'value'),
           State('weight_sales', 'value'),
           State('weight_availability', 'value'),
           State('bias', 'value'),
           State('variance', 'value'),
           State('leadtime_long', 'value'),
           State('leadtime_fast', 'value'),
           State('daily_buckets', 'value')])
def update_output_div(n_clicks, n_customers, n_items, max_stock, horizon,
                      freshness, seed, utility_fun, utility, weight_waste,
                      weight_sales, weight_availability, bias, variance,
                      leadtime_long, leadtime_fast, daily_buckets):
    if n_clicks is None:
        return dash.no_update
    if utility_fun == 'custom':
        utility_fun = CustomUtility(utility)
    bucketDist = d.uniform.Uniform(0, 1)
    sampled = bucketDist.sample((daily_buckets,))
    global sample_bucket_customers
    sample_bucket_customers = (n_customers*sampled/sampled.sum()).round()
    kwargsStore = {
        'assortment_size': n_items,
        'freshness': freshness,
        'seed': seed,
        'max_stock': max_stock,
        'utility_function': utility_fun,
        'utility_weights': {
            'alpha': weight_sales,
            'beta': weight_waste,
            'gamma': weight_availability,
        },
        'horizon': horizon,
        'lead_time': leadtime_long,
        'lead_time_fast': leadtime_fast,
        'forecastBias': bias,
        'forecastVariance': variance,
        'substep_count': daily_buckets,
        'bucket_cov': torch.eye(daily_buckets) / 100,
    }
    global store
    store = StoreEnv(**kwargsStore, bucket_customers=sample_bucket_customers)
    assortment_df = pd.DataFrame({
        'Cost': np.round(store.assortment.cost.numpy(), 2),
        'Price': np.round(store.assortment.selling_price.numpy(), 2),
        'Shelf life at purchase': store.assortment.shelf_lives.numpy(),
        'Name': name_df.sample(n_items).values.tolist(),
    })
    sc = px.scatter(assortment_df, x='Cost', y='Price', color='Shelf life at purchase',
                    title='Generated items at your store', hover_name='Name',
                    hover_data={'Name': False,
                                'Price': ":$,.2f",
                                'Cost': ":$,.2f",
                                'Shelf life at purchase': True})

    # sc.update_layout(hovertemplate =
   #                 '<b>%{Name}</b>'+
   #                 '<br><i>Price</i>: €%{Price:.2f}'+
   #                 '<br><i>Cost</i>: %{Cost:.2f}<br>')
    sc.update_yaxes(tickprefix="€")
    sc.update_xaxes(tickprefix="€")
    return(sc)


@app.callback(
    Output('output2', 'figure'),
    [Input('order_button', 'n_clicks')],
    state=[State('n_customers', 'value'),
           State('horizon', 'value'),
           State('order', 'value')])
def update_output_order(n_clicks, n_customers, horizon, order):
    if n_clicks is None:
        return dash.no_update
    done = False
    obs = store.reset()
    rewards = []
    while not done:
        customers = sample_bucket_customers.mean().round()
        stock = store.get_full_inventory_position()
        forecast = store.forecast.squeeze()
        std = torch.sqrt(customers*forecast+(1-forecast))
        number = F.relu(eval(order)).round()
        # Step the environment and get its observation
        obs = store.step(number.numpy())
        # Store reward for the specific time step
        rewards.append(obs[1].sum())
        done = obs[2]

    somme = np.sum(torch.stack(rewards).numpy().reshape(-1, 4), axis=1)
    fig = px.line(x=np.arange(0, horizon, 1), y=np.round(somme, 2),
                  title='Daily Utility value',
                  labels={'x': 'Time step',
                          'y': 'Utility'})

    return(fig)


if __name__ == '__main__':
    app.run_server(host='0.0.0.0', debug=True)
