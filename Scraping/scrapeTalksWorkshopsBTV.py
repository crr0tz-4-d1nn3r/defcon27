# scrapeTalksBTV.py
# last updated 2019 July 6 at 15:00
from bs4 import BeautifulSoup 
import csv 
import os
import re
import requests 
from dateutil import parser
from datetime import timedelta

def scrapeTalksWorkshopsBTV():    
    print('Running Scrape of BTV Talks and Workshops')
    
    # ------------ site scrape basics ------------
    URL1 = "https://www.blueteamvillage.org/dc27/schedule"
    URL2 = "https://www.blueteamvillage.org/dc27/talks"
    URL3 = "https://www.blueteamvillage.org/dc27/workshops"
    
    # info is spread across two sites
    # first site has time and title, the other has abstracts and bios
    r = requests.get(URL1, timeout=5) 
    soup = BeautifulSoup(r.content, 'html.parser') 
    
    # boy this site is a mess, 
    # but it looks like everything is given a unique id, so we know where to start
    data = soup.find('p', attrs={'id':'h.p_VLHc-F7LmxJj'})
    # and we can search for a time format to distinguish day/track info from talk
    rex1 = re.compile('\d\d:\d\d') 
    rex2 = re.compile('\d\d:\d\d: Open$|\d\d:\d\d: Close$')
    rex3 = re.compile('(\d+)(\w+) (\w+)')
    talksList = []
    workshopList = []
    day = ''
    track = ''
    while data.name == 'p':
        str1 = data.text
        # check if data time and talk
        if rex1.match(str1) and not rex2.match(str1):
            talk = {}
            talk['day'] = day
            talk['track'] = track
            talk['time'] = ':'.join(str1.split(':',2)[:2])
            str2 =str1.split(' (')
            talk['title'] = str2[0].split(': ',1)[1]
            if len(str2) > 1:
                g = rex3.match(str2[1]).groups()
                # time 
                if g[1] == 'Min':
                    talk['duration'] = g[0]
                    
                else:
                    talk['duration'] = '{0:.0f}'.format(int(g[0])*60)
                    
                # check if this is a talk or workshop
                if g[2] == 'Workshop':
                    talk['tags'] = 'workshop'
                    workshopList.append(talk)
                else:
                    talk['tags'] = 'Blue Team village'
                    talksList.append(talk)
                 
        elif not rex1.match(str1):
            day = str1.split(':')[0]
            track = str1.split(':')[1].strip()
        data = data.find_next()
    
    # To the talks site
    r = requests.get(URL2, timeout=5) 
    soup = BeautifulSoup(r.content, 'html.parser') 
    
    # talks are in day/time order and the only place h2 is used in the title of talks
    data = soup.find_all('h2')
    for n in range(len(data)):
        talk = talksList[n]
        pointer = data[n].find_next_sibling()
        speakersStr = ''
        speakerBio = ''
        while pointer.name == 'p' and pointer.strong is not None:
            speakersStr += pointer.strong.text + ', '
            speakerBio += pointer.text
            pointer = pointer.find_next_sibling()
        speakersStr = speakersStr[:-2]
        talk['speaker'] = speakersStr
        talk['speakerBio'] = speakerBio
        
        if pointer.name == 'p':
            talk['abstract'] = pointer.text
        else:
            talk['abstract'] = ''
            
    # To the workshops site
    r = requests.get(URL3, timeout=5) 
    soup = BeautifulSoup(r.content, 'html.parser') 
    
    data = soup.find_all('h2')
    for n in range(len(data)):
        workshop = workshopList[n]
        pointer = data[n].find_next_sibling()
        speakersStr = ''
        speakerBio = ''
        while pointer.name == 'p' and pointer.strong is not None:
            speakersStr += pointer.strong.text + ', '
            speakerBio += pointer.text
            pointer = pointer.find_next_sibling()
        speakersStr = speakersStr[:-2]
        workshop['speaker'] = speakersStr
        workshop['speakerBio'] = speakerBio
        
        abstractStr = ''
        while pointer is not None and pointer.name == 'p':
            abstractStr += pointer.text
            pointer = pointer.find_next_sibling()
        workshop['abstract'] = abstractStr
    
    
    
    # save the resuts
    dirname = os.path.dirname(__file__)
    filename = os.path.join(dirname, 'schedule_talks_btv.csv')
    print('Saving Results of BTV Talks to ' + filename)
    with open(filename, 'w', encoding='utf-8-sig',newline='') as f:
        w = csv.DictWriter(f,fieldnames =['title', 'day','time','track','duration','tags', 'speaker', 'abstract','speakerBio' ])
        w.writeheader()
        for talk in talksList:
            w.writerow(talk)
    
    # save the resuts
    dirname = os.path.dirname(__file__)
    filename = os.path.join(dirname, 'schedule_workshops_btv.csv')
    print('Saving Results of BTV Workshops to ' + filename)
    with open(filename, 'w', encoding='utf-8-sig',newline='') as f:
        w = csv.DictWriter(f,fieldnames =['title', 'day','time','track', 'duration', 'tags', 'speaker', 'abstract', 'speakerBio', 'skillLevel', 'prerequisites','materials', 'maxStudents', 'registration' ])
        w.writeheader()
        for workshop in workshopList:
            w.writerow(workshop)

if __name__ == '__main__':
    scrapeTalksWorkshopsBTV()