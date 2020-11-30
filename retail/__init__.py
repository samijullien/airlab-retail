import dash

from .retail_traj_info import RetailTrajInfo
from .layout import serve_layout_func


def create_app():
    external_stylesheets = [
        # Dash CSS
        'https://codepen.io/chriddyp/pen/bWLwgP.css',
        # Loading screen CSS
        'https://codepen.io/chriddyp/pen/brPBPO.css',
    ]

    app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
    app.config.suppress_callback_exceptions = True

    img = app.get_asset_url('grocery-beta.png')
    app.layout = serve_layout_func(img)  # should be a function, not an object

    return app
