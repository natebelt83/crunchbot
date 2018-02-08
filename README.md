# crunhbot setup

### terminal reqs
```
python3 --version
pip3 --version
```

### environment variables
```
export LDFLAGS="-L/usr/local/opt/openssl/lib"
export CPPFLAGS="-I/usr/local/opt/openssl/include"
```

### libraries
```
pip3 install steem
pip3 install tqdm
```

### config values (crunchbot_config.py)
BOT_ACCOUNT_NAME  
BOT_PWD  
BOT_POSTING_KEY  
AUTHOR_LIST  

### terminal 
```
python3 crunchbot_vote.py
while true; do python3 crunchbot_vote.py; sleep 60; done
pmset noidle
```

### to do
vote limit per day  
vote weight other than 100  
vote delay per author  
skip vote depending on existing votes  
