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

## Requirements

RetaiL requires R, with the copula package to generate items. Moreover, RetaiL requires rlpyt in its version 0.1.1.dev0.
RetaiL requires Python 3.6 or 3.7.

## Installation

	# Checkout this git repository
	# Create a virtual environment
	python3 -m venv env
	# Activate the environment
	source env/bin/activate
	# Install the latest version of pip
	pip3 install --upgrade pip
	# Install the dependencies
	pip install -r requirements.txt

## Usage

Run server:

	python3 app.py

View the grocery store simulation in your web browser at <http://localhost:8050/>.

## Development

A development environment can be set up regardless of the developer's operating system by using Docker.

	docker build . -t retail
	docker run -ti --rm -p 8050:8050 retail
