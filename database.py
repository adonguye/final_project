### database
import sqlite3
#make database
conn = sqlite3.connect('moviewatchers.db')
#create a cursor
c = conn.cursor()
#create a table
c.execute("""CREATE TABLE movies (
        id integer,
        overview text,
        original_language text,
        popularity real,
        vote_count integer,
        vote_average real,
        title text,
        name blob,
        release_date text
    )""")

c.execute("INSERT INTO moviewatchers VALUES ('')")
#commit our command
conn.commit()

#close our connection
conn.close()

#     overview: string
#         an overiew of the top rated movie
#     release_date: string
#         the release date of the top rated movie instance
#     id: integer
#         an id of the top rated movie instance in the data
#     original_title: string
#         the original title of the top rated movie instance
#     original_language: string
#         the original language of the movie
#     title: string
#         the title of the top rated movie in english
#     popularity: number
#         the popularity
#     vote_count: integer
#         the vote count that goes in the vote average of the movie
#     vote_average: number
#         the vote average of the top rated movie
# '''

#datatypes
# #NULL
# #INTERGER
# #REAL
# #TEXT
# #BLOB