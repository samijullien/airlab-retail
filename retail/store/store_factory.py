import torch
import torch.distributions as d

from ..utility import CustomUtility
from .store_env import StoreEnv


class StoreFactory:

    @classmethod
    def create_store_env(cls, n_customers, n_items, max_stock, horizon,
                         freshness, seed, utility_fun, utility, weight_waste,
                         weight_sales, weight_availability, bias, variance,
                         leadtime_long, leadtime_fast, daily_buckets):
        if utility_fun == 'custom':
            utility_fun = CustomUtility(utility)
        bucketDist = d.uniform.Uniform(0, 1)
        sampled = bucketDist.sample((daily_buckets,))
        store_kwargs = {
            'bucket_customers': (n_customers*sampled/sampled.sum()).round(),
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
        return StoreEnv(**store_kwargs)
