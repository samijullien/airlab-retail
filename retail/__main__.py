import os

import dash
from dash.dependencies import Input, Output, State

from . import create_app
from .store import StoreFactory


app = create_app()

@app.callback(
    Output('output', 'figure'),
    [Input('create', 'n_clicks'),
    Input('session-id', 'children')],
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
def update_output_div(n_clicks, session_id, n_customers, n_items, max_stock,
                      horizon, freshness, seed, utility_fun, utility,
                      weight_waste, weight_sales, weight_availability, bias,
                      variance, leadtime_long, leadtime_fast, daily_buckets):
    if n_clicks is None:
        return dash.no_update
    global store
    store = StoreFactory.create_store_env(n_customers, n_items, max_stock,
                      horizon, freshness, seed, utility_fun, utility,
                      weight_waste, weight_sales, weight_availability, bias,
                      variance, leadtime_long, leadtime_fast, daily_buckets)
    return store.assortment.scatter_plot()


@app.callback(
    Output('output2', 'figure'),
    [Input('order_button', 'n_clicks'),
    Input('session-id', 'children')],
    state=[State('n_customers', 'value'),
           State('horizon', 'value'),
           State('order', 'value')])
def update_output_order(n_clicks, session_id, n_customers, horizon, order):
    if n_clicks is None:
        return dash.no_update

    rewards = store.run_to_completion(order, n_customers)

    return store.plot_rewards(rewards, horizon)


if __name__ == '__main__':
    app.run_server(host='0.0.0.0', debug=True)
