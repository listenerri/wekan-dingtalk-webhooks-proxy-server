#!/usr/bin/env python3
# coding = utf-8
# author = listenerri
# maintainer = listenerri

import configs
import wekan_actions_handler
import mongo_db_utils
from flask import Flask, escape, request, abort, Response

app = Flask(__name__)
app.debug = 1
logger = app.logger

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
    logger.info("Accepted a webhook")
    wekan_json_data = request.json
    delivery = wekan_actions_handler.get_delivery(wekan_json_data)
    if delivery is None:
        abort(500)
    print(">>>>>>>>>>>>>>>>>>>>>delivery: ", delivery)
    return ("done")

def init_app():
    configs.setup_logger(logger)
    mongo_db_utils.setup_logger(logger)
    wekan_actions_handler.setup_logger(logger)

    if not configs.reload_server_config():
        exit(255)
    if not configs.reload_account_config():
        exit(255)

init_app()

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8080)
