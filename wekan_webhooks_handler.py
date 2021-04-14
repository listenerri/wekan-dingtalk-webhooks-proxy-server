#!/usr/bin/env python3
# coding = utf-8
# author = listenerri
# maintainer = listenerri

import configs
import queue
import threading
import mongo_db_utils

__logger = None
__delivery_queue = queue.Queue()
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
    __logger = logger

    __worker_thread = threading.Thread(target=__send_dingtalk_webhook_worker, daemon=True)
    __worker_thread.start()

    __Action_2_Handler.clear()
    for action in __Action_2_Delivery_Template.keys():
        __Action_2_Handler[action] = __common_handler

def __build_dingtalk_text_webhook_data(delivery, atMobiles):
    data_temp = """
        {
            "msgtype": "text",
            "text": {
                "content": "{}"
            },
            "at": {
                "isAtAll": false,
                "atMobiles": [{}]
            }
        }
        """
    delivery = "{}{}{}".format(configs.get_common_delivery_header(), delivery, configs.get_common_delivery_tail())
    at_content_part = ""
    for tel in atMobiles:
        at_content_part += "@{} ".format(tel)
    if len(at_content_part) != 0:
        delivery += "\n{}".format(at_content_part)
    atMobiles_str = ""
    if atMobiles is not None and len(atMobiles) > 0:
        atMobiles_str = ",".join(list(atMobiles))
    data = data_temp.format(delivery, atMobiles_str)
    return data

def __send_special_webhook(msg):
    if len(configs.get_admin_accounts()) == 0:
        return
    if configs.get_boards_2_dingtalk_webhook() is None:
        return
    boards_2_dingtalk_webhook = configs.get_boards_2_dingtalk_webhook()
    if boards_2_dingtalk_webhook is None or "*" not in boards_2_dingtalk_webhook:
        __logger.warn("Not found * item in boards-2-dingtalk-webhook config, can not send special webhook")
        return
    tels = set()
    for _, user_info in configs.get_admin_accounts().items():
        tel = user_info["phone-number"]
        if len(tel) != 0:
            continue
        tels.add(tel)
    if len(tels) == 0:
        return
    delivery = __build_dingtalk_text_webhook_data(msg, tels)
    webhook = boards_2_dingtalk_webhook["*"]
    __queue_tasks(delivery, webhook)

def __queue_tasks(delivery, webhook):
    data = (delivery, webhook)
    __delivery_queue.put(data)

def __send_dingtalk_webhook_worker():
    while True:
        delivery, webhook = __delivery_queue.get(block=True)
        # TODO(ri): send webhook
        print("!!!!!!!!!!!!!!!!!!!!!!!!new task to do: ", delivery)
        print("!!!!!!!!!!!!!!!!!!!!!!!!new task to do: ", webhook)

def __get_dingtalk_user_info(wekan_user_name):
    if wekan_user_name is None:
        return None
    pass

def __get_user_nam(user_id):
    db_client = mongo_db_utils.get_mongo_db_client()
    if user_id is None:
        return None
    result = db_client.wekan.users.find_one({"_id":user_id}, {"_id":0, "username":1})
    if result is None:
        return None
    user_name = result.get("username", None)
    if user_name is None:
        return None
    dingtalk_userinfo = configs.get_account_config().get(user_name, None)

def __common_handler(wekan_json_data):
    action = wekan_json_data["activityType"]
    if action not in __Action_2_Delivery_Template:
        msg = "Not found the delivery template for action: {}".format(wekan_json_data)
        __logger.error(msg)
        __send_special_webhook(msg)
        return None
    delivery_temp = __Action_2_Delivery_Template[action]
    db_client = mongo_db_utils.get_mongo_db_client()

    user_id = wekan_json_data.get("userId", None)
    user_name = ""
    if user_id is not None:
        result = db_client.wekan.users.find_one({"_id":user_id}, {"_id":0, "username":1})
        if result is not None:
            user_name = result.get("username", "")
            dingtalk_userinfo = configs.get_account_config().get(user_name, user_name)

    board_id = wekan_json_data.get("boardId", None)
    board_title = None
    if board_id is not None:
        result = db_client.wekan.boards.find_one({"_id":board_id}, {"_id":0, "title":1})
        if result is not None:
            board_title = result.get("title", None)

    list_id = wekan_json_data.get("listId", None)
    list_title = None
    if list_id is not None:
        result = db_client.wekan.lists.find_one({"_id":list_id}, {"_id":0, "title":1})
        if result is not None:
            list_title = result.get("title", None)

    card_id = wekan_json_data.get("cardId", None)
    card_title = None
    card_members = None
    if card_id is not None:
        result = db_client.wekan.cards.find_one({"_id":card_id}, {"_id":0, "title":1, "members":1})
        if result is not None:
            card_title = result.get("title", None)
            if card_title is not None:
                card_title = card_title.replace("\n", " ")
                if len(card_title) > 60:
                    card_title = card_title[0:60] + "..."
            card_members = result.get("members", None)
    delivery = delivery_temp.format(user=user_name, board=board_title, list=list_title, card=card_title)
    # __build_dingtalk_text_webhook_data(delivery, )
    return delivery

def __get_webhooks(wekan_json_data):
    webhooks = []
    boards_2_dingtalk_webhook = configs.get_boards_2_dingtalk_webhook()
    if boards_2_dingtalk_webhook is None:
        return webhooks
    if "*" in boards_2_dingtalk_webhook:
        webhooks.append(boards_2_dingtalk_webhook["*"])
    board_id = wekan_json_data.get("boardId", None)
    if board_id is not None:
        db_client = mongo_db_utils.get_mongo_db_client()
        result = db_client.wekan.boards.find_one({"_id":board_id}, {"title":1})
        board_name = result.get("title", None)
        if board_name in boards_2_dingtalk_webhook:
            webhooks.append(boards_2_dingtalk_webhook[board_name])
    if len(webhooks) == 0:
        msg = "Not found the webhook for request: {}".format(wekan_json_data)
        __logger.error(msg)
        __send_special_webhook(msg)
    return webhooks

def handle_activity(activity_json_data):
    action = activity_json_data["activityType"]
    if action not in __Action_2_Handler:
        msg = "Not found the handler for action: {}".format(action)
        __logger.error(msg)
        __send_special_webhook(msg)
        return False

    only_handle_actions = configs.get_only_handle_actions()
    if only_handle_actions is not None and len(only_handle_actions) > 0 and action not in only_handle_actions:
        __logger.info("Ignore action: {} because it not in only handle actions list".format(action))
        return True

    handler_func = __Action_2_Handler[action]
    delivery = handler_func(activity_json_data)
    if delivery is None:
        return False
    webhooks = __get_webhooks(activity_json_data)
    if len(webhooks) == 0:
        return False
    for webhook in webhooks:
        __queue_tasks(delivery, webhook)
    return True
