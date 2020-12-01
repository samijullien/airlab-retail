import uuid

import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html


overview_card = dbc.Card([
    html.H2('Manage your own store and see how it performs!', className="card-title"),
    html.P("The idea behind this web application is for you to customise your own store! But will you be able to avoid wasting? "
    "Once you've opened your brand new store, it is time to define your scoring metric - will it help you in understanding the underlying dynamics? "
    "Will you be able to order the right amount of items, to reduce the ecological footprint of your store?", className="card-text"),
], body=True, style={'border': 'none'})


store_param_card_group = dbc.CardColumns([
    dbc.Card([
        html.Label('Customers', htmlFor="n_customers", className="card-title"),
        dbc.Input(id="n_customers", type="number", value=500, min=0, max=2000, step=1, className="card-text"),
    ], body=True),
    dbc.Card([
        html.Label('Items', htmlFor="n_items", className="card-title"),
        dbc.Input(id="n_items", type="number", value=30, min=5, max=100, step=1, className="card-text"),
    ], body=True),
    dbc.Card([
        html.Label('Stock size', htmlFor="max_stock", className="card-title"),
        dbc.Input(id="max_stock", type="number", value=600, min=0, max=2000, step=1, className="card-text"),
    ], body=True),
    dbc.Card([
        html.Label('Horizon', htmlFor="horizon", className="card-title"),
        dbc.Input(id="horizon", type="number", value=91, min=40, max=1000, step=1, className="card-text"),
    ], body=True),
    dbc.Card([
        html.Label('Bias', htmlFor="bias", className="card-title"),
        dbc.Input(id="bias", type="number", value=0.0, min=-1, max=1, step=.01, className="card-text"),
    ], body=True),
    dbc.Card([
        html.Label('Variance', htmlFor="variance", className="card-title"),
        dbc.Input(id="variance", type="number", value=0.0, min=0, max=1, step=.01, className="card-text"),
    ], body=True),
    dbc.Card([
        html.Label('ON Leadtime', htmlFor="leadtime_fast", className="card-title"),
        dbc.Input(id="leadtime_fast", type="number", value=0, min=0, max=10, step=1, className="card-text"),
    ], body=True),
    dbc.Card([
        html.Label('ID Leadtime', htmlFor="leadtime_long", className="card-title"),
        dbc.Input(id="leadtime_long", type="number", value=1, min=1, max=10, step=1, className="card-text"),
    ], body=True),
    dbc.Card([
        html.Label('Buckets', htmlFor="daily_buckets", className="card-title"),
        dbc.Input(id="daily_buckets", type="number", value=4, min=1, max=12, step=1, className="card-text"),
    ], body=True),
    dbc.Card([
        html.Label('Seed', htmlFor="seed", className="card-title"),
        dbc.Input(id="seed", type="number", placeholder="seed", min=1, max=100000, step=1, className="card-text"),
    ], body=True)
])


store_creation_card = dbc.Card([
    html.H2('Store creation', className="card-title"),
    html.P("The first step is to create your store. Enter below the characteristics to define your store."
    "This will also generate an item assortment, which can be replicated by entering a seed.", className="card-text"),
    store_param_card_group,
], body=True, style={'border': 'none'})


success_metric_card = dbc.Card([
    html.H2('Success metric', className="card-title"),
    html.P('Now, it is time to define your success metric. You can pick one and specify weights, or select "Custom" and enter your own metric - containing the letters "a" for availability, "s" for sales, and  "w" for waste.', className="card-text"),
    dbc.Card(dcc.Dropdown(id='utility_fun', options=[
                                {'label': 'Cobb-Douglas utility function',
                                'value': 'cobbdouglas'},
                                {'label': 'Log Linear utility function',
                                'value': 'loglinear'},
                                {'label': 'Linear utility function',
                                'value': 'linear'},
                                {'label': 'Custom utility function',
                                'value': 'custom'}
                            ],
                            value='cobbdouglas'), body=True, style={'border': 'none'}),
    dbc.CardColumns([
        dbc.Card([
            html.Label('Waste weight', htmlFor="weight_waste", className="card-title"),
            dbc.Input(id="weight_waste", type="number", min=0, max=3, step=.01, value=0.5, className="card-text"),
        ], body=True),
        dbc.Card([
            html.Label('Sales weight', htmlFor="weight_sales", className="card-title"),
            dbc.Input(id="weight_sales", type="number", min=0, max=3, step=.01, value=0.5, className="card-text"),
        ], body=True),
        dbc.Card([
            html.Label('Availability', htmlFor="weight_availability", className="card-title"),
            dbc.Input(id="weight_availability", type="number", min=0, max=3, step=.01, value=0.5, className="card-text"),
        ], body=True),
    ], id="weights"),
    dbc.Card([
        html.Div('Custom function definition', className="card-title"),
        dbc.Input(id='utility', type='text', placeholder="Contains a, w, and s", className="card-text"),
    ], id='custom_utility', body=True),
], body=True, style={'border': 'none'})


output_items_card = dbc.Card([
    html.H2('Items', className="card-title"),
    html.P("Below, you can see the items present in your store, with their price and cost. "
    "The color indicates how long you can keep them for.", className="card-text"),
    dcc.Graph(id='output'),
], body=True, style={'border': 'none'})


freshness_card = dbc.Card([
    html.H2('Freshness level', className="card-title"),
    html.P("Freshness represents how long your items can be stored before the expiration date. "
    "The fresher the item, the shorter the time it can be stored! "
    "Overall, you can see this as the difficulty level. Try moving the slider!", className="card-text"),
    dcc.Slider('freshness', min=1, max=100, value=1, marks={
        1: 'Standard',
        10: 'Fresher items',
        25: 'Very fresh',
        50: 'Very very fresh',
        75: 'Too fresh',
        100: 'Bakery mode',
    }),
], body=True, style={'border': 'none'})


ordering_algorithm_card = dbc.Card([
    html.H2('Order algorithm', className="card-title"),
    dcc.Markdown('''
    The main goal is to adjust the number of each item you order for your store. To do so, you can build an expression around the following:
    - n_customers, the number of customers expected
    - forecast, the purchase probability of each of those customers
    - stock, the current stock (or inventory position) of items.
    ''', className="card-text"),
    dbc.Card([
        html.Div('Order input', className="card-title"),
        dbc.Input(value='forecast*n_customers - stock', type='text', id='order', className="card-text"),
    ], body=True),
], body=True, style={'border': 'none'})


tab1_content = dbc.Card(
    dbc.CardBody([
        overview_card,
        store_creation_card,
        success_metric_card,
        dbc.Button('Create store', id='create', color="primary", className="mr-1", block=True),
        output_items_card,
    ]), className="mt-3",
)


tab2_content = dbc.Card(
    dbc.CardBody([
        freshness_card,
        ordering_algorithm_card,
        dbc.Button('Order!', id='order_button', color="primary", className="mr-1", block=True),
        dcc.Graph(id='output2'),
    ]), className="mt-3",
)


tabs = dbc.Tabs([
    dbc.Tab(tab1_content, label="STORE GENERATOR"),
    dbc.Tab(tab2_content, label="ORDERING SIMULATION"),
])


def serve_layout_func(img):
    session_id = str(uuid.uuid4())

    def _serve_layout():
        return dbc.Container([
            dcc.Store(id="store"),
            html.Div(session_id, id='session-id', style={'display': 'none'}),
            dbc.Row([
                dbc.Col(html.H1(children='RetaiL Store Generator and Management')),
                dbc.Col(html.Img(src=img, style={'width': 200, 'float': 'right'})),
            ]),
            tabs,
        ], style={'padding': '50px'})

    return _serve_layout
