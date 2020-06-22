# RetaiL

## Overview

__RetaiL__ is a library aimed at improving experimentation in a grocery store context, to reduce generated waste. We think it is a great addition for both reinforcement learning and supply chain researchers, but also to data scientists working in retail environments.

We design RetaiL around two main components: 

 * [Item Generation](https://github.com/samijullien/airlab-retail/tree/master/retail/item_generation) contains the item Generation, scripted in R.
 * [Store environment](https://github.com/samijullien/airlab-retail/tree/master/retail/retail.py) 

We additionally provide three usage examples of RetaiL:

 * [Transporation cost impact on marginal ordering cost](Transportation_cost.ipynb)
 * [Daily customer distribution impact on ordering policy performance](Intraday_dist_impact.ipynb)
 * [Risk assesment of an ordering policy](cvar_computation.ipynb)

## Installation

RetaiL requires R, with the copula package to generate items. Moreover, RetaiL requires rlpyt in its version 0.1.1.dev0.
RetaiL requires Python 3.7 and virtualenv. You can get the RetaiL code running as follows:

1. Checkout this git repository
1. Create a virtual environment with `python3.6 -m venv env`
1. Activate the environment with `source env/bin/activate`
1. Install the latest version of pip with `pip install --upgrade pip`
1. Install the dependencies with `pip install -r requirements.txt`

