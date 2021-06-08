#!/usr/bin/env python3
# coding = utf-8
# author = listenerri
# maintainer = listenerri

import json

import configs

from urllib import request

def send_special_webhook(msg, logger):
    if len(configs.get_admin_accounts()) == 0:
        return
    boards_2_dingtalk_webhook = configs.get_boards_2_dingtalk_webhook()
    if boards_2_dingtalk_webhook is None or "*" not in boards_2_dingtalk_webhook:
        logger.warn("Not found * item in boards-2-dingtalk-webhook config, can not send special webhook")
        return
    phones = set()
    for _, user_info in configs.get_admin_accounts().items():
        tel = user_info["phone-number"]
        if len(tel) != 0:
            continue
        phones.add(tel)
    if len(phones) == 0:
        return
    delivery = build_dingtalk_text_webhook_data(msg, phones)
    webhook = boards_2_dingtalk_webhook["*"]
    send_dingtalk_webhook(delivery, webhook, logger)

def send_dingtalk_webhook(delivery, webhook, logger):
    logger.debug("##################### send webhook start")
    logger.debug(delivery)
    logger.debug(webhook)
    req = request.Request(webhook, data=bytes(delivery, encoding="UTF-8"))
    req.add_header("Content-Type", "application/json")
    res = request.urlopen(req)
    logger.debug((res.status, res.reason, res.read()))
    logger.debug("##################### send webhook end\n\n\n")

def build_dingtalk_text_webhook_data(delivery, at_mobiles):
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
