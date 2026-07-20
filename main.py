import flask as f
import mariadb
import os
import subprocess
import ast
import re
import random
import urllib
from ytmusicapi import YTMusic

app = f.Flask(__name__)

db_config = {
    'host': 'localhost',
    'port': 3306,
    'user': 'fred',
    'password': '1234',
    'database': 'Musik'
}

conn = mariadb.connect(**db_config)
cursor = conn.cursor()

yt = YTMusic()

@app.route("/")
def home():
    query = "SELECT id, name FROM albums"
    cursor.execute(query)

    albums = []
    for row in cursor:
        albums.append({"id":  row[0], "name": row[1]})

    return f.render_template("index.html", albums=albums)

@app.route("/new", methods=['GET', 'POST'])
def new():
    if f.request.method == 'POST':
        input_url = f.request.form.get("yt_url")
        
        query = urllib.parse.urlsplit(input_url)[3]
        playlist_id = urllib.parse.parse_qs(query)["list"][0]

        print(playlist_id)

        try:
            playlist = yt.get_playlist(playlist_id)
            yt_id = playlist["tracks"][0]["album"]["id"]
            album = yt.get_album(yt_id)
        except:
            return "Felaktig länk"

        album_query = "INSERT INTO albums (name, year, track_count) VALUES (?, ?, ?)"
        cursor.execute(album_query, (album["title"], album["year"], album["trackCount"]))
        conn.commit()
        album_id = cursor.lastrowid

        track_query = "INSERT INTO tracks (name, track_position, album_id) VALUES (?, ?, ?)"
        count = 1
        for track in album["tracks"]:
            cursor.execute(track_query, (track["title"], count, album_id))
            count += 1
        
        conn.commit()

        albums_path = "static/media/albums/"
        target_path = albums_path + str(album_id)
        os.mkdir(target_path)
        
        url = "https://music.youtube.com/playlist?list=" + playlist_id
        subprocess.run(["./download-media.sh", target_path, url])

        return f.redirect(f.url_for('home'))
    
    return f.render_template("new.html")

@app.route("/album/<album_id>")
def album(album_id):
    query1 = "SELECT name, date, track_count, duration FROM albums WHERE id = (?)"
    cursor.execute(query1, (album_id,))
    album_info = cursor.fetchone()

    query2 = "SELECT name, track_position FROM tracks WHERE album_id = (?) ORDER BY track_position"
    cursor.execute(query2, (album_id,))
    tracks = []
    for row in cursor:
        tracks.append([row[0], "{:05d}".format(row[1])])

    if album_info:
        name, date, track_count, duration = album_info

        return f.render_template("album.html", 
            name=name, date=date, track_count=track_count,
            duration=duration, tracks=tracks, album_id=album_id
        )
    else:
        return "", 404

if __name__ == "__main__":
    app.run()

