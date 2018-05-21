# This is a project which records clan war battles for clans in Clash Royale

Modify config.sample.ini and save as config.ini

## Requires
```
python 3.x
sqlite 3.x
```

## Start Update Clan Details every hour
```
nohup python3 updateClan.py
```

## Stop Update
```
kill -9 $(ps -e | grep python | grep updateClan.py | awk '{print $1}')
```