import os

import dash
from dash.dependencies import Input, Output, State
from flask_caching import Cache

from . import create_app
from .store import StoreFactory


app = create_app()
cache = Cache(app.server, config={
    'CACHE_TYPE': 'redis',
    'CACHE_REDIS_URL': os.environ.get('REDIS_URL', 'redis://localhost:6379'),

    # should be equal to maximum number of users on the app at a single time
    'CACHE_THRESHOLD': 100,
})


# perform expensive computations in this "global store"
# these computations are cached in a globally available
# redis memory store which is available across processes
# and for all time.
@cache.memoize()
def get_store(*args):
    # expensive query
    return StoreFactory.create_store_env(*args)


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
                        variance, leadtime_long, leadtime_fast, daily_buckets,
                        order):
    if n_clicks is None:
        return dash.no_update

    store = get_store(n_customers, n_items, max_stock,
                      horizon, freshness, seed, utility_fun, utility,
                      weight_waste, weight_sales, weight_availability, bias,
                      variance, leadtime_long, leadtime_fast, daily_buckets)

    rewards = store.run_to_completion(order, n_customers)

    return store.plot_rewards(rewards, horizon)


if __name__ == '__main__':
    app.run_server(host='0.0.0.0', debug=True)
