# Redis Card Game
* Card game for memory practice built with redis!
* I built this with redis because "get", "set" and "delete" operations of redis reminded me of this game
* This branch includes changes for concurrent game playing. I did it when I first deployed this project to a website. 
## Technologies
* Redis is used for storing values under cards. The data is not stored in browser memory. 
* Vue.js for frontend
* Flask for api

## Running

* Install docker and docker-compose
* Run `docker-compose up -d` in root folder.
