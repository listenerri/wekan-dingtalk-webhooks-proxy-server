#!/usr/bin/env python3
# coding = utf-8
# author = listenerri
# maintainer = listenerri

import os
import json
import mongo_db_utils

__Server_Config_File_Path = "config/config-server.json"
__Account_Config_File_Path = "config/config-account.json"

__Server_Config = None
__Account_Config = None
__Admin_Accounts = {}

__logger = None

def setup_logger(logger):
    global __logger
    __logger = logger

def reload_server_config():
    global __Server_Config
    global __Admin_Accounts
    if not os.path.isfile(__Server_Config_File_Path):
        __logger.error("Config file: {} not exists".format(__Server_Config_File_Path))
        return False
    with open(__Server_Config_File_Path, "r") as f:
        try:
            __Server_Config = json.load(f)
        except Exception as e:
            __logger.error("Config file: {} load failed".format(__Server_Config_File_Path))
            return False
    mongo_db_utils.init_db()
    return True

def reload_account_config():
    global __Account_Config
    if not os.path.isfile(__Account_Config_File_Path):
        __logger.error("Config file: {} not exists".format(__Account_Config_File_Path))
        return False
    with open(__Account_Config_File_Path, "r") as f:
        try:
            __Account_Config = json.load(f)
        except Exception as e:
            __logger.error("Config file: {} load failed".format(__Account_Config_File_Path))
            return False
    for wekan_user, user_info in __Account_Config.items():
        if "admin" in user_info and user_info["admin"]:
            __Admin_Accounts[wekan_user] = user_info
    return True

def get_server_config():
    return __Server_Config

def get_mongo_db_config():
    return __Server_Config.get("mongo-db-config", None)

def get_common_delivery_header():
    return __Server_Config.get("common-delivery-header", "")

def get_common_delivery_tail():
    return __Server_Config.get("common-delivery-tail", "")

def get_boards_2_dingtalk_webhook():
    return __Server_Config.get("boards-2-dingtalk-webhook", None)

def get_only_handle_actions():
    return __Server_Config.get("only-handle-actions", None)

def get_account_config():
    return __Account_Config

def get_admin_accounts():
    return __Admin_Accounts
