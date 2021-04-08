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
    server_config = configs.server_config()
    count = 0
    while True:
        try:
            __DB_Client = pymongo.MongoClient(server_config["mongo-db-config"]["connect-uri"], connect=True)
            break
        except Exception as e:
            count += 1
            __logger.error("Connect mongo db failed, retry {}".format(count))
            time.sleep(1)
    __logger.info("Connect to mongo db successed")

def mongo_db_client():
    return __DB_Client