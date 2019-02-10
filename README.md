# REST API for Songs DB with Flask and MongoDB

This service is written for GET or POST informations on a song database which have features like,
  * song_id
  * artist
  * title
  * difficulty
  * level
  * released
 
Methods which can be used in this REST API are,
  1. **_GET_** _/songs_
     * Getting all the songs as a list in the database with the option of pagination (e.g. /songs/?page=1).
  2. **_POST_** _/songs_
     * Posting the song data to songs collection in the database. Song with same artist and title can only be adding to the collection once.
  3. **_GET_** _/songs/search/<string:message>_
     * With a parameter, search can be done throughout the whole data by looking at title and artist features with given message parameter. 
  4. **_GET_** _/songs/avg/difficulty/<int:level>_
     * Here by giving level parameter, songs with that level are grouped and average difficulty value is calculated and returned as response. If any level parameter is given in this GET method, then average difficulty of all the songs is calculated.
  5. **_POST_** _/songs/rating/_
     * In this method, any song in the songs collection is rated by passing song_id and rating parameters to this method. Rating must be done by giving value between 1 and 5, unless it gives error.
  6. **_GET_** _/songs/avg/rating/<int:song_id>_
     * By passing a song id to this method the minimum, maximum and average rating values of that song id are returned as a response.

## Installation

#### 1 - Installation with _Docker_

    git clone https://github.com/vurbag/songs-db-api.git
    cd songs-db-api
    docker-compose build
    docker-compose up

This is the easy method to start using the API.

It only requires to install Docker and git,

_Docker_: https://docs.docker.com/install/
_git_: https://git-scm.com/downloads

After they are installed, follow these steps,

1. Open CMD/Terminal
2. Go to or create the directory which you want to download the code
3. Run git clone to download this repository and then run "cd songs-db-api" to go to the main directory of programme

    "git clone https://github.com/vurbag/songs-db-api.git"
    
    "cd songs-db-api"
    
4. Run "docker-compose build", which set python, mongodb and all the requirements for this project at once
5. And then run "docker-compose up" which starts running flask server

After it starts, you can go to your web browser and type "http://localhost:5000", you should see the following response,
  
  ```json
  {
    "response": {
        "owner": "Burc Turkoglu",
        "projectName": "REST API For Songs DB",
        "version": "1.0"
    }
  }
  ```
  
#### 2 - Installation from scratch

With this method you will be able to install everything from scratch.


