import praw
import config
import re
import os
import time
import nba_stat_scraper_2 as nss



def login():
    # Connects bot to reddit.
    reddit = praw.Reddit(client_id = config.client_id,
                client_secret = config.client_secret, password = config.password,
                user_agent = "NBA Stats Bot v1.0 (by /u/NBA_Stats_Bot)",
                username = config.username)
    
    return reddit

def get_saved_comments():
    # Opens saved comments file or creates a new one.
    if not os.path.isfile('saved_comments.txt'):
        saved_comments = []
    else:
        with open('saved_comments.txt', 'r') as f_obj:
            saved_comments = f_obj.read()
            saved_comments = saved_comments.split('\n')

    return saved_comments

def run_bot(reddit, saved_comments):
    # Searches for NBA players names and posts a reply with stats.
    print('Searching comments')
    player_names = []
    for comment in reddit.subreddit('nba').comments(limit=25):
        if 'STATS' in comment.body and comment.id not in saved_comments and not comment.author == reddit.user.me():
            print('Comment with "STATS" found')
            search = comment.body
            name = re.findall('.+?(?=\sSTATS)', search)
            player_names.append(name)

            saved_comments.append(comment.id)
            with open('saved_comments.txt', 'a') as f_obj:
                f_obj.write(comment.id + '\n')
            
            player_names = [''.join(a) for a in player_names]
            for name in player_names:
                print('Getting stats')
                spl = name.split(' ')
                player_first = spl[0]
                player_last = spl[1]
                print('Posting comment')
                nss.post_stats(player_first, player_last, comment)
                del player_names[:]
            
def main():
    # Runs Program.
    saved_comments = get_saved_comments()
    reddit = login()
    while True:        
        run_bot(reddit, saved_comments)
        print('Restarting in 15 seconds')
        time.sleep(15)
        

if __name__ == "__main__":
    main()
    
