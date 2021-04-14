#!/usr/bin/env python3
# coding = utf-8
# author = listenerri
# maintainer = listenerri

import datetime
import pymongo
import configs
import wekan_webhooks_handler
import mongo_db_utils
from flask import Flask, escape, request, abort, Response

app = Flask(__name__)
app.debug = 1
logger = app.logger

__latest_activity_ts = None

@app.route('/api/wekan/reload-config/server/')
def reload_server_config():
    if not configs.reload_server_config():
        abort(500)
    return ("done")

@app.route('/api/wekan/reload-config/account/')
def reload_account_config():
    if not configs.reload_account_config():
        abort(500)
    return ("done")

@app.route('/api/wekan/webhook/', methods=["POST"])
def wekan_webhook():
    global __latest_activity_ts
    logger.info("Accepted a webhook")
    result = mongo_db_utils.get_mongo_db_client().wekan.activities.find(
        {"modifiedAt":{"$gt":__latest_activity_ts}}).sort("modifiedAt", pymongo.ASCENDING)
    for row in result:
        print("##################### activity: ", row)
        __latest_activity_ts = row["modifiedAt"]
        wekan_webhooks_handler.handle_activity(row)
    return ("done")

def init_app():
    global __latest_activity_ts
    configs.setup_logger(logger)
    mongo_db_utils.setup_logger(logger)
    wekan_webhooks_handler.init_handler(logger)

    if not configs.reload_server_config():
        exit(255)
    if not configs.reload_account_config():
        exit(255)

    # init local ts flag
    result = mongo_db_utils.get_mongo_db_client().wekan.activities.find(
        {}, {"modifiedAt":1}).sort("modifiedAt", pymongo.DESCENDING).limit(1)
    for row in result:
        __latest_activity_ts = row["modifiedAt"]
    if __latest_activity_ts is None:
        __latest_activity_ts = datetime.datetime.utcnow()

init_app()

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8080)
