#!/usr/bin/env python3
# coding = utf-8
# author = listenerri
# maintainer = listenerri

import configs
import delivery_templates

from utils import mongo_db_utils
from utils import dingtalk_webhook_utils

def comment_add_edit_handler(activity_data, logger):
    action = activity_data["activityType"]
    if action not in delivery_templates.Action_2_Delivery_Template:
        msg = "Not found the delivery template for action: {}".format(activity_data)
        logger.error(msg)
        dingtalk_webhook_utils.send_special_webhook(msg, logger)
        return None
    delivery_temp = delivery_templates.Action_2_Delivery_Template[action]

    wekan_user_id = activity_data.get("userId", None)
    dingtalk_user_name = configs.get_dingtalk_user_name_by_wekan_user_id(wekan_user_id)

    board_id = activity_data.get("boardId", None)
    board_title = mongo_db_utils.get_board_title_by_id(board_id)

    list_id = activity_data.get("listId", None)
    list_title = mongo_db_utils.get_list_title_by_id(list_id)

    card_id = activity_data.get("cardId", None)
    card_title = mongo_db_utils.get_card_title_by_id(card_id)

    comment_id = activity_data.get("commentId", None)
    comment_text = mongo_db_utils.get_comment_by_id(comment_id)
    if comment_text is not None and len(comment_text) > 200:
        comment_text = comment_text[0:200] + "...（内容过长已省略）"

    delivery = delivery_temp.format(
        user=dingtalk_user_name, board=board_title, list=list_title, card=card_title, comment=comment_text)

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
    delivery = dingtalk_webhook_utils.build_dingtalk_text_webhook_data(delivery, at_mobiles)
    return delivery
