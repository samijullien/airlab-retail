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

This application was written using Python 3.7 and R, including the R package `copula` to generate items.

It was packaged using Docker 19.03.13 for easy setup and usage regardless of operating system.

## Usage

With Docker:

	docker pull shubhaguha/retail:latest
	docker run -ti --rm -p 8050:8050 shubhaguha/retail:latest

Without Docker:

	# Checkout this git repository
	git clone https://github.com/samijullien/airlab-retail.git
	cd airlab-retail

	# Use a virtual environment
	python3 -m venv env
	source env/bin/activate

	# Install and run
	python3 setup.py install
	python3 app.py

View the grocery store simulation in your web browser at <http://localhost:8050/>.
