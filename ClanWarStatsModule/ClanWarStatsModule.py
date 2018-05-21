#!/usr/local/bin/python3

from .dbHandler import dbHandler
import requests
import json

class ClanWarStatsModule:
  API_COLLECTION_DAY = 'clanWarCollectionDay'
  API_WAR_DAY = 'clanWarWarDay'

  autoUpdate = False

  def __init__(self, dbPath, crAPI_AUTH, clanTag, admin=''):
    self.dbPath = dbPath
    self.dbHandler = dbHandler(dbPath)
    self.crAPI_AUTH = crAPI_AUTH
    self.clanTag = clanTag

    self.admin = admin

  def getDbPath(self):
    return self.dbPath

  def setAutoUpdate(self, autoUpdate):
    self.autoUpdate = autoUpdate

  def updateMemberList(self):
    r = requests.get("https://api.royaleapi.com/clan/{0}".format(self.clanTag), headers={"Authorization" : self.crAPI_AUTH})

    if r.status_code == 200:
      clan_json = r.json()

      members_data = []
      member = {}
      for member in clan_json['members']:
        member[self.dbHandler.DB_MEMBER_TAG] = member['tag']
        member[self.dbHandler.DB_MEMBER_NAME] = member['name']
        members_data.append(member)

        member = {}
      return self.dbHandler.updateMemberList(members_data)
    else:
      return False

  def updateMemberBattleLog(self):
    activeMemberTag = self.dbHandler.getActiveClanMemberTag()
    activeMemberNumber = self.dbHandler.getActiveMemberNumber()
    link = "https://api.royaleapi.com/player/{0}/battles".format(activeMemberTag)
    r = requests.get(link, headers={"Authorization" : self.crAPI_AUTH}, timeout=180)
    if r.status_code == 200:
      battles_json = r.json()

      if activeMemberNumber > 1 :
        for player in battles_json:
          for log in player:
            if log['type'] == self.API_COLLECTION_DAY or log['type'] == self.API_WAR_DAY:
              memberTag = log['team'][0]['tag']
              matchType = self.dbHandler.DB_VALUE_MATCH_COLLECTION_DAY[0] if log['type'] == self.API_COLLECTION_DAY else self.dbHandler.DB_VALUE_MATCH_WAR_DAY[0]
              result = self.dbHandler.DB_VALUE_RESULT_WIN[0] if log['winner'] > 0 else self.dbHandler.DB_VALUE_RESULT_LOSE[0]
              utcTime = log['utcTime']
              self.dbHandler.updateMemberBattleLog(memberTag, matchType, result, utcTime)
    else:
      return False

  def getActiveClanMemberTag(self):
    return self.dbHandler.getActiveClanMemberTag()
