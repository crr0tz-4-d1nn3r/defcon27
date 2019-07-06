# scrapeWorkshopsMain.py
# last updated 2019 July 6 at 14:30

from bs4 import BeautifulSoup 
import csv 
import os
import re
import requests 
from dateutil import parser
from datetime import timedelta

def scrapeWorkshopsMain():
    
    print('Running Scrape of Main Workshops')
    # ------------ site scrape basics ------------
    URL = "https://www.defcon.org/html/defcon-27/dc-27-workshops.html"
    r = requests.get(URL, timeout=5) 
    soup = BeautifulSoup(r.content, 'html.parser') 
    
    # ------------ do stuff with data ------------
    workshopList = []
    articles = soup.findAll('article',attrs={"class":"talk"})
    reg0 = re.compile(r'(.*), (.*) in (.*)')
    for article in articles:
        workshop = {}
        
        # title
        workshop['title'] = article.find('h3', attrs={'class':'talkTitle'}).text
        
        # day, time, track, duration
        t = article.find('p', attrs={'class':'abstract'}).text
        g0 = reg0.match(t).groups()
        
        if g0[0] != '':
            workshop['day'] = g0[0]
            t1 = str(int(g0[1].split('-')[0])/100).replace('.', ':') + '0'
            t2 = str(int(g0[1].split('-')[1])/100).replace('.', ':') + '0'
            workshop['time'] = t1
            workshop['track'] = g0[2]
            
            minutes = (parser.parse(t2) - parser.parse(t1))/timedelta(seconds=60)
            workshop['duration'] = '{0:.0f}'.format(minutes)
        else:
            workshop['day'] = ''
            workshop['time'] = ''
            workshop['track'] = ''
            workshop['duration'] = ''
        
        # speakers
        speakers = article.find_all('h4', attrs={'class':'speaker'})
        speakersStr = ''
        for speaker in speakers:
            speakersStr = speakersStr + speaker.text + ','
        speakersStr = speakersStr[:-1]
        workshop['speaker'] = speakersStr
        
        # abstract        
        found = False
        abstractStr = ''
        # first one in the page should be location and time, skip it
        temp = article.find(['p', 'li']) 
        while not found:
            # get the next p or li tag
            temp = temp.find_next(['p', 'li'])
            # if we reach the Skill Level section - record info and stop
            # otherwise add it to the abstract
            if temp.find(string='Skill Level'):
                workshop['skillLevel'] = temp.text.split('Skill Level')[1]
                found = True
            else:
                abstractStr = abstractStr + temp.text
        workshop['abstract'] = abstractStr
        
        # assuming the following are in this order
        # not the prettiest - but a loop would not be much better, imo
        temp = temp.find_next('p', attrs={'class':'abstract'});
        workshop['prerequisites'] = temp.text.split(':')[1]
        temp = temp.find_next('p', attrs={'class':'abstract'});
        workshop['materials'] = temp.text.split(':')[1]
        temp = temp.find_next('p', attrs={'class':'abstract'});
        workshop['maxStudents'] = temp.text.split(':')[1]
        temp = temp.find_next('p', attrs={'class':'abstract'});
        workshop['registration'] = temp.text.split(':',1)[1]
        
        # speaker bio
        speakers = article.find_all('p', attrs={'class':'speakerBio'})
        speakersStr = ''
        for speaker in speakers:
            speakersStr = speakersStr + speaker.text + ','
        speakersStr = speakersStr[:-1]
        workshop['speakerBio'] = speakersStr
    
        # for partial merging with talks list
        workshop['tags'] = 'workshop'
        
        # store results
        workshopList.append(workshop)
        
    # sorting
    Thursday = []
    Friday = []
    Saturday = []
    Sunday = []
    TBA = []
    for workshop in workshopList:
        if workshop['day'] == 'Thursday':
            Thursday.append(workshop)
        elif workshop['day'] == 'Friday':
            Friday.append(workshop)
        elif workshop['day'] == 'Saturday':
            Saturday.append(workshop)
        elif workshop['day'] == 'Sunday':
            Sunday.append(workshop)
        else:
            TBA.append(workshop)
    
    workshopList = sorted(Thursday, key=lambda x: x['time'])
    workshopList.extend(sorted(Friday, key=lambda x: x['time']))
    workshopList.extend(sorted(Saturday, key=lambda x: x['time']))
    workshopList.extend(sorted(Sunday, key=lambda x: x['time']))
    workshopList.extend(sorted(TBA, key=lambda x: x['time']))
    
    # save the resuts
    dirname = os.path.dirname(__file__)
    filename = os.path.join(dirname, 'schedule_workshops_main.csv')
    print('Saving Results of Main Workshops to ' + filename)
    with open(filename, 'w', encoding='utf-8-sig',newline='') as f:
        w = csv.DictWriter(f,fieldnames =['title', 'day','time','track', 'duration', 'tags', 'speaker', 'abstract', 'speakerBio', 'skillLevel', 'prerequisites','materials', 'maxStudents', 'registration' ])
        w.writeheader()
        for workshop in workshopList:
            w.writerow(workshop)

if __name__ == '__main__':
    scrapeWorkshopsPHV()