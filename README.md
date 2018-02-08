# crunhbot setup

### terminal reqs
```
python --version
pip --version
```

### libraries
```
pip install steem
pip install tqdm
```

### config values (crunchbot_config.py)
BOT_ACCOUNT_NAME  
BOT_PWD  
BOT_POSTING_KEY  
AUTHOR_LIST  

### terminal 
```
python crunchbot_vote.py
while true; do python crunchbot_vote.py; sleep 60; done
pmset noidle
```

### to do
vote limit per day  
vote weight other than 100  
vote delay per author  
skip vote depending on existing votes  
