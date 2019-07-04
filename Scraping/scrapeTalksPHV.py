# scrapeTalksPHV.py
# last updated 2019 July 3 at 15:00

from bs4 import BeautifulSoup 
import csv 
import os
import re
import requests 
from dateutil import parser
from datetime import timedelta

# ------------ site scrape basics ------------
URL = "https://www.wallofsheep.com/blogs/news/packet-hacking-village-talks-and-schedule-at-def-con-27-finalized.html"
r = requests.get(URL, timeout=5) 
soup = BeautifulSoup(r.content, 'html.parser') 

# ------------ do stuff with data ------------
# use the table to get the basic list going - then check links for abstract and bios
table_body = soup.find('tbody')
rows = table_body.find_all('tr')

# making a lists of dictionaries
# each list contains Dictionaries with the following keys
# day, time, title, speaker, abstract, speakerBio, duration, track=26th Floor Bally's, tags ='',  
TalksList = []

# some talks span a couple rows - keep a counter
# set counter > 0 to keep track for how many rows to skip before looking for it again
skipFlag = [0,0,0]
cellDict = {0:'Friday', 1:'Saturday', 2:'Sunday'}

# first row is the headers - skip
for row in rows[1:]:
    # time of talk should be in the header of this row
    time = row.th.text
        
    # figure out which cells in this row we should hit
    cellCount = []
    count = 0
    for flag in skipFlag:
        if not flag:
            cellCount.append(count)
        count+=1
    
    # decrement the skip counters
    skipFlag[:] = [x-1 if x > 0 else 0 for x in skipFlag]
    
    # get cells in this row (# between 0 and 3)
    cells = row.find_all('td')
        
    count = 0
    for cell in cells:
        # make sure not empty
        if not(cell.text=='' or cell.text.isspace()):               
            talk = {}
            # check to see if cell has a link - if no, this is not a talk
            if cell.a is not None:            
                talk['title'] = cell.a.text.strip()   
                
                # grab anchor text (strip the '#'), use to find abstract and bio 
                anchor = cell.a['href'].replace('#','')
                a = soup.find('h3', attrs = {'id':anchor})
                a = a.find_next('h4')
                talk['speaker'] = a.text
                
                # currently, only one paragraph of abstract
                a = a.find_next('p')
                talk['abstract'] = a.text
                
                # as of now, there are only two speakers max, if more - change to while
                speakerStr = ''
                a = a.find_next_sibling()
                speakerStr = a.text        
                a = a.find_next_sibling()
                if a.name == 'p':
                    speakerStr += a.text
                talk['speakerBio'] = speakerStr
                
                # some defaults
                talk['day'] = cellDict[cellCount[count]]
                talk['time'] = time
                talk['track'] = 'Skyview 1, 2, 5, 6 -Bally\'s'
                talk['tags'] = 'packet hacking village'
                
                # save info
                TalksList.append(talk)
        
        # empty or otherwise get ready for next cell
        if cell.has_attr('rowspan'):
            skipFlag[cellCount[count]] = int(cell.attrs['rowspan']) - 1
        count+=1

# sorting
Friday = []
Saturday = []
Sunday = []
TBA = []
for talk in TalksList:
    if talk['day'] == 'Friday':
        Friday.append(talk)
    elif talk['day'] == 'Saturday':
        Saturday.append(talk)
    elif talk['day'] == 'Sunday':
        Sunday.append(talk)
    else:
        TBA.append(talk)

TalksList = sorted(Friday, key=lambda x: x['time'])
TalksList.extend(sorted(Saturday, key=lambda x: x['time']))
TalksList.extend(sorted(Sunday, key=lambda x: x['time']))
TalksList.extend(sorted(TBA, key=lambda x: x['time']))

# now, for duration
duration = '60 minutes'
for i in range(1,len(TalksList)):
    if TalksList[i]['day'] == TalksList[i-1]['day']:
        minutes = (parser.parse(TalksList[i]['time']) - parser.parse(TalksList[i-1]['time']))/timedelta(seconds=60)
        TalksList[i-1]['duration'] = '{0:.0f}'.format(minutes)
    else:
        # seems that the last talks of the day are 60 min, may change in the future
        TalksList[i-1]['duration'] = '60'
TalksList[i]['duration'] = '60'

# save the resuts
dirname = os.path.dirname(__file__)
filename = os.path.join(dirname, 'schedule_talks_phv.csv')
with open(filename, 'w', encoding='utf-8-sig',newline='') as f:
    w = csv.DictWriter(f,fieldnames =['title', 'day','time','track','duration','tags', 'speaker', 'abstract','speakerBio' ])
    w.writeheader()
    for talk in TalksList:
        w.writerow(talk)
