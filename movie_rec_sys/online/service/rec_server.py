#!/usr/bin/env python
# -*- coding: utf-8 -*-

import time
from flask import Flask, request
from gevent import monkey
from gevent.pywsgi import WSGIServer
from geventwebsocket.handler import WebSocketHandler
import json
import global_movie_conf as global_conf
from movie_rec_sys.online.data_manager.data_manager import data_manager_holder, DataManager



data_manager_holder.load_data(movie_data_path=global_conf.sample_data_dir + "movies.csv",
                              link_data_path=global_conf.sample_data_dir + "links.csv",
                              rating_data_path=global_conf.sample_data_dir + "ratings.csv",
                              movie_emb_path=global_conf.sample_data_dir + "item2vecEmb.csv",
                              user_emb_path=global_conf.sample_data_dir + "userEmb.csv",
                              movie_redis_key="i2vEmb",
                              user_redis_key="uEmb")

monkey.patch_all()

app = Flask(__name__)

app.config.update(
    DEBUG=True
)


def obj2dict():
    pass


@app.route('/get_recommendation/', methods=['GET'])
def get_recommendation():
    # http://192.168.3.28:7878/get_recommendation/?genre=Adventure&size=10&sortby=rating
    genre = request.args.get('genre')
    size = int(request.args.get('size', 10))
    sort = request.args.get('sortby')
    movies = data_manager_holder.get_movies_by_genre(genre=genre, size=size, sort_by=sort)
    return json.dumps(DataManager.obj2dict(movies), ensure_ascii=False)


@app.route('/get_rec_for_you/', methods=['GET'])
def get_rec_for_you():
    time.sleep(1)
    return 'hello test'


if __name__ == "__main__":
    """
       使用flask自带的传递参数threaded与processes，也可以实现异步非阻塞，但是这个原理是
       同时开启多个线程或者多个进程来接受发送的请求，每个线程或者进程还是阻塞式处理任务
       如果想使用threaded或processes参数，必须将debug设置为False才能生效，不然不起作用
       同时Windows下不支持同时开启多进程，所以在win下使用processes无效
    """
    # app.run(host='0.0.0.0', port=10008, debug=False, threaded=True, processes=5)
    http_server = WSGIServer(('192.168.3.28', 7878), app, handler_class=WebSocketHandler)
    http_server.serve_forever()
