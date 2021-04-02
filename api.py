
# importing vlc module              
import os
import requests
import json
import time
import sys
import re

class Subtitle:
      def get__(imdb_code):
            response = requests.post("https://yifysubtitles.org/movie-imdb/{}".format(imdb_code))
            urls = re.findall("/subtitles/.*-serbian-yify-[0-9]*",response.text)
            if(len(urls) == 0):
                  return ""
            return re.sub("/subtitles/", "https://yifysubtitles.org/subtitle/", urls[0])+".zip"

class Movie(object):
    def __init__(self, *args):
        pass

    def __init__(self, movie_json):
        self.title = movie_json["title"]
        self.url = movie_json["url"]
        self.genres = movie_json["genres"]
        self.summary = movie_json["summary"]
        self.torrents = []

        for torrent in movie_json["torrents"]:
              self.torrents.append({
                "quality": torrent["quality"],
                "hash": torrent["hash"],
                "magnet": "magnet:?xt=urn:btih:{}&dn={}&tr=udp://open.demonii.com:1337/announce&tr=udp://tracker.openbittorrent.com:80".format(torrent["hash"], self.title)
              })

    def to_string(self):
          return "name: {}\n   magnet: {} \n\n".format(self.title, self.torrents[0]["magnet"])
       

class YTS(object):
      def __init__(self, *args):
            pass
    
      def search__(q):
            response = requests.post("https://yts.mx/api/v2/list_movies.json?query_term={}".format(q))
            movies_json = json.loads(response.text)["data"]["movies"]

            movies = []

            for movie in movies_json:
                  movies.append(Movie(movie))

            return movies_json

      def getById__(id):
            response = requests.post("https://yts.mx/api/v2/movie_details.json?movie_id={}".format(id))
            print(response.text)
            movie_json = json.loads(response.text)["data"]["movie"]

            for i in range(len(movie_json["torrents"])):
                  torrent = movie_json["torrents"][i]
                  title = movie_json["title"]
                  movie_json["torrents"][i]["magnet"] = "magnet:?xt=urn:btih:{}&dn={}&tr=udp://open.demonii.com:1337/announce&tr=udp://tracker.openbittorrent.com:80".format(torrent["hash"], title)

            return movie_json
        

class Seedr(object):
      
    def __init__(self):
        pass
    
    def login(self, username, password):
          body = {
                    "type": "login",
                    "grant_type": "password",
                    "client_id": "seedr_chrome",
                    "username": username,
                    "password": password
                  }

          response = requests.post("https://www.seedr.cc/oauth_test/token.php", data = body)
          parsed = json.loads(response.text)

          self.__access_token = parsed["access_token"]
        
    def __get_folders(self):
          response = requests.get("https://www.seedr.cc/api/folder?access_token=" + self.__access_token);
          return json.loads(response.text)

    def get_files_from_folder(self, folder):
          response = requests.get("https://www.seedr.cc/api/folder/{}?access_token={}".format(folder, self.__access_token));
          return json.loads(response.text)["files"]

    def get_all_files(self):
          folders = self.__get_folders()

          resp = []

          for folder in folders["folders"]:
                resp += self.get_files_from_folder(folder["id"])

          return resp

    def get_file_url(self, file):
          body = {
                    "access_token": self.__access_token,
                    "func": "fetch_file",
                    "folder_file_id": file["folder_file_id"]
                  }

          response = requests.post("https://www.seedr.cc/oauth_test/resource.php", data = body)
          parsed = json.loads(response.text)

          return parsed

    def add_torrent(self, magnet):
        body = {
                    "access_token": self.__access_token,
                    "func": "add_torrent",
                    "torrent_magnet": magnet
                  }

        response = requests.post("https://www.seedr.cc/oauth_test/resource.php", data = body)
        parsed = json.loads(response.text)

        return parsed
  
    def delete_folders(self):
          folders = self.__get_folders()["folders"]
          delete = []

          for folder in folders:
                delete.append({"id": folder["id"], "type":"folder"})

          print(delete)

          body = {
                    "access_token": self.__access_token,
                    "func": "delete",
                    "delete_arr": json.dumps(delete)
                  }

          response = requests.post("https://www.seedr.cc/oauth_test/resource.php", data = body)
          parsed = json.loads(response.text)

          return parsed

def openUrl(url):
      os.system("vlc \""+url + "\"")
      # instance = vlc.Instance()
      # player = instance.media_player_new()
      # media = instance.media_new(url)
      # player.set_media(media)
      # player.play()
      # time.sleep(10)
    

if __name__ == "__main__":

      print(Subtitle.get__("tt1790809"))

      # movie =YTS.getById__(29766)
      # print(json.dumps(movie, indent=4, sort_keys=True))
#   seedr = Seedr();
  
#   login_resp = seedr.login("dosljakvelibor@gmail.com", "natasa12@")

#   print(seedr.delete_folders())

#   search = str(sys.argv[1])
#   print(search)

#   movies = YTS.search__(search)
#   seedr.add_torrent([t["magnet"] for t in movies[0].torrents if t["quality"]=="720p"][0])
#   files = seedr.get_all_files()

#   while(len(files)==0):
#         files = seedr.get_all_files()
#         time.sleep(1)
  
#   for file in [video for video in files if video["play_video"]]:
#         openUrl(seedr.get_file_url(file)["url"])
#   files = seedr.get_all_files()

#   for file in [file for file in files if file["play_video"]]:
#     file_url = seedr.get_file_url(file)
#     print(file_url)

 