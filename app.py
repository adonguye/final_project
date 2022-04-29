import json
import langcodes
import secret
import requests
import sqlite3
import pygal
from flask import Flask, render_template, Markup # tools that will make it easier to build on things
from flask_sqlalchemy import SQLAlchemy # handles database stuff for us - need to pip install flask_sqlalchemy in your virtual env, environment, etc to use this and run this
from bs4 import BeautifulSoup
import requests
import lang_secret
import json
import urllib.request
import urllib.error
import string
import sys

# ### database
# import sqlite3
# #make database
# conn = sqlite3.connect('database.db')
# #create a cursor
# c = conn.cursor()
# #create a table
# c.execute("""CREATE TABLE movies (
#         id DATATYPE,
#         overview DATATYPE,
#         original_language DATATYPE,
#         popularity DATATYPE,
#         vote_count DATATYPE,
#         vote_average DATATYPE,
#         poster_path DATATYPE,
#         title DATATYPE,
#         name DATATYPE,
#         release_date DATATYPE
#     )""")
# #NULL
# #INTERGER
# #REAL
# #TEXT
# #BLOB
# conn.commit()
# conn.close()

# def db_create_table_topmovies():
#     ''' create the table named "Top Movies" in the database
#     Parameters
#     ----------
#     None
#     Returns
#     -------
#     none
#     '''
#     conn = sqlite3.connect(DB_NAME) #create a database. It will create a connection object.
#     cur = conn.cursor() # To create a table in the relation database, With this cursor object, we can now execute the commands and queries on the database.
#     create_topmovies_sql = '''
#         CREATE TABLE IF NOT EXISTS "Top Movies" (
#             "release_date" INTEGER PRIMARY KEY UNIQUE,
#             "id" TEXT NOT NULL,
#             "original_title" TEXT NOT NULL,
#             "original_language" INTEGER NOT NULL,
#             "title" REAL NOT NULL,
#             "popularity" TEXT NOT NULL,
#             "vote_count" TEXT NOT NULL
#             "vote_average" TEXT NOT NULL
#         )
#     '''
#     # cur.execute(drop_cities_sql)
#     cur.execute(create_topmovies_sql)
#     conn.commit()
#     conn.close()

#figure out how to get info to print

API_KEY = secret.API_KEY #API_KEY is located on the secret.py file
DB_NAME = 'tableResult.sqlite'
headers = {
    'User-Agent': 'UMSI 507 Course Final Project',
    'From': 'adonguye@umich.edu',
    'Course-Info': 'https://si.umich.edu/programs/courses/507'
}
### figure out database --- https://flask-sqlalchemy.palletsprojects.com/en/2.x/quickstart/#a-minimal-application

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/test.db' #this is the name of the database
#manage tables
db = SQLAlchemy(app)


class User(db.Model):
    #below are the columns we want to see
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)

    def __repr__(self):
        return '<User %r>' % self.username

#from a import db
db.create_all()

#### my urls

baseurl = 'https://developers.themoviedb.org/3/movies/get-top-rated-movies'
baseurl2 = 'https://www.loc.gov/standards/iso639-2/php/code_list.php'
#https://en.wikipedia.org/wiki/List_of_ISO_639-1_codes'
#https://api.joshuaproject.net/v1/docs/column_descriptions/languages

#########################################
############# Flask Web App #############
#########################################

@app.route('/')
def home():
    req = requests.get(f'https://api.themoviedb.org/3/trending/all/day?api_key={secret.API_KEY}')
    json_data = req.json()
    results = json_data['results']
    movies = convert_to_movie_objects(results=results)

    return render_template('base.html', title='Trending by Year', trending=movies)
    #return render_template('base.html', title='Trending by Year', trending=results, bar_chart=bar_chart, scatter_chart=

@app.route('/ratings')
def top():
    req = requests.get(f'https://api.themoviedb.org/3/trending/all/day?api_key={secret.API_KEY}')
    json_data = req.json()
    results = json_data['results']
    print(results) #all the info printed out 
    movies = convert_to_movie_objects(results)
    movies_objs = map(lambda data: Movie(data=data), results)
    # Get bar chart of movies by rating
    rating_chart = pygal.Bar()
    rating_chart.title = 'Ratings of Movies Trending Today'
    rating_chart.x_labels = map(lambda movie: movie.title, movies_objs)
    for movie in movies_objs:
        rating_chart.add(movie.title, movie.vote_average)

    rating_chart = rating_chart.render_data_uri()

    top_movie = max(movies, key=lambda movie: movie.vote_average)

    # ––––– GET more details about the top movie like budget, genre, actors, etc.
    top_movie_details = get_movie_details(top_movie.id)

    print('TOP MOVIE DETAILS: ', top_movie_details)
    return render_template('ratings.html',
        title='Top Movies',
        ratings_chart=rating_chart,
        top_movie=top_movie,
        top_movie_details=top_movie_details
    )

def get_movie_details(movie_id):
    req = requests.get(f'https://api.themoviedb.org/3/movie/{movie_id}?api_key={secret.API_KEY}')
    json_data = req.json()
    return json_data

def convert_to_movie_objects(results):
    movies = []
    for data in results:
        movie = Movie(data=data)
        movies.append(movie)
    return movies

class Movie:
    '''definition of top_rated
    Instance Attributes
    -------------------
    overview: string
        an overiew of the top rated movie
    release_date: string
        the release date of the top rated movie instance
    id: integer
        an id of the top rated movie instance in the data
    original_title: string
        the original title of the top rated movie instance
    original_language: string
        the original language of the movie
    title: string
        the title of the top rated movie in english
    popularity: number
        the popularity
    vote_count: integer
        the vote count that goes in the vote average of the movie
    vote_average: number
        the vote average of the top rated movie
'''

    def __init__(self, data):
        self.id = data['id']
        self.overview = data['overview']
        self.original_language = data['original_language']
        self.popularity = data['popularity']
        self.vote_count = data['vote_count']
        self.vote_average = data['vote_average']
        self.poster_path = data['poster_path']
        self.title = data['title'] if 'title' in data else data['name']
        if 'release_date' in data:
            self.release_date = data['release_date']

##### get production info

@app.route('/production')
def side():
    req = requests.get(f'https://api.themoviedb.org/3/movie?api_key={secret.API_KEY}')
    json_data = req.json()
    results = json_data['results']
    movies = convert_to_production_objects(results)
    productions_objs = map(lambda data: Production(data=data), results)
    # Get bar chart of productions --in process 
    production_chart = pygal.Bar()
    production_chart.title = 'Movies Production'
    production_chart.x_labels = map(lambda production: production.title, productions_objs)
    for production in productions_objs:
        production_chart.add(production.title, production.vote_average)

    production_chart = production_chart.render_data_uri()

    top_production = max(movies, key=lambda movie: movie.vote_average)

    # ––––– GET more details about the top movie like budget, genre, actors, etc.
    top_production_details = get_production_details(top_production.id)

    print('TOP MOVIE DETAILS: ', top_production_details)
    return render_template('production.html',
        title='Top Production',
        production_chart=production_chart,
        top_production=top_production,
        top_production_details=top_production_details
    )

def get_production_details(movie_id):
    req = requests.get(f'https://api.themoviedb.org/3/movie/{movie_id}?api_key={secret.API_KEY}')
    json_data1 = req.json()
    print(json_data1)

def convert_to_production_objects(results):
    Productions = []
    for data in results:
        production = Production(data=data)
        Productions.append(production)
    return Productions

class Production:
    '''definition of Production_company
    Instance Attributes
    -------------------
    original_language: string
        orignal language of the movie
    production_companies: array[object]
        array of the production company info including name, id, logo path, and origin country
    production_countries: array[object]
        array of the production country info including iso_3166_1 and name
    spoken_languages: array[object]
        the spoken_languages movie instance
    imdb_id: string or null
        the imdb id of the movie
'''
    def __init__(self, data):
        self.original_language = data['original_language']
        self.production_companies = data['production_companies']
        # self.production_countries = data['production_companies']
        # self.spoken_languages = data['spoken_languages'] #how do I look at this seperately istead of array?  iso_639_1, langs
        # self.imdb_id = data['imdb_id']

# ### language info for iso API. the wiki page I wanted to use orignally was too messy

# @app.route('/lang')
# # set some important variables
# def lang():
#     req = requests.get(f'https://api.joshuaproject.net/v1/docs/column_descriptions/languages.json?api_key={lang_secret.keyz}')
#     json_data = req.json()
#     results = json_data['results']
#     langs = convert_to_lang_objects(results=results)

#     return render_template('base.html', title='Languages', trending=langs)

# class iso_language_codes:
#     '''definition of language_codes
#     Instance Attributes
#     -------------------
#     language_name: string
#         name of language
#     language_code: string
#         2 letter code of language
# '''
#     def __init__(self, data):
#         self.ROL3 = data['ROL3']
#         self.ROG3 = data['ROG3']
#         self.WorldSpeakers = data['WorldSpeakers']

# def get_lang_details(id):
#     req = requests.get(f'https://api.joshuaproject.net/v1/docs/column_descriptions/languages.json{id}?api_key={lang_secret.keyz}')
#     json_data = req.json()
#     return json_data

# def convert_to_lang_objects(results):
#     langs = []
#     for data in results:
#         movie = Movie(data=data)
#         langs.append(movie)
#     return langs

##### simp lang #####
#def get_languagemess_details(movie_id):
#    req = requests.get(f'https://www.loc.gov/standards/iso639-2/php/code_list.php')
#    json_data = req.json()
#    return json_data

#def convert_to_languagemess_objects(results):
#    movies = []
#    for data in results:
#        movie = Movie(data=data)
#        movies.append(movie)
#    return movies


headers = {
    'Access-Control-Allow-Origin': '*',
    'Access-Control-Allow-Methods': 'GET',
    'Access-Control-Allow-Headers': 'Content-Type',
    'Access-Control-Max-Age': '3600',
    'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:52.0) Gecko/20100101 Firefox/52.0'
    }
#https://www.w3.org/WAI/ER/IG/ert/iso639.htm
url = "https://www.loc.gov/standards/iso639-2/php/code_list.php"
req = requests.get(url, headers)
soup = BeautifulSoup(req.content, 'html.parser')
#print(soup.prettify())


#########################################
############### Caching #################
#########################################

def load_cache(cache_file_name):
    '''Load response text cache if already generated, else initiate an empty dictionary.
    Parameters
    ----------
    None
    Returns
    -------
    cache: dictionary
        The dictionary which maps url to response text.
    '''
    try:
        cache_file = open(cache_file_name, 'r')
        cache_file_contents = cache_file.read()
        cache = json.loads(cache_file_contents)
        cache_file.close()
    except:
        cache = {}
    return cache

def save_cache(cache, cache_file_name):
    '''Save the cache
    Parameters
    ----------
    cache: dictionary
        The dictionary which maps url to response.
    Returns
    -------
    None
    '''
    cache_file = open(cache_file_name, 'w')
    contents_to_write = json.dumps(cache)
    cache_file.write(contents_to_write)
    cache_file.close()

CACHE_FILE = 'cache.json'
CACHE_DICT = load_cache(CACHE_FILE)

#########################################
########### Data Processing #############
#########################################

# def db_create_table_topmovies():
#     ''' create the table named "Top Movies" in the database
#     Parameters
#     ----------
#     None
#     Returns
#     -------
#     none
#     '''
#     conn = sqlite3.connect(DB_NAME) #create a database. It will create a connection object.
#     cur = conn.cursor() # To create a table in the relation database, With this cursor object, we can now execute the commands and queries on the database.
#     # drop_movies_sql = 'DROP TABLE IF EXISTS "Movies"'
#     create_topmovies_sql = '''
#         CREATE TABLE IF NOT EXISTS "Top Movies" (
#             "release_date" INTEGER PRIMARY KEY UNIQUE,
#             "id" TEXT NOT NULL,
#             "original_title" TEXT NOT NULL,
#             "original_language" INTEGER NOT NULL,
#             "title" REAL NOT NULL,
#             "popularity" TEXT NOT NULL,
#             "vote_count" TEXT NOT NULL
#             "vote_average" TEXT NOT NULL
#         )
#     '''
#     # cur.execute(drop_cities_sql)
#     cur.execute(create_topmovies_sql)
#     conn.commit()
#     conn.close()

# def db_create_table_iso_language_codes():
#     ''' create the table named "iso_language_codes" in the database
#     Parameters
#     ----------
#     None
#     Returns
#     -------
#     none
#     '''
#     conn = sqlite3.connect(DB_NAME)
#     cur = conn.cursor()
#     # drop_iso_language_codes_sql = 'DROP TABLE IF EXISTS "language"'
#     create_iso_language_codes_sql = '''
#         CREATE TABLE IF NOT EXISTS "language" (
#             "language_name" INTEGER PRIMARY KEY AUTOINCREMENT,
#             "language_code" INTEGER NOT NULL,
#         )
#     '''
#     # cur.execute(drop_language_sql)
#     cur.execute(create_iso_language_codes_sql)
#     conn.commit()
#     conn.close()

# def construct_unique_key(baseurl, params):
#     ''' constructs a key that is guaranteed to uniquely and
#     repeatably identify an API request by its baseurl and params
#     Parameters
#     ----------
#     baseurl: string
#         The URL for the API endpoint
#     params: dictionary
#         A dictionary of param: param_value pairs
#     Returns
#     -------
#     string
#         the unique key as a string
#     '''
#     param_strings = []
#     connector = '_'
#     for k in params.keys():
#         param_strings.append(f'{k}_{params[k]}')

#     param_strings.sort()
#     unique_key = baseurl + connector + connector.join(param_strings)
#     return unique_key

def make_url_request_using_cache(url_or_uniqkey, params=None):
    '''Given a url, fetch if cache not exist, else use the cache.

    Parameters
    ----------
    url: string
        The URL for a specific web page
    cache_dict: dictionary
        The dictionary which maps url to response text
    params: dictionary
        A dictionary of param: param_value pairs

    Returns
    -------
    cache[url]: response
    '''
    if url_or_uniqkey in CACHE_DICT.keys():
        print('Using cache')
        return CACHE_DICT[url_or_uniqkey]

    print('Fetching')
    if params == None: # dictionary: url -> response.text
        # time.sleep(1)
        response = requests.get(url_or_uniqkey, headers=headers)
        CACHE_DICT[url_or_uniqkey] = response.text
    else: # dictionary: uniqkey -> response.json()
        endpoint_url = 'https://developers.themoviedb.org/3/movies/get-top-rated-movies'
        response = requests.get(endpoint_url, headers = headers, params=params)
        CACHE_DICT[url_or_uniqkey] = response.json()
        print(CACHE_DICT[url_or_uniqkey])

    save_cache(CACHE_DICT, CACHE_FILE)
    return CACHE_DICT[url_or_uniqkey]

# ##
# '''def construct_unique_key(baseurl, params):
#     param_strings = []
#     connector = '_'
#     for k in params.keys():
#         param_strings.append(f'{k}_{params[k]}')
#     param_strings.sort()
#     unique_key = baseurl + connector +  connector.join(param_strings)
#     return unique_key '''


#endpoint_url = 'https://api.twitter.com/1.1/search/tweets.json'
#params = {'q': '@umsi', 'count':'100', ‘lang’: ‘en'}
#print(construct_unique_key(endpoint_url, params))




if __name__ == '__main__':
    app.run(debug=True)