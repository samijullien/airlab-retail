import os
import subprocess

import numpy as np
import pandas as pd
import plotly.express as px
import torch


name_df = pd.read_csv('Grocery_UPC_Database.csv')


class Assortment:

    def __init__(self, size, freshness=1, seed=None):
        self.size = size
        self.freshness = freshness
        self.seed = seed

        file_path = os.path.dirname(os.path.abspath(__file__))
        args = [str(size), str(seed), file_path]
        path_to_rscript = os.path.join(file_path,
                                       '../item_generation/assortmentGen.R')
        subprocess.call(['Rscript', path_to_rscript] + args,
                        universal_newlines=True)

        # os.system("Rscript item_generation\\assortmentGen.R " + str(size) + " " + str(seed))

        path_to_csv = os.path.join(file_path,
                                   '../item_generation/assortment.csv')
        df = pd.read_csv(path_to_csv)
        self.selling_price = torch.tensor(df.Price)
        self.cost = torch.tensor(df.Cost)

        # clamp base demand as some outliers in the data generation might ruin the purchase probability

        self.base_demand = torch.tensor(df.Base_Demand).clamp(0, 1000)
        self.shelf_lives = torch.round(torch.tensor(df.Shelf_life,
                                                    dtype=torch.float32)/freshness)
        self.dims = torch.tensor(df.iloc[:, 1:4].values)
        self.characs = torch.stack((self.selling_price, self.cost,
                                    self.shelf_lives)).t()

    # Functions for further improvement

    def changePrices(self, new_prices):
        # dosomething
        return NotImplemented

    def removeItems(self, items):
        # Also do something
        return NotImplemented

    def addItems(self, items):
        # do something again
        return NotImplemented

    def permuteItems(self):
        # dothewoogyboogy
        return NotImplemented

    def to_dataframe(self):
        return pd.DataFrame({
            'Cost': np.round(self.cost.numpy(), 2),
            'Price': np.round(self.selling_price.numpy(), 2),
            'Shelf life at purchase': self.shelf_lives.numpy(),
            'Name': name_df.sample(self.size).values.tolist(),
        })

    def scatter_plot(self):
        sc = px.scatter(self.to_dataframe(),
                        x='Cost', y='Price', color='Shelf life at purchase',
                        title='Generated items at your store', hover_name='Name',
                        hover_data={'Name': False,
                                    'Price': ":$,.2f",
                                    'Cost': ":$,.2f",
                                    'Shelf life at purchase': True})
        sc.update_yaxes(tickprefix="€")
        sc.update_xaxes(tickprefix="€")
        return sc
