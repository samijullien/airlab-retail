# RetaiL

## Overview

__RetaiL__ is a library aimed at improving experimentation in a grocery store context, to reduce generated waste. We think it is a great addition for both reinforcement learning and supply chain researchers, but also to data scientists working in retail environments.

We presented part of RetaiL as a demo for NeurIPS 2020.

We design RetaiL around two main components: 

 * [Item Generation](https://github.com/samijullien/airlab-retail/tree/master/retail/item_generation) contains the item Generation, scripted in R.
 * [Store environment](https://github.com/samijullien/airlab-retail/tree/master/retail/retail.py) 

We additionally provide four usage examples of RetaiL:

 * [Experiments showing performance of classical heuristics and imitation learning](notebooks/Experiments.ipynb)
 * [Transporation cost impact on marginal ordering cost](notebooks/Transportation_cost.ipynb)
 * [Daily customer distribution impact on ordering policy performance](notebooks/Intraday_dist_impact.ipynb)
 * [Risk assesment of an ordering policy](notebooks/cvar_computation.ipynb)

## Requirements

This application was written using Python 3.7 and R, including the R package `copula` to generate items.

It was packaged using Docker 19.03.13 for easy setup and usage regardless of operating system.

Memcached requires libmemcached. On Mac OS:

	brew install libmemcached

## Usage

You can visit the running app at: <http://airlab-retail.northeurope.azurecontainer.io/>

### Local Development Server

With Docker Compose:

	docker-compose up

With Docker but no Docker Compose:

	# web app
	docker pull shubhaguha/retail:latest
	docker run -ti --rm --name retail-web -p 80:80 shubhaguha/retail:latest

	# external cache server
	docker run -ti --rm --name retail-memcached -p 11211:11211 memcached

	# network connecting these two running containers
	docker network create retail-network
	docker network connect retail-network retail-web
	docker network connect retail-network retail-memcached

Without Docker or Docker Compose:

	# Checkout this git repository
	git clone https://github.com/samijullien/airlab-retail.git
	cd airlab-retail

	# Use a virtual environment
	python3 -m venv env
	source env/bin/activate

	# Install and run
	python3 setup.py install
	python3 -m retail

View the grocery store simulation in your web browser at <http://localhost:8050/>.

## Development

### Build

To increment a version:

- Update the version in [setup.py](setup.py).
- Create a git tag with the same version, e.g. [0.1.1](https://github.com/samijullien/airlab-retail/releases/tag/0.1.1).
- Build and publish Docker image.

Docker commands:

	docker build . -t shubhaguha/retail:${VERSION} -t shubhaguha/retail:latest
	docker push shubhaguha/retail:${VERSION}
	docker push shubhaguha/retail:latest

### Deploy

This application is deployed in Microsoft Azure using Container Groups.

To deploy:

	./deploy/script.sh create

To check deployment status:

	./deploy/script.sh show

To view logs:

	./deploy/script.sh logs
