from flask import Flask
from flask import render_template, Blueprint, send_file, Markup
from flask import request
import time
import requests
import zipfile
import os
import webvtt
from pycaption import SRTReader, WebVTTWriter, CaptionConverter


from api import Seedr, YTS, Movie, Subtitle

app = Flask(__name__)

seedr = Seedr();
  
login_resp = seedr.login("fdpttubhmqiwnrakqa@wqcefp.com", "123456789")


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
    os.system("rm -r subtitle.zip")
    os.system("rm -r ./static/*.srt")
    
    subtitleUrl = Subtitle.get__(imdb_code)
    if(subtitleUrl != ""):
        r = requests.get(subtitleUrl, allow_redirects=True)
        with open("subtitle.zip", 'wb') as file:
            file.write(r.content)
            
        with zipfile.ZipFile("./subtitle.zip", 'r') as zip_ref:
            zip_ref.extractall("./static/")

        os.system("mv ./static/*.srt ./static/subtitle.srt")

        with open("./static/subtitle.srt", "r" , errors =  "replace",  encoding = 'ascii') as subtitle:
            content = subtitle.read()
            return content
        
    return ""

    


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=8090, debug=True)
    