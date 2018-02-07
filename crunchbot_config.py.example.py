# set this to True to view results without actual votes or replies
RUN_IN_TEST_MODE = False

# the default node from the Python library throws connection errors
NODE_URI = 'https://api.steemit.com'

BOT_ACCOUNT_NAME = 'account_name_here'
BOT_PWD = 'account_pwd_here'
BOT_POSTING_KEY = 'account_private_posting_key_here'
# BOT_ACTIVE_KEY = 'account_private_active_key_here'

DO_UPVOTE_POSTS = True
VOTE_WEIGHT = 100.0
UPVOTE_DELAY_MINUTES = 15
SLEEP_VOTE_SECONDS = 7

DO_REPLY_TO_MENTIONS = False
REPLY_TEXT = 'OH YEAH!!!!'
SLEEP_REPLY_SECONDS = 25

# comma-separated list of account to check
AUTHOR_LIST = [
    'author_account_name_one',
    'author_account_name_two'
]
AUTHOR_HISTORY_COUNT = 3

DEBUG_MODE = True