import datetime
import crunchbot_config
import steem.utils
from steem import Steem
from time import sleep
from tqdm import tqdm, trange
from dateutil import parser

##############################################################################################

class SteemPostDetail:

    def __init__(self, detail_dict, steem_instance):
        self.details = detail_dict
        self.steem = steem_instance
        self.replies = None
        self.identifier = None

    def get_firstlevel_replies(self):
        if self.replies is None:
            self.replies = self.steem.get_content_replies(self.details['author'], self.details['permlink'])
        return self.replies
        
    def get_identifier(self):
        if self.identifier is None:
            self.identifier = steem.utils.construct_identifier(
                self.details['author'],
                self.details['permlink']
        )
        return self.identifier

    def get_minutes_old(self):
        return (datetime.datetime.utcnow() - parser.parse(self.details['created'])).total_seconds() / 60
        
    def vote_for_post(self, voter_name, weight):
        s.commit.vote(self.get_identifier(), weight, voter_name)

    def is_upvoteable_for_voter(self, voter_name, age_buffer_in_minutes):
        if self.details['depth'] > 0:
            debug_msg('Post is not top level')
            return False
        elif self.details['net_rshares'] is None:
            debug_msg('Post is archived')
            return False
        else:
            if self.get_minutes_old() < age_buffer_in_minutes:
                debug_msg('Post is not old enough')
                return False

        for vote in self.details['active_votes']:
            if vote['voter'] == voter_name:
                debug_msg(voter_name + ' already voted')
                return False

        return True
        
    def needs_reply_for_author(self, author_name):
        if self.has_mention_for_author(author_name) and not self.has_author_replied(author_name):
            return True
        return False
        
    def has_mention_for_author(self, author_name):
        if str('@' + author_name) in self.details['body']:
            return True
        return False

    def has_author_replied(self, author_name):
        for r in self.get_firstlevel_replies():
            if r['author'] == author_name:
                return True
        return False

def wait_with_progress_bar(seconds):
    print('Waiting ' + str(seconds) + ' seconds')
    l = [None] * seconds
    for s in tqdm(l, total=seconds, ncols=100):
        sleep(1)

def print_msg_header(msg):
    print('------------------------------------------------------------')
    print(msg)
    print('------------------------------------------------------------')
    
def debug_msg(msg):
    if crunchbot_config.DEBUG_MODE:
        print(msg)
        
##############################################################################################
# s.commit.transfer('mr-dobalina', .001, 'SBD', 'OH YEAH! You got .001 SBD!', 'koolaidbot-9000')

print_msg_header(str(datetime.datetime.now()) + ': Process beginning with account = ' + crunchbot_config.BOT_ACCOUNT_NAME)

# s = Steem(nodes=[crunchbot_config.NODE_URI], wif=crunchbot_config.BOT_PWD, keys=[crunchbot_config.BOT_POSTING_KEY, crunchbot_config.BOT_ACTIVE_KEY])
s = Steem(nodes=[crunchbot_config.NODE_URI], wif=crunchbot_config.BOT_PWD, keys=[crunchbot_config.BOT_POSTING_KEY])
stats = {}

for author_name in crunchbot_config.AUTHOR_LIST:

    stats[author_name] = {'posts': 0, 'votes': 0, 'replies': 0}
    posts = s.get_blog_entries(author_name, -1, crunchbot_config.AUTHOR_HISTORY_COUNT)

    for post in posts:

        stats[author_name]['posts'] += 1

        post_detail = SteemPostDetail(s.get_content(post['author'], post['permlink']), s)
        
        if crunchbot_config.DO_UPVOTE_POSTS:
            print('Voteable check for ' + post_detail.get_identifier() + ' ...')
            if post_detail.is_upvoteable_for_voter(crunchbot_config.BOT_ACCOUNT_NAME, crunchbot_config.UPVOTE_DELAY_MINUTES):
            
                print(crunchbot_config.BOT_ACCOUNT_NAME + ' will upvote ' + post_detail.get_identifier())
            
                if crunchbot_config.RUN_IN_TEST_MODE:
                    print('Running in test mode ... no vote added')
                else:  
                    post_detail.vote_for_post(crunchbot_config.BOT_ACCOUNT_NAME, crunchbot_config.VOTE_WEIGHT)
                
                stats[author_name]['votes'] += 1
                wait_with_progress_bar(crunchbot_config.SLEEP_VOTE_SECONDS)

        if crunchbot_config.DO_REPLY_TO_MENTIONS:
            print('Mention check for ' + post_detail.get_identifier() + ' ...')
            for reply_content in post_detail.get_firstlevel_replies():
            
                reply_detail = SteemPostDetail(reply_content, s)
                if reply_detail.needs_reply_for_author(crunchbot_config.BOT_ACCOUNT_NAME):

                    print(crunchbot_config.BOT_ACCOUNT_NAME + ' will reply to ' + reply_detail.get_identifier())
                    if crunchbot_config.RUN_IN_TEST_MODE:
                        print('Running in test mode ... no reply added')
                    else: 
                        s.commit.post('', crunchbot_config.REPLY_TEXT, json_metadata=None, author=crunchbot_config.BOT_ACCOUNT_NAME, reply_identifier=reply_detail.get_identifier())
                    
                    stats[author_name]['replies'] += 1
                    wait_with_progress_bar(crunchbot_config.SLEEP_REPLY_SECONDS)

        print('')

print_msg_header(str(datetime.datetime.now()) + ': Process complete')
print(stats)
print('------------------------------------------------------------')