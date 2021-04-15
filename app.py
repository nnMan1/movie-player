from flask import Flask
from flask import render_template, Blueprint, send_file, Markup
from flask import request
import time
import requests
from zipfile import ZipFile
import os
import webvtt
from io import BytesIO
from pycaption import SRTReader, WebVTTWriter, CaptionConverter
import sys


from api import Seedr, YTS, Movie, Subtitle

app = Flask(__name__)

seedr = Seedr();
  
login_resp = seedr.login("dosljakvelibor@gmail.com", "natasa12@")


@app.route("/")
def index():
    searchQuery = request.args.get('q')
    if searchQuery == None:
        searchQuery = ""

    movies = YTS.search__(searchQuery)
    print(movies)

    movie = {
        "url": "https://de15.seedr.cc/ff_get/881668353/Pirates.Of.The.Caribbean.Dead.Men.Tell.No.Tales.2017.720p.BluRay.x264-[YTS.AG].mp4?st=bKmtfXGGaf5Vo_OMD8ycqA&e=1617305713",
        "name": "Pirates of caribbean"
    }

    return render_template("searchPage.htm", movies = movies)

@app.route("/get-movie/")
def getMovie():
    id = request.args.get('id')

    movie = YTS.getById__(id)

    print(movie)

    return render_template("movie.htm", movie = movie)

@app.route("/play/")
def play():
    magnet = request.args.get('magnet')
    imdb_code = request.args.get("imdb_code")

    print(magnet)
    
    seedr.delete_folders()
    

    seedr.add_torrent(magnet)
    
    
    files = seedr.get_all_files()

    caption = subtitle()

    while(len(files)==0):
        files = seedr.get_all_files()
        time.sleep(1)

    

    url = ""
    for file in [video for video in files if video["play_video"]]:
        url = seedr.get_file_url(file)["url"]

    data = {
        "url": url,
        "imdb_code": imdb_code,
        "caption": caption
    }

    return render_template("play.htm", data = data)

@app.route("/subtitle/")
def subtitle():
    imdb_code = request.args.get("imdb_code")
    
    subtitleUrl = Subtitle.get__(imdb_code)

    print(imdb_code)

    print("Subtitle url = ", subtitleUrl)
    sys.stdout.flush()

    if(subtitleUrl != ""):
        r = requests.get(subtitleUrl, allow_redirects=True)

        filebytes = BytesIO(r.content)
            
        myzipfile = ZipFile(filebytes)

        print(myzipfile.namelist())
        sys.stdout.flush()

        subtitle = myzipfile.open(myzipfile.namelist()[0])

        try:
            return subtitle.read().decode("utf8")
        except:
            try:
                return subtitle.read().decode("utf16")
            except:
                return subtitle.read().decode("ascii")
        
    return ""

    


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=8090, debug=True)
    
