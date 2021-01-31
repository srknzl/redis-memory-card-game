from flask import Flask, request
import logging as log
import redis
import random
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

r = redis.Redis(host='redis', port=6379, db=0)


@app.route('/')
def home():
    return {"service_status_is": "OK"}


@app.route('/init', methods=['POST'])
def init():
    if request.json is None:
        return {"msg": "json pls"}, 422
    if "size" not in request.json or type(request.json["size"]) != int or request.json["size"] <= 0 \
            or request.json["size"] % 2 == 1:
        return {"msg": "give valid size param in json"}

    try:
        size = request.json["size"]
        game_number = r.incr("game_number")
        # If size is 4 init is done as follows (keys)
        # 1 2 3 4
        # 5 6 7 8
        # 9 10 11 12
        # 13 14 15 16
        # Values are given randomly to these keys. The value set includes 1,1, 2,2 ... 8,8.
        # So there are 8 pairs to match in this example
        value_list = []
        for i in range(1, (size * size // 2) + 1):
            value_list.append(i)
            value_list.append(i)
        log.warning(value_list)
        random.shuffle(value_list)

        for i in range(1, size * size + 1):  # 1 to size
            r.set(f"{game_number}-{i}", value_list[i - 1])
    except Exception as e:
        log.exception("err init ", exc_info=e)
        return {"msg": f"err: {e}"}, 500

    return {"msg": "OK", "game_number": game_number}, 200


@app.route('/get-card', methods=['POST'])
def get_card():
    if request.json is None:
        return {"msg": "json pls"}, 422
    if "index" not in request.json or type(request.json["index"]) != int:
        return {"msg": "give index param in json"}
    if "game_number" not in request.json or type(request.json["game_number"]) != int:
        return {"msg": "give game_number param in json"}

    value = r.get(f"{request.json['game_number']}-{request.json['index']}")
    if value is None:
        return {"msg": "key does not exist"}, 400
    else:
        try:
            return {"msg": int(value.decode())}, 200
        except Exception as e:
            log.exception("get card value error", exc_info=e)
            return {"msg": "value error"}, 500


@app.route('/submit', methods=['POST'])
def submit():
    if request.json is None:
        return {"msg": "json pls"}, 422
    if "index1" not in request.json or type(request.json["index1"]) != int or "index2" not in request.json or type(
            request.json["index2"]) != int:
        return {"msg": "give index1 and index2 param in json"}

    if "game_number" not in request.json or type(request.json["game_number"]) != int:
        return {"msg": "give game_number param in json"}

    value1 = r.get(f"{request.json['game_number']}-{request.json['index1']}")
    value2 = r.get(f"{request.json['game_number']}-{request.json['index2']}")
    log.warning(f"value1: {value1} value2: {value2}")
    if value1 is not None and value2 is not None:
        if value1 == value2:
            r.delete(f"{request.json['game_number']}-{request.json['index1']}")
            r.delete(f"{request.json['game_number']}-{request.json['index2']}")
            return {}, 200
        else:
            return {}, 400
    else:
        return {"msg": "one of keys does not exists"}, 400


@app.route('/get-board', methods=['GET'])
def get_board():
    game_number = request.args.get("game_number")
    if game_number is None:
        return {"keys": []}, 400
    keys = r.keys(f"{game_number}-*")
    keys_returned = []
    for key in keys:
        try:
            key_value = key.decode()
            splitted = key_value.split("-")
            keys_returned.append(int(splitted[-1]))
        except Exception as e:
            log.exception("get-board value error", exc_info=e)

    return {"keys": keys_returned}, 200


@app.errorhandler(500)
def internal_error(error):
    return {"err": error}, 500


@app.errorhandler(404)
def not_found(error):
    return {"404_not_found": error}, 404
