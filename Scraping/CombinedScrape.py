
import os
import glob
import pandas as pd
import scrapeTalksMain
import scrapeTalksPHV
import scrapeTalksWorkshopsBTV
import scrapeWorkshopsMain
import scrapeWorkshopsPHV


dirname = os.path.dirname(__file__)
os.chdir(dirname)

# run all scripts for updated info
scrapeTalksMain.scrapeTalksMain()
scrapeTalksPHV.scrapeTalksPHV()
scrapeTalksWorkshopsBTV.scrapeTalksWorkshopsBTV()
scrapeWorkshopsMain.scrapeWorkshopsMain()
scrapeWorkshopsPHV.scrapeWorkshopsPHV()

days2Dates = {'Thursday':'08/08/2019', 'Friday':'08/09/2019', 'Saturday':'08/10/2019', 'Sunday':'08/11/2019', 'nan':'08/12/2019'}
# talks master schedule
all_filenames = [n for n in glob.glob('schedule_talks_*.csv')]
# combine all files in the list
combined_csv = pd.concat([pd.read_csv(f) for f in all_filenames ])
dates = []
for val in combined_csv['day']:
    dates.append(days2Dates[str(val)])
combined_csv['date'] = dates
    
# aort by day and time
sort = combined_csv.sort_values(['date','time'])
#export to csv
sort.to_csv( "combined_schedule_talks.csv", index=False, encoding='utf-8-sig')


# workshops master schedule
all_filenames = [n for n in glob.glob('schedule_workshops_*.csv')]
# combine all files in the list
combined_csv = pd.concat([pd.read_csv(f) for f in all_filenames ])
dates = []
for val in combined_csv['day']:
    dates.append(days2Dates[str(val)])
combined_csv['date'] = dates
    
# aort by day and time
sort = combined_csv.sort_values(['date','time'])
#export to csv
sort.to_csv( "combined_schedule_workshops.csv", index=False, encoding='utf-8-sig')