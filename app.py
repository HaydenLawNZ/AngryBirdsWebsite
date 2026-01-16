from flask import Flask, render_template, request

import sqlite3
from sqlite3 import Error

app = Flask(__name__)
DATABASE = "/Users/haydenlaw/Desktop/DATABASE ASSESSMENT/bird.db"

def create_connection(db_file):
    try:
        connection=sqlite3.connect(db_file)
        return connection
    except Error as e:
        print(e)
    return None

@app.route('/')
def render_home():
    return render_template("index.html")

@app.route('/webpages')
def render_webpages():
    sort = request.args.get('sort')
    if sort is None:
        sort = "ID"

    if sort in []:
        query = f"SELECT ID, Name, Type, Gender, Species, Colour, Side, Ability, Angry_Birds_Game, Level_Introduction, Strength, Size FROM bird_info WHERE Type='Bird' ORDER BY {sort} ASC"
    else:
        query = f"SELECT ID, Name, Type, Gender, Species, Colour, Side, Ability, Angry_Birds_Game, Level_Introduction, Strength, Size FROM bird_info WHERE Type='Bird' ORDER BY {sort} COLLATE NOCASE ASC"

    con = create_connection(DATABASE)
    cur = con.cursor()
    cur.execute(query)
    tag_list = cur.fetchall()
    con.close()

    return render_template("webpages.html", tags=tag_list)


@app.route('/styles')
def render_styles():
    sort = request.args.get('sort')
    if sort is None:
        sort = "ID"

    if sort in []:
        query = f"SELECT ID, Name, Type, Gender, Species, Colour, Side, Ability, Angry_Birds_Game, Level_Introduction, Strength, Size FROM bird_info WHERE Type='Pig' ORDER BY {sort} ASC"
    else:
        query = f"SELECT ID, Name, Type, Gender, Species, Colour, Side, Ability, Angry_Birds_Game, Level_Introduction, Strength, Size FROM bird_info WHERE Type='Pig' ORDER BY {sort} COLLATE NOCASE ASC"

    con = create_connection(DATABASE)
    cur = con.cursor()
    cur.execute(query)
    tag_list = cur.fetchall()
    con.close()
    return render_template("styles.html", tags=tag_list)

@app.route('/search', methods=['GET', 'POST'])
def render_search():
    search = request.form['search']
    sort_by = request.form['sort_by']

    if not search and not sort_by:
        error_message = "Please enter a search query or select a column for sorting."
        return render_template('index.html', error_message=error_message)

    query = "SELECT ID, Name, Type, Gender, Species, Colour, Side, Ability, Angry_Birds_Game, Level_Introduction, Strength, Size FROM bird_info WHERE ID LIKE ? OR Type LIKE ? OR Name LIKE ? OR Gender LIKE ? OR Species LIKE ? OR Colour LIKE ? OR Side LIKE ? OR Ability LIKE ? OR Angry_Birds_Game LIKE ? OR Level_Introduction LIKE ? OR Strength LIKE ? OR Size LIKE ?"

    if sort_by:
        query += f" ORDER BY {sort_by}"

    search = "%" + search + "%"

    con = create_connection(DATABASE)
    cur = con.cursor()
    cur.execute(query, (search, search, search, search, search, search, search, search, search, search, search, search))
    tag_list = cur.fetchall()
    con.close()

    if not tag_list:
        error_message = "No matching results found."
        return render_template('index.html', error_message=error_message)

    return render_template("webpages.html", tags=tag_list)

if __name__ == '__main__':
    app.run()