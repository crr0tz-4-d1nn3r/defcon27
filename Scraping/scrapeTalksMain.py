# scrapeTalksMain.py
# last updated 2019 July 6 at 15:00
from bs4 import BeautifulSoup 
import csv 
import os
import re
import requests 

def scrapeTalksMain():
    
    print('Running Scrape of Main Talks')
    # ------------ site scrape basics ------------
    URL = "https://www.defcon.org/html/defcon-27/dc-27-speakers.html"
    r = requests.get(URL, timeout=5) 
    soup = BeautifulSoup(r.content, 'html.parser') 
    
    # ------------ do stuff with data ------------
    agendaList = []
    articles = soup.findAll('article',attrs={"class":"talk"})
    reg0 = re.compile(r'(.*)\n\t(.*)')
    reg1 = re.compile(r'(.*) at (.*) in (.*)')
    for article in articles:
        agenda = {}
        
        # title
        agenda['title'] = article.find('h3', attrs={'class':'talkTitle'}).text
        
        # day, time, track, duration, tags - if any
        t = article.find('p', attrs={'class':'details'}).text
        temp = t.split('|')
        g0 = reg0.match(temp[0]).groups()
        
        if g0[0] != '':
            g1 = reg1.match(g0[0]).groups()
            agenda['day'] = g1[0]
            agenda['time'] = g1[1]
            agenda['track'] = g1[2]
        else:
            agenda['day'] = ''
            agenda['time'] = ''
            agenda['track'] = ''
        
        if g0[1] != '':
            agenda['duration'] = g0[1].split(' minutes')[0]
        else:
            agenda['duration'] = ''
        
        if len(temp) > 1:
            agenda['tags'] = temp[1]
        else:
            agenda['tags'] = ''
        
        # speaker
        agenda['speaker'] = article.find('h4', attrs={'class':'speaker'}).text
        
        # abstract
        agenda['abstract'] = article.find('p', attrs={'class':'abstract'}).text
        
        # speaker bio
        if article.find('p', attrs={'class':'speakerBio'}) is None:
            agenda['speakerBio'] = ''
        else:
            agenda['speakerBio'] = article.find('p', attrs={'class':'speakerBio'}).text
        
        agendaList.append(agenda)
        
    # sorting
    Thursday = []
    Friday = []
    Saturday = []
    Sunday = []
    TBA = []
    for agenda in agendaList:
        if agenda['day'] == 'Thursday':
            Thursday.append(agenda)
        elif agenda['day'] == 'Friday':
            Friday.append(agenda)
        elif agenda['day'] == 'Saturday':
            Saturday.append(agenda)
        elif agenda['day'] == 'Sunday':
            Sunday.append(agenda)
        else:
            TBA.append(agenda)
    
    agendaList = sorted(Thursday ,  key=lambda x: (x['time'], x['track']))
    agendaList.extend(sorted(Friday ,  key=lambda x: (x['time'], x['track'])))
    agendaList.extend(sorted(Saturday ,  key=lambda x: (x['time'], x['track'])))
    agendaList.extend(sorted(Sunday ,  key=lambda x: (x['time'], x['track'])))
    agendaList.extend(sorted(TBA ,  key=lambda x: (x['time'], x['track'])))
    
    
    # save the resuts
    dirname = os.path.dirname(__file__)
    filename = os.path.join(dirname, 'schedule_talks_main.csv')
    print('Saving Results of Main Talks to ' + filename)
    with open(filename, 'w', encoding='utf-8-sig',newline='') as f:
        w = csv.DictWriter(f,fieldnames =['title', 'day','time','track','duration','tags', 'speaker', 'abstract','speakerBio' ])
        w.writeheader()
        for agenda in agendaList:
            w.writerow(agenda)
            
if __name__ == '__main__':
    scrapeTalksMain()