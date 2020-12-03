import logging
import os

import dash
from dash.dependencies import Input, Output, State
from pymemcache.client.base import Client
from pymemcache import serde

from . import create_app
from .store import StoreFactory


# Dash server
app = create_app()

# Flask server (for gunicorn)
server = app.server

# Cache server
memcached_server = os.getenv('MEMCACHED_SERVER', 'localhost')
cache = Client(memcached_server, serde=serde.pickle_serde)
logging.info("Initialized client with memcached server at: %s", memcached_server)


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

    # Create StoreEnv
    store = StoreFactory.create_store_env(
        n_customers, n_items, max_stock, horizon, freshness, seed, utility_fun,
        utility, weight_waste, weight_sales, weight_availability, bias,
        variance, leadtime_long, leadtime_fast, daily_buckets)

    # Save to cache
    logging.info("Saving to cache under session ID: %s", session_id)
    cache.set(session_id, store, expire=300)

    # Get some stats
    stats = cache.stats()
    logging.info("Current cache size after save: %d items, %.1f MB",
                 stats[b'curr_items'], stats[b'bytes']/1000000.)

    # Scatter plot
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

    # Retrieve from cache
    logging.info("Retrieving from cache using session ID: %s", session_id)
    store = cache.get(session_id)

    # Run RL simulation
    rewards = store.run_to_completion(order, n_customers)

    # Plot rewards
    return store.plot_rewards(rewards, horizon)


if __name__ == '__main__':
    app.run_server(host='0.0.0.0', debug=True)


if __name__ != '__main__':
    gunicorn_logger = logging.getLogger('gunicorn.error')
    app.logger.handlers = gunicorn_logger.handlers
    app.logger.setLevel(gunicorn_logger.level)
