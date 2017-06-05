# NBA_Stats_Bot
NBA player stats bot for Reddit.

NBA_Stats_Bot is a bot (/u/NBA_Stats_Bot) written using praw that searches in  r/nba subreddit for a comment with a players name and the keyword "STATS". Then searches basketball-reference.com for players stats and replies to comment with players name, nba debut, main stats, and a link to the source url. 

NBA_Stats_Bot.py is the main file that logs in, retrieves comments file, and runs bot. Comment limit set to 25 and restarts after 15 seconds. Program imports a modified version of nba_stat_scraper which instead of asking for player input, uses the names retrieved from comment to search in basketball-reference database and posts comment instead of print() function.

config.py is imported for bot credentials: contains username, password, client id, and client secret. Actual information not given.

![ScreenShot](https://github.com/wfar/NBA_Stats_Bot/blob/master/NBA_Stats_Bot/Stats%20bot%20example.png)

