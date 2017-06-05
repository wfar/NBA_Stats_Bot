from bs4 import BeautifulSoup
import requests
import re

def get_player_page(player_last, player_first):
    # Asks for player and gets player href.
    url = 'http://www.basketball-reference.com/players/'
    last = player_last.lower()
    first = player_first.lower()
    fullname = first.capitalize() + ' ' + last.capitalize()
    s_fullname = first + ' ' + last
    last_i = last[0] +'/'
    connect = url + last_i
    source = requests.get(connect).text
    soup = BeautifulSoup(source, 'lxml')
    hrefs = []
    for a in soup.findAll('a'):
        name = a.get_text().lower()
        if s_fullname == name:
            href = a.get('href')
            hrefs.append(href)
    
    return hrefs, fullname

def create_url(hrefs):
    # Uses player href to make player url.
    url = 'http://www.basketball-reference.com'
    player_url_list = []
    for x in hrefs:
            player_url = url + x
            player_url_list.append(player_url)

    return player_url_list

def get_debut(player_url):
    # Searches and returns players NBA debut date.
    rx = '(Jan(uary)?|Feb(ruary)?|Mar(ch)?|Apr(il)?|May|Jun(e)?|Jul(y)?|Aug(ust)?|Sep(tember)?|Oct(ober)?|Nov(ember)?|Dec(ember)?)\s+\d{1,2},\s+\d{4}'
    source = requests.get(player_url).text
    soup = BeautifulSoup(source, 'lxml')
    date = []
    for x in soup.findAll('p'):
        for z in x.findAll('strong'):
            text_1 = z.string
            if 'NBA Debut:' in str(text_1):
                date.append(text_1)
        for y in x.findAll('a'):
            text_2 = y.string
            if re.search(rx, text_2):
                date.append(text_2)
    return date

def get_player_stats(player_url):
    # Gets NBA players stats and puts them into lists.
    p1 = []
    p2 = []
    p3 = []
    source = requests.get(player_url).text
    soup = BeautifulSoup(source, 'lxml')
    for p in soup.findAll('div' , {'class': 'p1'}):
        par = p.findAll('p')
        for q in par:
            p1.append(q)    
    for p in soup.findAll('div' , {'class': 'p2'}):
        par = p.findAll('p')
        for q in par:
            p2.append(q)    
    for p in soup.findAll('div' , {'class': 'p3'}):
        par = p.findAll('p')
        for q in par:
            p3.append(q)    
    
    return p1, p2, p3

def remove_elements(p1,p2,p3):
    # Turns data into strings and removes all tags.
    p1 = [str(x) for x in p1]
    p2 = [str(x) for x in p2]
    p3 = [str(x) for x in p3]
    
    p1 = [x.replace('<p>', '') for x in p1]
    p2 = [x.replace('<p>', '') for x in p2]
    p3 = [x.replace('<p>', '') for x in p3]

    p1 = [x.replace('</p>', '') for x in p1]
    p2 = [x.replace('</p>', '') for x in p2]
    p3 = [x.replace('</p>', '') for x in p3]

    return p1, p2, p3

def sort_stats(p1, p2, p3):
    # Sorts all of player stats from lists into dictionary.
    value_p1 = ['G', 'G', 'PTS', 'PTS', 'TRB', 'TRB', 'AST', 'AST', 'WS', 'WS' ]
    value_p2 = ['FG%', 'FG%', 'FG3%', 'FG3%', 'FT%', 'FT%', 'eFG%', 'eFG%'  ]
    value_p3 = ['PER', 'PER', 'WS', 'WS' ]
    
    current_dict = {}
    career_dict = {}

    loc = 0
    for x,y in zip(p1, value_p1):
        if loc == 0:
            current_dict[y] = x
            loc += 1
        else:
            career_dict[y] = x
            loc -= 1
    for x,y in zip(p2, value_p2):
        if loc == 0:
            current_dict[y] = x
            loc += 1
        else:
            career_dict[y] = x
            loc -= 1
    for x,y in zip(p3, value_p3):
        if loc == 0:
            current_dict[y] = x
            loc += 1
        else:
            career_dict[y] = x
            loc -= 1
    
    return current_dict, career_dict

def present_stats(current_dict, career_dict, date, comment, fullname, source):
    # Prints all player stats in a clean and ordered format.
    
    data_0 = '{:^8} {:^8} {:^8} {:^8} {:^8} {:^8} {:^8} {:^8} {:^8} {:^8} {:^8} {:^8}'.format('','','G','PTS','TRB','AST','FG%',
                                                                                        'FG3%','FT%','eFG%','PER','WS')
    spacer = '{:^8} {:^8} {:^8} {:^8} {:^8} {:^8} {:^8} {:^8} {:^8} {:^8} {:^8} {:^8}'.format('','','----','----','----','----',
                                                                                        '----','----','----','----','----','----')
        
    data_1 = '{:^8} {:^8} {:^8} {:^8} {:^8} {:^8} {:^8} {:^8} {:^8} {:^8} {:^8} {:^8}'.format('','Current:',current_dict.get('G'),current_dict.get('PTS'),
                                                        current_dict.get('TRB'),current_dict.get('AST'),current_dict.get('FG%'), current_dict.get('FG3%'),
                                                        current_dict.get('FT%'), current_dict.get('eFG%'),current_dict.get('PER'), current_dict.get('WS'))
    data_2 = '{:^8} {:^8} {:^8} {:^8} {:^8} {:^8} {:^8} {:^8} {:^8} {:^8} {:^8} {:^8}'.format('','Career:',career_dict.get('G'),career_dict.get('PTS'),
                                                        career_dict.get('TRB'),career_dict.get('AST'),career_dict.get('FG%'), career_dict.get('FG3%'),
                                                        career_dict.get('FT%'), career_dict.get('eFG%'),career_dict.get('PER'), career_dict.get('WS'))
        
    if '' not in current_dict.values():
        comment.reply('\nPlayer: ' + fullname + '\n \n' + date[0] + date[1] + '\n\n' + data_0 + '\n' + spacer + '\n' + data_1 + '\n' + data_2 +  '\n \n' + source)
    else:
        comment.reply('\nPlayer: ' + fullname + '\n \n' + date[0] + date[1] + '\n\n' + data_0 + '\n' + spacer + '\n' + data_2 + '\n \n' + source)

def post_stats(player_first, player_last, comment):
    # Pieces together all components and posts reply to reddit.    
    hrefs, fullname = get_player_page(player_last, player_first)
    player_url_list = create_url(hrefs)
    if len(player_url_list) >= 1:
        for x in player_url_list:
            player_url = x
            source = '[Source](' + player_url + ')'
            date = get_debut(player_url)
            p1, p2, p3 = get_player_stats(player_url)
            p1, p2, p3 = remove_elements(p1, p2, p3)
            current_dict, career_dict = sort_stats(p1, p2, p3)
            present_stats(current_dict, career_dict, date, comment, fullname, source)
    else:
        comment.reply('\nPlayer not found. Please try again.')
    


