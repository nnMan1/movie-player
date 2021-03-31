from flask import Flask
from flask import render_template, Blueprint
from flask import request
import time

from api import Seedr, YTS, Movie

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

    seedr.delete_folders()

    seedr.add_torrent(magnet)

    files = seedr.get_all_files()

    while(len(files)==0):
        files = seedr.get_all_files()
        time.sleep(1)

    print(files)

    url = ""
    for file in [video for video in files if video["play_video"]]:
        url = seedr.get_file_url(file)["url"]

    return render_template("play.htm", url = url)

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=8080, debug=True)
    