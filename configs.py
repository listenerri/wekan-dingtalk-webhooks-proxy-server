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

__logger = None

def setup_logger(logger):
    global __logger
    __logger = logger

def reload_server_config():
    global __Server_Config
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
    return True

def server_config():
    return __Server_Config

def account_config():
    return __Account_Config
