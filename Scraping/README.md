# DC 27 Event Schedule Scraping

These are a collection of web scraping scipts to assist in planning ones DEFCON activites. The output of these scripts is a csv file stored in the same directory as the script. 

scrapeTalks\*.py:
These scripts currently attempt to parse out the title, day, time, track, duration, tags (e.g. demo/tool or village), speaker(s), abstract, and speaker(s) bio if available.

scrapeWorkshops\*.py:
These scipts currently attempt to parese out the title, day, time, track, duration, tags (e.g. workshop), speaker(s), abstract, speaker(s) bio, skill level, prerequisites, materials, maximum number of students, and registration URL (if any).

## Current Work
Main, Packet Hacking Village (PHV), Blue Team Village (BTV)

## To Do
Wireless Village, IoT Village, Skytalks, Crypto & Privacy Village, BioHacking Village, CarHacking Village, ICS Village, Lockpick Village, AI Village, Blockchain Village, Monero Village, Recon Village, Red Team, Village, Ethics Village, Social Engineering Village, Voting Hacking Village, Data Duplication Village, r00tz, Aviation Hacking Village, Drone Warz, Hack the Sea, Hardware Hacking Village, Rogues Village, Tamper Evident Village, Cloud Village, VX (Chip-off) Village, Ham Radio Village, AppSec Village

## Useful References
http://defcon.outel.org/

## Prerequisites
Python3 and pip3

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install the following:

```bash
pip3 install BeautifulSoup4
pip3 install requests
pip3 install python-dateutil
```

## Usage
```bash
python3 scrapeTalksMain.py
python3 scrapeTalksPHV.py
python3 scrapeWorkshopsMain.py
```

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

## License
[MIT](https://choosealicense.com/licenses/mit/)
