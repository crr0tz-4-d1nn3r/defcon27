# scrapeWorkshopsPHV.py
# last updated 2019 July 6 at 14:30

from bs4 import BeautifulSoup 
import csv 
import os
import requests 
from dateutil import parser
from datetime import timedelta

def scrapeWorkshopsPHV():
    
    print('Running Scrape of PHV Workshops')
    # ------------ site scrape basics ------------
    URL = "https://www.wallofsheep.com/blogs/news/packet-hacking-village-workshops-at-def-con-27-finalized"
    r = requests.get(URL, timeout=5) 
    soup = BeautifulSoup(r.content, 'html.parser') 
    
    # ------------ do stuff with data ------------
    
    # use the table to get the basic list going - then check links for abstract and bios
    # there are three tables on this page - one for each day
    tables = soup.find_all('tbody')
    days = ['Friday', 'Saturday', 'Sunday']
    # making a lists of dictionaries
    # each list contains Dictionaries with the following keys
    # 'title', 'day','time','track', 'duration', 'tags'=workshop, 'speaker', 'abstract',
    # 'speakerBio', 'skillLevel'='', 'prerequisites', 'materials'='', 'maxStudents'='', 
    # 'registration'= TBA
    workshopList = []
    count = 0
    for table in tables:
        rows = table.find_all('tr')
        day = days[count]
        for row in rows:
            workshop = {}
            # time of talk should be in the header of this row
            t1 = row.th.text.split('-')[0]
            t2 = row.th.text.split('-')[1]
            minutes = (parser.parse(t2) - parser.parse(t1))/timedelta(seconds=60)
            workshop['day'] = day
            workshop['time'] = t1
            workshop['duration'] = '{0:.0f}'.format(minutes)
            
                        
            # grab anchor text (strip the '#'), use to workshop info 
            anchor = row.td.a['href'].replace('#','')
            more = soup.find('h3', attrs = {'id':anchor})
            
            # title, speakers and abstract are easy
            workshop['title'] = more.text.strip()   
            more = more.find_next('h4')
            workshop['speaker'] = more.text
            more = more.find_next('p')
            workshop['abstract'] = more.text.strip()
            
            # this may be followed by a Prereqs paragraph, and one or more speaker bios
            more = more.find_next()
            flag = True
            speakersStr = ''
            while more.name == 'p':
                # the first paragraph following abstract may be a prereq
                if flag and 'Prerequisites' in more.text:
                    workshop['prerequisites'] = more.text.strip()
                else:
                     flag = False
                     speakersStr += more.text.strip()
                more = more.find_next()
            workshop['speakerBio'] = speakersStr
            
            # defaults
            workshop['track'] = 'Skyview 1, 2, 5, 6 -Bally\'s'
            workshop['tags'] = 'workshop'
            workshop['skillLevel'] = ''
            workshop['materials'] = ''
            workshop['maxStudents'] = ''
            workshop['registration'] = 'TBA'
            workshopList.append(workshop)
        
        # get ready for next table/day
        count += 1
    
    # save the resuts
    dirname = os.path.dirname(__file__)
    filename = os.path.join(dirname, 'schedule_workshops_phv.csv')
    print('Saving Results of PHV Workshops to ' + filename)
    with open(filename, 'w', encoding='utf-8-sig',newline='') as f:
        w = csv.DictWriter(f,fieldnames =['title', 'day','time','track', 'duration', 'tags', 'speaker', 'abstract', 'speakerBio', 'skillLevel', 'prerequisites','materials', 'maxStudents', 'registration' ])
        w.writeheader()
        for workshop in workshopList:
            w.writerow(workshop)
        

if __name__ == '__main__':
    scrapeWorkshopsPHV()

