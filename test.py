#!/usr/local/bin/python3

import configparser
import os
import pathlib
import time

from datetime import datetime, timedelta

from ClanWarStatsModule.ClanWarStatsModule import ClanWarStatsModule


def readConfigFile():
  config = configparser.ConfigParser()
  config.read('config.ini')

  royale_api_auth = config['DEFAULT']['ROYALE_API_AUTH']
  db_path = os.path.join(config['DEFAULT']['DB_PATH'], config['DEFAULT']['DB_NAME'])
  clan_tag = config['DEFAULT']['CLAN_TAG']

  return (royale_api_auth, db_path, clan_tag)

def updateSqlite3():
  (royale_api_auth, db_path, clan_tag) = readConfigFile()
  cwsm = ClanWarStatsModule(db_path, royale_api_auth, clan_tag)
  print (cwsm.dbHandler.readBattle(1, 1526916957))

if __name__ == '__main__':
  updateSqlite3()
