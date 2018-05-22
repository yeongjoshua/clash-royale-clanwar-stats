#!/usr/local/bin/python3

import sqlite3

class dbHandler:

  DB_TABLE_MEMBER = 'members'
  DB_MEMBER_ID = 'id'
  DB_MEMBER_TAG = 'tag'
  DB_MEMBER_NAME = 'name'
  DB_MEMBER_KEY_STATUS = 'keyStatus'

  DB_TABLE_BATTLES = 'battles'
  DB_BATTLES_ID = 'id'
  DB_BATTLES_KEY_MEMBERID = 'memberId'
  DB_BATTLES_KEY_MATCH = 'keyMatch'
  DB_BATTLES_KEY_RESULT = 'keyResult'
  DB_BATTLES_UTC = 'utcTime'

  DB_TABLE_KEY_MATCH = 'keyMatch'
  DB_MATCH_ID = 'id'
  DB_MATCH_NAME = 'name'
  DB_VALUE_MATCH_COLLECTION_DAY = [0, 'Collection Day']
  DB_VALUE_MATCH_WAR_DAY = [1, 'War Day']

  DB_TABLE_KEY_RESULT = 'keyResult'
  DB_RESULT_ID = 'id'
  DB_RESULT_NAME = 'name'
  DB_VALUE_RESULT_WIN = [0, 'Win']
  DB_VALUE_RESULT_DRAW = [1, 'Draw']
  DB_VALUE_RESULT_LOSE = [2, 'Lose']

  DB_TABLE_KEY_STATUS = 'keyStatus'
  DB_STATUS_ID = 'id'
  DB_STATUS_NAME = 'name'
  DB_VALUE_STATUS_ACTIVE = [0, 'Active']
  DB_VALUE_STATUS_INACTIVE = [1, 'Inactive']

  def createTableIfNotExist(self):
    if self.conn.cursor().execute("SELECT COUNT(*) FROM sqlite_master WHERE type = 'table'").fetchone()[0] == 0:
      c = self.conn.cursor()
      c.execute('CREATE table {0} ({1} INTEGER PRIMARY KEY AUTOINCREMENT, {2} TEXT, {3} TEXT, {4} INTEGER)'.format(self.DB_TABLE_MEMBER, self.DB_MEMBER_ID, self.DB_MEMBER_TAG, self.DB_MEMBER_NAME, self.DB_MEMBER_KEY_STATUS))
      c.execute('CREATE table {0} ({1} INTEGER PRIMARY KEY AUTOINCREMENT, {2} INTEGER, {3} INTEGER, {4} INTEGER, {5} INTEGER)'.format(self.DB_TABLE_BATTLES, self.DB_BATTLES_ID, self.DB_BATTLES_KEY_MEMBERID, self.DB_BATTLES_KEY_MATCH, self.DB_BATTLES_KEY_RESULT, self.DB_BATTLES_UTC))
      c.execute('CREATE table {0} ({1} INTEGER PRIMARY KEY, {2} TEXT)'.format(self.DB_TABLE_KEY_MATCH, self.DB_MATCH_ID, self.DB_MATCH_NAME))
      c.execute('CREATE table {0} ({1} INTEGER PRIMARY KEY, {2} TEXT)'.format(self.DB_TABLE_KEY_RESULT, self.DB_RESULT_ID, self.DB_RESULT_NAME))
      c.execute('CREATE table {0} ({1} INTEGER PRIMARY KEY, {2} TEXT)'.format(self.DB_TABLE_KEY_STATUS, self.DB_STATUS_ID, self.DB_STATUS_NAME))
      self.conn.commit()

      c.execute('INSERT INTO {0} ({1}, {2}) VALUES ("{3}", "{4}")'.format(self.DB_TABLE_KEY_MATCH, self.DB_MATCH_ID, self.DB_MATCH_NAME, self.DB_VALUE_MATCH_COLLECTION_DAY[0], self.DB_VALUE_MATCH_COLLECTION_DAY[1]))
      c.execute('INSERT INTO {0} ({1}, {2}) VALUES ("{3}", "{4}")'.format(self.DB_TABLE_KEY_MATCH, self.DB_MATCH_ID, self.DB_MATCH_NAME, self.DB_VALUE_MATCH_WAR_DAY[0], self.DB_VALUE_MATCH_WAR_DAY[1]))
      self.conn.commit()

      c.execute('INSERT INTO {0} ({1}, {2}) VALUES ("{3}", "{4}")'.format(self.DB_TABLE_KEY_RESULT, self.DB_RESULT_ID, self.DB_RESULT_NAME, self.DB_VALUE_RESULT_WIN[0], self.DB_VALUE_RESULT_WIN[1]))
      c.execute('INSERT INTO {0} ({1}, {2}) VALUES ("{3}", "{4}")'.format(self.DB_TABLE_KEY_RESULT, self.DB_RESULT_ID, self.DB_RESULT_NAME, self.DB_VALUE_RESULT_DRAW[0], self.DB_VALUE_RESULT_DRAW[1]))
      c.execute('INSERT INTO {0} ({1}, {2}) VALUES ("{3}", "{4}")'.format(self.DB_TABLE_KEY_RESULT, self.DB_RESULT_ID, self.DB_RESULT_NAME, self.DB_VALUE_RESULT_LOSE[0], self.DB_VALUE_RESULT_LOSE[1]))
      self.conn.commit()

      c.execute('INSERT INTO {0} ({1}, {2}) VALUES ("{3}", "{4}")'.format(self.DB_TABLE_KEY_STATUS, self.DB_STATUS_ID, self.DB_STATUS_NAME, self.DB_VALUE_STATUS_ACTIVE[0], self.DB_VALUE_STATUS_ACTIVE[1]))
      c.execute('INSERT INTO {0} ({1}, {2}) VALUES ("{3}", "{4}")'.format(self.DB_TABLE_KEY_STATUS, self.DB_STATUS_ID, self.DB_STATUS_NAME, self.DB_VALUE_STATUS_INACTIVE[0], self.DB_VALUE_STATUS_INACTIVE[1]))
      self.conn.commit()

    return True

  def dbOpen(self):
    self.conn = sqlite3.connect(self.dbPath)

  def dbClose(self):
    self.conn.close()

  def createMember(self, tag, name, status=DB_VALUE_STATUS_ACTIVE[0]):
    c = self.conn.cursor()
    c.execute("INSERT INTO {0} ({1}, {2}, {3}) VALUES (?, ?, ?)".format(self.DB_TABLE_MEMBER, self.DB_MEMBER_NAME, self.DB_MEMBER_TAG, self.DB_MEMBER_KEY_STATUS), (name, tag, status))
    self.conn.commit()

    return True

  def updaterMemberStatus(self, tag, status):
    c = self.conn.cursor()
    c.execute("UPDATE {0} SET {1}='{2}' WHERE {3}='{4}'".format(self.DB_TABLE_MEMBER, self.DB_MEMBER_KEY_STATUS, status, self.DB_MEMBER_TAG, tag))
    self.conn.commit()

  def readMember_Tag(self, tag):
    c = self.conn.cursor()
    c.execute("SELECT * FROM {0} WHERE {1}=?".format(self.DB_TABLE_MEMBER, self.DB_MEMBER_TAG), (tag,))
    for row in c:
      return row

  def createBattle(self, memberId, match, result, utcTime):
    c = self.conn.cursor()
    c.execute("INSERT INTO {0} ({1}, {2}, {3}, {4}) VALUES (?, ?, ?, ?)".format(self.DB_TABLE_BATTLES, self.DB_BATTLES_KEY_MEMBERID, self.DB_BATTLES_KEY_MATCH, self.DB_BATTLES_KEY_RESULT, self.DB_BATTLES_UTC), (memberId, match, result, utcTime))
    self.conn.commit()

    return True

  def readBattle(self, memberId, utcTime):
    c = self.conn.cursor()
    c.execute("SELECT * FROM {0} WHERE {1}=? AND {2}=?".format(self.DB_TABLE_BATTLES, self.DB_BATTLES_KEY_MEMBERID, self.DB_BATTLES_UTC), (memberId, utcTime))
    for row in c:
      return row

  def getMemberIdFromTag(self, memberTag):
    c = self.conn.cursor()
    c.execute("SELECT * FROM {0} WHERE {1}=?".format(self.DB_TABLE_MEMBER, self.DB_MEMBER_TAG), (memberTag,))
    for row in c:
      return row[0] if not row == None else None

  def updaterOtherMemberInactive(self, active_Tag):
    activeTag_string = ''
    for tag in active_Tag:
      activeTag_string = activeTag_string + ",'{0}'".format(tag)
    activeTag_string = activeTag_string[1:]

    c = self.conn.cursor()
    c.execute("SELECT {0} FROM {1} WHERE {2} not IN ({3})".format(self.DB_MEMBER_TAG, self.DB_TABLE_MEMBER, self.DB_MEMBER_TAG, activeTag_string))

    for tag in c:
      self.updaterMemberStatus(tag[0], self.DB_VALUE_STATUS_INACTIVE[0])

  def updateMemberList(self, memberList):
    active_Tag = []
    for member in memberList:
      active_Tag.append(member[self.DB_MEMBER_TAG])
      if self.readMember_Tag(member[self.DB_MEMBER_TAG]) == None:
        self.createMember(member[self.DB_MEMBER_TAG], member[self.DB_MEMBER_NAME])

    self.updaterOtherMemberInactive(active_Tag)

  def updateMemberBattleLog(self, memberTag, matchType, result, utcTime):
    memberId = self.getMemberIdFromTag(memberTag)
    if not memberId == None and self.readBattle(memberId, utcTime) == None:
      self.createBattle(memberId, matchType, result, utcTime)

    return True

  def getActiveClanMemberTag(self):
    c = self.conn.cursor()
    c.execute("SELECT * FROM {0} WHERE {1}='{2}'".format(self.DB_TABLE_MEMBER, self.DB_MEMBER_KEY_STATUS, self.DB_VALUE_STATUS_ACTIVE[0]))
    tag = []
    tag_string = ''
    for row in c:
      tag.append(row[0])
      tag_string = tag_string + ',' + str(row[1])
    return tag_string[1:]

  def getActiveMemberNumber(self):
    c = self.conn.cursor()
    c.execute("SELECT count(*) as count, * from {0} where {1}='{2}'".format(self.DB_TABLE_MEMBER, self.DB_MEMBER_KEY_STATUS, self.DB_VALUE_STATUS_ACTIVE[0]))
    for row in c:
      return row[0]

  def __init__(self, dbPath):
    self.dbPath = dbPath

    self.dbOpen()
    self.createTableIfNotExist()
