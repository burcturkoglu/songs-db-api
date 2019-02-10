from flask import Flask, jsonify, url_for, redirect, request
from flask_pymongo import PyMongo
from flask_restful import Api, Resource
from pymongo import MongoClient
import re, os, json


app = Flask(__name__)
try:
    client = MongoClient(
        os.environ['DB_PORT_27017_TCP_ADDR'],
        27017)

    db = client.songs_db
except:
    app.config["MONGO_URI"] = "mongodb://localhost:27017/songs_db"
    db = PyMongo(app).db


"""
Throughout this project, songs.json data which contains several informations about different songs is used. 


"""


def getLastUserId():
  if db.songs.find().count() is not 0:
    last_id = list(db.songs.find({}).sort("song_id", -1).limit(1))
    return last_id[0]["song_id"]
  else:
    return 0


def uploadInitialSongs(data):
    with open(data) as f:
        d = json.load(f)
        ids = [{"song_id": i} for i in range(1, len(d) + 1)]
        d = list(map(lambda x, y: {**x, **y}, ids, d))
        db.songs.insert(d)
        f.close()




class Index(Resource):

    def get(self):

        data = {
            "version" : "1.0",
            "owner" : "Burc Turkoglu",
            "projectName" : "REST API For Songs DB"
        }

        return jsonify({"response": data})


class Songs(Resource):

    def get(self):
        data = []
        pagination = request.args.get("page") #page value taken as optional parameter


        if pagination:

            """
            Here the page number parameter which is given as an optional parameter 
            and the page size parameter which is 10 by default are used to create proper pagination. 
            """
            page_size = 10
            page_num = int(pagination)
            skips = page_size * (page_num - 1)

            """
            By using skip and limit methods on cursor, collection is divided into blocks/pages.
            
            Afterwards, with "(page_size * page_num - cursor.count()) < page_size" it is checked 
            whether there is enough data to show user in given page number or not. 
            """
            cursor = db.songs.find({}, {"_id": 0, "update_time": 0}).skip(skips).limit(page_size)

            """
            By using cursor.count() method, it is checked that if there is any data returned 
            from cursor.find(...) method. This is used few more times in different part of the code.
            """
            if cursor.count() > 0 and (page_size * page_num - cursor.count()) < page_size:
                for song in cursor:
                    data.append(song)

                return jsonify({"page":page_num, "response": data})

            elif cursor.count() > 0 and (page_size * page_num - cursor.count()) > page_size:
                return jsonify({"response": "Page %d does not exist." % page_num})

            else:
                return jsonify({"response": "There isn't any data to show"})

        else:
            """
            Here the data is viewed all at once without pagination.
            """
            cursor = db.songs.find({}, {"_id": 0, "update_time": 0})

            if cursor.count() > 0:
                for song in cursor:
                    data.append(song)

                return jsonify({"response": data})
            else:
                return jsonify({"response": "There isn't any data to show"})


    def post(self):
        data = request.get_json()


        if not data:
            data = {"response": "File is not valid"}
            return jsonify(data)
        else:
            """Here in addition to ObjectId, manually created song_id is added to the data"""
            # for idx, i in enumerate(data):
            #     cursor = db.songs.find({"$and": [{"title": i["title"]},
            #                                            {"artist": i["artist"]}]})
            #     if cursor.count() > 0:
            #         del data[idx]
            #
            # ids = [{"song_id": i} for i in range(1, len(data) + 1)]
            # data = list(map(lambda x, y: {**x, **y}, ids, data))
            # db.songs.insert(data)

            if type(data) is list:
                for i in data:
                    cursor = db.songs.find({"title": i["title"], "artist": i["artist"]})
                    if cursor.count() > 0:
                        pass
                    else:
                        last_id = getLastUserId()
                        db.songs.insert_one({**{"song_id": last_id+1}, **i})
            if type(data) is dict:
                cursor = db.songs.find({"title": data["title"], "artist": data["artist"]})
                if cursor.count() > 0:
                    pass
                else:
                    last_id = getLastUserId()
                    db.songs.insert_one({**{"song_id": last_id + 1}, **data})

        return redirect(url_for("songs"))


class SongSearch(Resource):
    def get(self, message=None):
        data = []

        if message:

            cursor = db.songs.find({"$or": [{"title": re.compile(message, re.IGNORECASE)},
                                                  {"artist": re.compile(message, re.IGNORECASE)}]},
                                         {"_id": 0, "update_time": 0})
            if cursor.count() > 0:
                for song in cursor:
                    data.append(song)

                return jsonify({"response": data})
            else:
                return jsonify({"response": "Nothing found"})

        else:
            return redirect(url_for("songs"))

class SongsDifficulty(Resource):
    def get(self, level=None):
        data = []



        if level:
            cursor = db.songs.find({"level": level}, {"_id": 0})
            print(cursor.max("difficulty"))
            if cursor.count() > 0:
                for song in cursor:
                    data.append(song["difficulty"])

                return jsonify({"level": level, "response": {"average difficulty": round(sum(data) / len(data), 2)}})
            else:
                return jsonify({"level": level, "response": "There isn't any songs in that level."})
        else:
            cursor = db.songs.find({}, {"_id": 0})

            for song in cursor:
                data.append(song["difficulty"])

            return jsonify({"response": {"average difficulty": round(sum(data) / len(data), 2)}})

class SongsRating(Resource):
    def get(self, song_id=None):
        data = []

        if song_id:
            cursor = db.songratings.find({"song_id":song_id}, {"_id": 0})
            cursor_all_ratings = db.songratings.find({}, {"_id": 0})
            if cursor.count() > 0:
                for song in cursor:
                    data.append(song["rating"])

                return jsonify({"song_id": song_id, "response": {"average rating": round(sum(data) / len(data), 2),
                                                                 "minimum rating": min(data),
                                                                 "maximum rating": max(data)}})
            elif cursor_all_ratings.count() > 0 and not cursor.count() > 0:
                return jsonify({"response": "There is no rating for this song id!"})
            else:
                return jsonify({"response":"There is no song rating list exist yet!"})
        else:
            cursor = db.songratings.find({}, {"_id": 0})
            if cursor.count() > 0:
                for song in cursor:
                    data.append(song)
                return jsonify({"response":data})
            else:
                return jsonify({"response": "There is no song rating list exist yet!"})

    def post(self):
        data = request.get_json()

        if not data:
            return jsonify({"response": "file is not valid"}) #prompted message when empty file is given
        else:
            song_id = data.get('song_id')
            rating = data.get('rating')
            if song_id and rating:
                if not 1 <= rating <= 5:
                    return jsonify({"response": "ratings should be between 1 and 5!"}) #faulty rating entry message
                else:
                    song = db.songs.find({"song_id": song_id}) #checking if song exist in songs collection
                    if song.count() > 0:
                        db.songratings.insert(data) #successfully insert rating of a song to songratings collection
                        return jsonify({"response": "rating is successfully made"}) #success message
                    else:
                        return jsonify({"response": "this song does not exist"}) #entered song_id not found in songs collection message
            else:
                if not song_id and not rating:
                    return jsonify({"response": "both song id and rating are missing"}) #message that returns when both song_id and rating are missing
                elif not song_id and rating:
                    return jsonify({"response": "song id is missing"}) #message that returns when song_id is missing
                else:
                    return jsonify({"response": "rating is missing"}) #message that returns when rating is missing




api = Api(app)
api.add_resource(Index, "/", endpoint="index")
api.add_resource(Songs, "/songs/", endpoint="songs")
api.add_resource(SongsDifficulty, "/songs/avg/difficulty/", "/songs/avg/difficulty/<int:level>", endpoint="level")
api.add_resource(SongSearch, "/songs/search/", "/songs/search/<string:message>", endpoint="message")
# api.add_resource(SongsRating, "/songs/rating/", endpoint="rating")
api.add_resource(SongsRating, "/songs/rating/", "/songs/avg/rating/", "/songs/avg/rating/<int:song_id>", endpoint="avg_rating")


if __name__ == '__main__':
    app.run(host='0.0.0.0')
