#!/usr/bin/env python3
# coding = utf-8
# author = listenerri
# maintainer = listenerri

import os
import json
import time
import pymongo
from flask import Flask, escape, request, abort, Response

app = Flask(__name__)
app.debug = 1
logger = app.logger

__Server_Config_File_Path = "config-server.json"
__Account_Config_File_Path = "config-account.json"

__Server_Config = None
__Account_Config = None

__DB_Client = None

def init_db():
    global __DB_Client
    count = 0
    while True:
        try:
            __DB_Client = pymongo.MongoClient(__Server_Config["mongo-db-config"]["connect-uri"], connect=True)
            break
        except Exception as e:
            count += 1
            logger.error("Connect mongo db failed, retry {}".format(count))
            time.sleep(1)
    logger.info("Connect to mongo db successed")

@app.route('/api/wekan/reload-config/server/')
def reload_server_config(init=False):
    global __Server_Config
    if not os.path.isfile(__Server_Config_File_Path):
        logger.error("config file: {} not exists".format(__Server_Config_File_Path))
        exit(255)
    with open(__Server_Config_File_Path, "r") as f:
        try:
            __Server_Config = json.load(f)
        except Exception as e:
            logger.error("config file: {} load failed".format(__Server_Config_File_Path))
            if init:
                exit(255)
            else:
                abort(500)
    init_db()
    return ("done")

@app.route('/api/wekan/reload-config/account/')
def reload_account_config(init=False):
    global __Account_Config
    if not os.path.isfile(__Account_Config_File_Path):
        logger.error("config file: {} not exists".format(__Account_Config_File_Path))
        exit(255)
    with open(__Account_Config_File_Path, "r") as f:
        try:
            __Account_Config = json.load(f)
        except Exception as e:
            logger.error("config file: {} load failed".format(__Account_Config_File_Path))
            if init:
                exit(255)
            else:
                abort(500)
    return ("done")

@app.route('/api/wekan/webhook/', methods=["POST"])
def wekan_webhook():
    logger.info("accepted a webhook")
    for k, v in request.json.items():
        print(k, v)
    return ("done")

def init_app():
    reload_server_config(init=True)
    reload_account_config(init=True)

init_app()

if __name__ == '__main__':
    app.run()
