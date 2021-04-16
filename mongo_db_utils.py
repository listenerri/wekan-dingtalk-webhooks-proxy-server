#!/usr/bin/env python3
# coding = utf-8
# author = listenerri
# maintainer = listenerri

import datetime
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

def get_latest_activity():
    result = __DB_Client.wekan.activities.find(
        {}, {"modifiedAt":1}).sort("modifiedAt", pymongo.DESCENDING).limit(1)
    return result

def get_latest_activity_ts():
    result = get_latest_activity()
    ts = datetime.datetime.utcnow() if result is None else result[0]["modifiedAt"]
    return ts

def get_newer_activity(ts):
    result = __DB_Client.wekan.activities.find(
        {"modifiedAt":{"$gt":ts}}).sort("modifiedAt", pymongo.ASCENDING)
    return result

def get_wekan_user_name_by_id(wekan_user_id):
    if wekan_user_id is None:
        return None
    result = __DB_Client.wekan.users.find_one({"_id":wekan_user_id}, {"_id":0, "username":1})
    if result is None:
        return None
    return result.get("username", None)

def get_board_title_by_id(board_id):
    if board_id is None:
        return None
    result = __DB_Client.wekan.boards.find_one({"_id":board_id}, {"_id":0, "title":1})
    if result is None:
        return None
    return result.get("title", None)

def get_list_title_by_id(list_id):
    if list_id is None:
        return None
    result = __DB_Client.wekan.lists.find_one({"_id":list_id}, {"_id":0, "title":1})
    if result is None:
        return None
    return result.get("title", None)

def get_card_title_by_id(card_id):
    if card_id is None:
        return None
    result = __DB_Client.wekan.cards.find_one({"_id":card_id}, {"_id":0, "title":1})
    if result is None:
        return None
    return result.get("title", None)

def get_card_members_by_id(card_id):
    if card_id is None:
        return None
    result = __DB_Client.wekan.cards.find_one({"_id":card_id}, {"_id":0, "members":1})
    if result is None:
        return None
    return result.get("members", None)

def get_card_creator_by_id(card_id):
    if card_id is None:
        return None
    result = __DB_Client.wekan.cards.find_one({"_id":card_id}, {"_id":0, "userId":1})
    if result is None:
        return None
    return result.get("userId", None)
