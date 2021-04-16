#!/usr/bin/env python3
# coding = utf-8
# author = listenerri
# maintainer = listenerri

import json
import time
import configs
import queue
import threading
import mongo_db_utils

from urllib import request

__logger = None
__activity_queue = queue.Queue()
__worker_thread = None

__Action_2_Handler = {}
__Action_2_Delivery_Template = {
    "addAttachment": "{user} 添加了附件\n看板：{board}\n列表：{list}\n任务：{card}",
    "deleteAttachment": "{user} 移除了附件\n看板：{board}\n列表：{list}\n任务：{card}",
    "addSubtask": "{user} 添加了子任务\n看板：{board}\n列表：{list}\n任务：{card}",
    "addedLabel": "{user} 添加了标签\n看板：{board}\n列表：{list}\n任务：{card}",
    "removedLabel": "{user} 移除了标签\n看板：{board}\n列表：{list}\n任务：{card}",
    "addChecklist": "{user} 添加了待办清单\n看板：{board}\n列表：{list}\n任务：{card}",
    "removeChecklist": "{user} 移除了待办清单\n看板：{board}\n列表：{list}\n任务：{card}",
    "addChecklistItem": "{user} 添加了待办清单项\n看板：{board}\n列表：{list}\n任务：{card}",
    "checkedItem": "{user} 完成了待办清单项\n看板：{board}\n列表：{list}\n任务：{card}",
    "uncheckedItem": "{user} 修改/复原了待办清单项\n看板：{board}\n列表：{list}\n任务：{card}",
    "removedChecklistItem": "{user} 移除了待办清单项\n看板：{board}\n列表：{list}\n任务：{card}",
    "completeChecklist": "{user} 完成了清单\n看板：{board}\n列表：{list}\n任务：{card}",
    "uncompleteChecklist": "{user} 复原了清单\n看板：{board}\n列表：{list}\n任务：{card}",
    "addComment": "{user} 评论了任务\n看板：{board}\n列表：{list}\n任务：{card}",
    "editComment": "{user} 编辑了任务评论\n看板：{board}\n列表：{list}\n任务：{card}",
    "deleteComment": "{user} 删除任务评论\n看板：{board}\n列表：{list}\n任务：{card}",
    "createBoard": "{user} 创建了看板\n看板：{board}",
    "archivedBoard": "{user} 归档了看板\n看板：{board}",
    "removeBoard": "{user} 删除了看板\n看板：{board}",
    "createSwimlane": "{user} 创建了泳道\n看板：{board}",
    "archivedSwimlane": "{user} 归档了泳道\n看板：{board}\n列表：{list}\n任务：{card}",
    "createList": "{user} 创建了列表\n看板：{board}\n列表：{list}",
    "archivedList": "{user} 归档了列表\n看板：{board}\n列表：{list}\n任务：{card}",
    "removeList": "{user} 删除了列表\n看板：{board}\n列表：{list}\n任务：{card}",
    "createCard": "{user} 创建了任务\n看板：{board}\n列表：{list}\n任务：{card}",
    "archivedCard": "{user} 归档了任务\n看板：{board}\n列表：{list}\n任务：{card}",
    "restoredCard": "{user} 恢复了任务\n看板：{board}\n列表：{list}\n任务：{card}",
    "createCustomField": "{user} 创建了自定义字段\n看板：{board}\n列表：{list}\n任务：{card}",
    "deleteCustomField": "{user} 删除了自定义字段\n看板：{board}\n列表：{list}\n任务：{card}",
    "setCustomField": "{user} 修改了自定义字段\n看板：{board}\n列表：{list}\n任务：{card}",
    "addBoardMember": "{user} 添加了看板成员\n看板：{board}",
    "removeBoardMember": "{user} 移除了看板成员\n看板：{board}",
    "joinMember": "{user} 增加了任务成员\n看板：{board}\n列表：{list}\n任务：{card}",
    "unjoinMember": "{user} 移除了任务成员\n看板：{board}\n列表：{list}\n任务：{card}",
    "joinAssignee": "{user} 增加了任务被指派成员\n看板：{board}\n列表：{list}\n任务：{card}",
    "unjoinAssignee": "{user} 移除了任务被指派成员\n看板：{board}\n列表：{list}\n任务：{card}",
    "moveCard": "{user} 移动了任务\n看板：{board}\n列表：{list}\n任务：{card}",
    "moveCardBoard": "{user} 移动了任务\n看板：{board}\n列表：{list}\n任务：{card}",
    "a-dueAt": "{user} 修改了任务到期时间\n看板：{board}\n列表：{list}\n任务：{card}",
    "a-endAt": "{user} 修改了任务结束时间\n看板：{board}\n列表：{list}\n任务：{card}",
    "a-startAt": "{user} 修改了任务开始时间\n看板：{board}\n列表：{list}\n任务：{card}",
    "a-receivedAt": "{user} 修改了任务接收时间\n看板：{board}\n列表：{list}\n任务：{card}",
    "newDue": "{user} 任务到期提醒\n看板：{board}\n列表：{list}\n任务：{card}",
    "withDue": "{user} 任务到期提醒\n看板：{board}\n列表：{list}\n任务：{card}",
    "almostdue": "{user} 任务到期提醒\n看板：{board}\n列表：{list}\n任务：{card}",
    "pastdue": "{user} 任务到期提醒\n看板：{board}\n列表：{list}\n任务：{card}",
    "duenow": "{user} 任务到期提醒\n看板：{board}\n列表：{list}\n任务：{card}"
}

def init_handler(logger):
    global __logger
    global __worker_thread

    __logger = logger
    __worker_thread = threading.Thread(target=__handle_activity_worker, daemon=True)
    __worker_thread.start()

    __Action_2_Handler.clear()
    for action in __Action_2_Delivery_Template.keys():
        __Action_2_Handler[action] = __common_handler

def __build_dingtalk_text_webhook_data(delivery, at_mobiles):
    if delivery is None:
        return None
    data_temp = {
            "msgtype": "text",
            "text": {
                "content": None
            },
            "at": {
                "isAtAll": False,
                "atMobiles": None
            }
        }
    delivery = "{}{}{}".format(configs.get_common_delivery_header(), delivery, configs.get_common_delivery_tail())
    at_content_part = ""
    for tel in at_mobiles:
        at_content_part += "@{} ".format(tel)
    if len(at_content_part) != 0:
        delivery += "\n{}".format(at_content_part)
    data_temp["text"]["content"] = delivery
    data_temp["at"]["atMobiles"] = list(at_mobiles)
    data = json.dumps(data_temp, ensure_ascii=False)
    return data

def __send_special_webhook(msg):
    if len(configs.get_admin_accounts()) == 0:
        return
    boards_2_dingtalk_webhook = configs.get_boards_2_dingtalk_webhook()
    if boards_2_dingtalk_webhook is None or "*" not in boards_2_dingtalk_webhook:
        __logger.warn("Not found * item in boards-2-dingtalk-webhook config, can not send special webhook")
        return
    phones = set()
    for _, user_info in configs.get_admin_accounts().items():
        tel = user_info["phone-number"]
        if len(tel) != 0:
            continue
        phones.add(tel)
    if len(phones) == 0:
        return
    delivery = __build_dingtalk_text_webhook_data(msg, phones)
    webhook = boards_2_dingtalk_webhook["*"]
    __send_dingtalk_webhook(delivery, webhook)

def __send_dingtalk_webhook(delivery, webhook):
    __logger.debug("##################### send webhook start")
    __logger.debug(delivery)
    __logger.debug(webhook)
    req = request.Request(webhook, data=bytes(delivery, encoding="UTF-8"))
    req.add_header("Content-Type", "application/json")
    res = request.urlopen(req)
    __logger.debug((res.status, res.reason, res.read()))
    __logger.debug("##################### send webhook end\n\n\n")

def __common_handler(activity_data):
    action = activity_data["activityType"]
    if action not in __Action_2_Delivery_Template:
        msg = "Not found the delivery template for action: {}".format(activity_data)
        __logger.error(msg)
        __send_special_webhook(msg)
        return None
    delivery_temp = __Action_2_Delivery_Template[action]

    wekan_user_id = activity_data.get("userId", None)
    dingtalk_user_name = configs.get_dingtalk_user_name_by_wekan_user_id(wekan_user_id)

    board_id = activity_data.get("boardId", None)
    board_title = mongo_db_utils.get_board_title_by_id(board_id)

    list_id = activity_data.get("listId", None)
    list_title = mongo_db_utils.get_list_title_by_id(list_id)

    card_id = activity_data.get("cardId", None)
    card_title = mongo_db_utils.get_card_title_by_id(card_id)

    delivery = delivery_temp.format(user=dingtalk_user_name, board=board_title, list=list_title, card=card_title)

    at_mobiles = set()
    card_members = mongo_db_utils.get_card_members_by_id(card_id)
    if card_members is not None:
        for user_id in card_members:
            phone = configs.get_dingtalk_phone_number_by_wekan_user_id(user_id)
            if phone is None:
                continue
            at_mobiles.add(phone)
    card_creator_id = mongo_db_utils.get_card_creator_by_id(card_id)
    if card_creator_id is not None:
        phone = configs.get_dingtalk_phone_number_by_wekan_user_id(card_creator_id)
        if phone is not None:
            at_mobiles.add(phone)
    delivery = __build_dingtalk_text_webhook_data(delivery, at_mobiles)
    return delivery

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
        __send_special_webhook(msg)
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
            __send_special_webhook(msg)
            continue

        only_handle_actions = configs.get_only_handle_actions()
        if only_handle_actions is not None and len(only_handle_actions) > 0 and action not in only_handle_actions:
            __logger.info("Ignore action: {} because it not in only handle actions list".format(action))
            continue

        handler_func = __Action_2_Handler[action]
        delivery = handler_func(activity_data)
        if delivery is None:
            continue
        webhooks = __get_webhooks_url(activity_data)
        if len(webhooks) == 0:
            continue
        for webhook in webhooks:
            __send_dingtalk_webhook(delivery, webhook)
        continue

def handle_activity(activity_data):
    __activity_queue.put(activity_data)
