# Tiger Inn Alumni Web Scraper

to use:
- download the correct chromedriver for your computer 
  - https://chromedriver.chromium.org/downloads
  - put the `chromedriver.exe` file in the same folder as `webScraper.py`
- run `python3 webScrape.py` from terminal
- enter the class year of which you wish to collect the information
- Chrome will open. Log in to your Princeton NetId
- returns a .csv of found information: Name (first, last), class, email, and major
  - 'nd' if no data found
  
TigerNet limits the number of pageviews per NetID per day, so this limits the search by class
- if the search runs out of pageviews, it returns the CSV with the last row 'LIMITED' 
  
try searching the class of 1890...
