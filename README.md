# TvCharts [[Live Site]](https://zyv1k.eu.pythonanywhere.com/tvcharts/)
See how much your favourite TV show has dropped in quality over time (according to IMDB ratings)...

I've scraped data for over 1000 most popular shows (nearly 100k episodes) and presented it in form of graphs. 
(Scraper is included in this repository.)
## Tech stack
Programming language: Python 3.7

Web Framework: Django 3

Database: SqLite3

API framework: Django REST API

Front-end: bootstrap 4, CSS3, JavaScript
## Installation
If for some reason you want to run this WebApp locally here is 'installation' instruction:
* Install python 3.7 +
* Open command line in folder containing *requirements.txt* and run:  
```
pip install requirements.txt
```
* Migrate database - run:
```
python manage.py migrate
```
* Populate database - run (and wait - it will take a while):
```
python load_scraped_data.py
```
* Start server - run:
```
python manage.py runserver
```
* Open http://127.0.0.1:8000/ in your browser