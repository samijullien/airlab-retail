import numpy as np
import os
import pandas as pd

import torch
import torch.distributions as d
import torch.nn.functional as F

import dash
from dash.dependencies import Input, Output, State
import plotly.express as px

from retail import create_app
from retail.retail import StoreEnv
from retail.utility import CustomUtility


name_df = pd.read_csv('Grocery_UPC_Database.csv')

app = create_app()

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
