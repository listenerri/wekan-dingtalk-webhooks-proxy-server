#!/usr/bin/env python3
# coding = utf-8
# author = listenerri
# maintainer = listenerri

import configs
import wekan_webhooks_handler

from flask import Flask, escape, request, abort, Response

from utils import mongo_db_utils

app = Flask(__name__)
app.debug = True
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
    result = mongo_db_utils.get_newer_activity(__latest_activity_ts)
    if result is None:
        logger.error("Not found newer activity")
    else:
        for row in result:
            logger.debug("##################### activity content start")
            for k, v in row.items():
                logger.debug("{} {} {}".format(k, ":", v))
            logger.debug("##################### activity content end")
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
    __latest_activity_ts = mongo_db_utils.get_latest_activity_ts()

init_app()

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8080)
