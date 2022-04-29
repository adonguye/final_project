**Introduction**

This project aims to create a simple web application that returns information about top trending movies that are associated with languges. Some modules are adopted to allow this application to access data efficiently web API and manipulate the data using SQLite into information. Then, Flask, Pygal and Plotly are used for data visualization on this website.

**Data Sources**
1. The Movie DB, which is the data source for the table "Top Movies" in the database
https://developers.themoviedb.org/3/movies/get-top-rated-movies
2. The web from Wiki, which is the data source for the table "Original Language of Movie" in the database.
https://en.wikipedia.org/wiki/List_of_ISO_639-1_codes

**Data Processing**
1. Create the table named “Top Movies” in the database
2. Create the table named “Original Language of Movie"” in the database
3. Make graphs showing different interesting things about the data
4. Create a graph of five languages and what movies (like 50) are connected to it
5. Fill the table named Original Language of Movie with data that are retrieved from scraping the Movie DB website.

**Data Presentation**
This app is represented on a website by using Flask, Pygal and Plotly to show the data.
Once the Flask application is running, the user should navigate to "http://127.0.0.1:5000/" in a web browser (or whatever port Flask is hosting the site on, if port 5000 is already in use on your system).
- Use http://127.0.0.1:5000/ratings to see charts

**Run the Program**

Step 1:
- Apply an API Key for the MovieDB, and languge site
- Create a new python file "secret.py" in the same folder as "webapp.py". And add the code:

Step 2:
- Install packages
    - import json
    - import langcodes
    - import secret
    - import requests
    - import sqlite3
    - import pygal
    - from flask import Flask, render_template, Markup # tools that will make it easier to build on things
    - from flask_sqlalchemy import SQLAlchemy # handles database stuff for us - need to pip install flask_sqlalchemy in your virtual env, environment, etc to use this and run this
    - from bs4 import BeautifulSoup
    - import requests
    - import lang_secret
    - import json
    - import urllib.request
    - import urllib.error
    - import string
    - import sys

Step 3:
- Run app.py


