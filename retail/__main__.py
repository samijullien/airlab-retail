import os

import dash
from dash.dependencies import Input, Output, State
from flask_caching import Cache

from . import create_app
from .store import StoreFactory


app = create_app()
cache = Cache(app.server, config={
    'CACHE_TYPE': 'memcached',
    'CACHE_MEMCACHED_SERVERS': os.getenv('MEMCACHED_SERVERS', ('localhost:11211',)),

    # The default timeout that is used if no timeout is specified. Unit of time is seconds.
    'CACHE_DEFAULT_TIMEOUT': 120,
})


@cache.memoize()
def get_store(*args):
    # expensive query
    return StoreFactory.create_store_env(*args)


@app.callback(
    [Output('custom_utility', 'style'),
    Output('weights', 'style')],
    [Input('utility_fun', 'value')])
def show_hide_element(utility_function):
    if utility_function == 'custom':
        return {'display': 'block'}, {'display': 'none'}
    else:
        return {'display': 'none'}, {'display': 'block'}


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
           State('daily_buckets', 'value'),
           State('order', 'value')])
def update_output_order(n_clicks, session_id, n_customers, n_items, max_stock,
                      horizon, freshness, seed, utility_fun, utility,
                      weight_waste, weight_sales, weight_availability, bias,
                      variance, leadtime_long, leadtime_fast, daily_buckets, order):
    if n_clicks is None:
        return dash.no_update

    store = StoreFactory.create_store_env(n_customers, n_items, max_stock,
                      horizon, freshness, seed, utility_fun, utility,
                      weight_waste, weight_sales, weight_availability, bias,
                      variance, leadtime_long, leadtime_fast, daily_buckets)

    rewards = store.run_to_completion(order, n_customers)

    return store.plot_rewards(rewards, horizon)


if __name__ == '__main__':
    app.run_server(host='0.0.0.0', debug=True)
