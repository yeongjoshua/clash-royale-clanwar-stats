# This is a project which records clan war battles for clans in Clash Royale

## Libraries Required
```
sqlite 3.3.x and above
```

## Start Update Clan Details every hour
```
nohup python3 updateClan.py
```

## Stop Update
```
kill -9 $(ps -e | grep python | grep updateClan.py | awk '{print $1}')
```