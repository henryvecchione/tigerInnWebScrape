# Tiger Inn Alumni Web Scraper

requirements:
- python 3
- selenium package

to install: run `pip install -r requirements.txt`

to use:
- download the correct chromedriver for your computer and version of Chrome (the one in this repo is MacOS 64 bit)
  - https://chromedriver.chromium.org/downloads
  - put the `chromedriver.exe` file in the same folder as `webScraper.py`
- run `python3 webScrape.py` from terminal
- enter the class year of which you wish to collect the information
- Chrome will open. Log in to your Princeton NetId
- Don't interact with the Chrome window after logging in, the browser will execute the search and begin iterating through profiles
  - The names being scraped will start printing in the terminal if the software is working. 
- when finished, the program will exit and create a .csv of found information: Name (first, last), class, email, and major
  - this file is in the same folder as `webScrape.py` 
  - 'nd' if no data found
  
TigerNet limits the number of pageviews per NetID per day, so this limits the search by class
- if the search runs out of pageviews, it returns the CSV with the last row 'LIMITED' 
  
try searching the class of 1890...
