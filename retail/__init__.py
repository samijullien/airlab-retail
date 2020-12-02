import logging

import dash

from .retail_traj_info import RetailTrajInfo
from .layout import serve_layout_func


def create_app():
    # Initialize logging
    logging.basicConfig(level=logging.INFO, format='[%(asctime)s] [%(levelname)s] %(message)s')
    logging.info('Initialized logging')

    # Initialize app with external stylesheets
    app = dash.Dash(__name__, external_stylesheets=[
        # Dash CSS
        'https://codepen.io/chriddyp/pen/bWLwgP.css',
        # Loading screen CSS
        'https://codepen.io/chriddyp/pen/brPBPO.css',
    ])
    app.config.suppress_callback_exceptions = True

    # Set page title
    app.title = 'RetaiL'

    # As a function, the layout can be reloaded for each individual user,
    # allowing us to embed a hidden user-specific session ID in the HTML
    app.layout = serve_layout_func(app.get_asset_url('grocery-beta.png'))

    return app
