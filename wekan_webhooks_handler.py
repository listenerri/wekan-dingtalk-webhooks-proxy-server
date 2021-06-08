#!/usr/bin/env python3
# coding = utf-8
# author = listenerri
# maintainer = listenerri

import time
import queue
import threading

import delivery_templates
import configs

from utils import mongo_db_utils
from utils import dingtalk_webhook_utils
from handlers import common_handler

__logger = None
__activity_queue = queue.Queue()
__worker_thread = None

__Action_2_Handler = {}

def init_handler(logger):
    global __logger
    global __worker_thread

    __logger = logger
    __worker_thread = threading.Thread(target=__handle_activity_worker, daemon=True)
    __worker_thread.start()

    __Action_2_Handler.clear()
    for action in delivery_templates.Action_2_Delivery_Template.keys():
        __Action_2_Handler[action] = common_handler.common_handler

def __get_webhooks_url(activity_data):
    webhooks = []
    boards_2_dingtalk_webhook = configs.get_boards_2_dingtalk_webhook()
    if boards_2_dingtalk_webhook is None:
        return webhooks
    if "*" in boards_2_dingtalk_webhook:
        webhooks.append(boards_2_dingtalk_webhook["*"])
    board_id = activity_data.get("boardId", None)
    board_name = mongo_db_utils.get_board_title_by_id(board_id)
    if board_name in boards_2_dingtalk_webhook:
        webhooks.append(boards_2_dingtalk_webhook[board_name])
    if len(webhooks) == 0:
        msg = "Not found the webhook for request: {}".format(activity_data)
        __logger.error(msg)
        dingtalk_webhook_utils.send_special_webhook(msg, __logger)
    return webhooks

def __handle_activity_worker():
    while True:
        activity_data = __activity_queue.get(block=True)
        # The data in the database does not seem to have been modified when the Kanban sends webhooks,
        # here is a delayed processing
        time.sleep(2)
        action = activity_data["activityType"]
        if action not in __Action_2_Handler:
            msg = "Not found the handler for action: {}".format(action)
            __logger.error(msg)
            dingtalk_webhook_utils.send_special_webhook(msg, __logger)
            continue

        only_handle_actions = configs.get_only_handle_actions()
        if only_handle_actions is not None and len(only_handle_actions) > 0 and action not in only_handle_actions:
            __logger.info("Ignore action: {} because it not in only handle actions list".format(action))
            continue

        handler_func = __Action_2_Handler[action]
        delivery = handler_func(activity_data, __logger)
        if delivery is None:
            continue
        webhooks = __get_webhooks_url(activity_data)
        if len(webhooks) == 0:
            continue
        for webhook in webhooks:
            dingtalk_webhook_utils.send_dingtalk_webhook(delivery, webhook, __logger)
        continue

def handle_activity(activity_data):
    __activity_queue.put(activity_data)
