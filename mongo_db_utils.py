#!/usr/bin/env python3
# coding = utf-8
# author = listenerri
# maintainer = listenerri

import pymongo
import time
import configs

__DB_Client = None

__logger = None

def setup_logger(logger):
    global __logger
    __logger = logger

def init_db():
    global __DB_Client
    count = 0
    while True:
        try:
            __DB_Client = pymongo.MongoClient(configs.get_mongo_db_config()["connect-uri"], connect=True)
            break
        except Exception as e:
            count += 1
            __logger.error("Connect mongo db failed, retry {}".format(count))
            time.sleep(1)
    __logger.info("Connect to mongo db successed")

def get_mongo_db_client():
    return __DB_Client

def get_wekan_user_name_by_id(wekan_user_id):
    if wekan_user_id is None:
        return None
    result = __DB_Client.wekan.users.find_one({"_id":wekan_user_id}, {"_id":0, "username":1})
    if result is None:
        return None
    return result.get("username", None)

def get_board_title_by_id(board_id):
    board_title = None
    if board_id is not None:
        result = __DB_Client.wekan.boards.find_one({"_id":board_id}, {"_id":0, "title":1})
        if result is not None:
            board_title = result.get("title", None)
