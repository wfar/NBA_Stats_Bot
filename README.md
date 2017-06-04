# NBA_Stats_Bot
NBA player stats bot for Reddit.

NBA_Stats_Bot is a bot (/u/NBA_Stats_Bot) written using praw that searches in  r/nba subreddit for a comment with a players name and the keyword "STATS". Then searched basketball-reference.com for players stats and replies to comment with players name, nba debut, main stats, and a link to the source url. 

NBA_Stats_Bot.py is the main file. Inside is login_bot(),  connects the bot to reddit, get_saved_comments(), which loads saved_comments.txt if there is one or if there isnt a saved_comments.txt file, it makes a new list called saved_comments which gets saved into a .txt file.  run_bot() searches through the comments in r/NBA for the word "STATS" and if the comment is not in saved_comments.txt or a comment made by the bot itself it takes the players name that preceeds it, searches through basketball-reference.com database for player posts a reply to the comment with player stats.



