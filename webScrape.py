from selenium import webdriver
from selenium.webdriver.support import ui
from selenium.webdriver.common.by import By
import time
import csv
from datetime import date

import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)

def main():

  # CLI
  print('Tiger Inn Alumni Web Scraper')
  print("(c) 2022 Henry Vecchione '22 (hjv@)")
  print('Warning: Due to rate limiting on the TigerNet service, \n a limited number of profiles can be scraped per NetID per day\n\n')
  yr = int(input('Enter the class year to search: '))
  if yr < 1930 or yr > date.today().year:
    print('Year must be after 1930 and before or equal to the current year')
    return
  print(f'Searching the class of {yr}')

  # attempt to open site
  web = webdriver.Chrome("/Users/henryvecchione/Desktop/Home/tiAlum/chromedriver.exe")
  web.get('https://tigernet.princeton.edu/s/1760/02-tigernet/20/interior.aspx?sid=1760&gid=2&pgid=6#/Search/Advanced')

  wait = ui.WebDriverWait(web, 10)

  def isLoaded(driver):
    return driver.find_element(By.TAG_NAME, "body") != None

  wait.until(isLoaded)

  # likely not logged in, so wait for user to log in with NetID
  while True:
    try:
      checkLogin = web.find_element(By.XPATH, '/html/body/form/div[3]/main/section/div/div/section/div[3]/div[1]/div/div[2]/h2')
      print('Login successful')
      break
    except:
      print('Select "Log in" in the browser and authenticate your NetID', end='\r')
      continue
  
  
  # once logged in, begin scraping loop
  years = range(yr, yr+1) # grad years -- just one for now since it's rate limiting
  for year in years:
    print(f'Year: {year}')
    # (1) get Advanced Search site
    web.get('https://tigernet.princeton.edu/s/1760/02-tigernet/20/interior.aspx?sid=1760&gid=2&pgid=6#/Search/Advanced')
    while True:
      try:
        # (2.1) select Activities field
        activitySelect = ui.Select(web.find_element(By.ID, 'mf_411')) 
        # (2.2) select Year field
        yearSelect = ui.Select(web.find_element(By.ID, "mf_882"))
        # (2.3) select Submit button
        submit = web.find_element(By.XPATH, '//*[@id="imod-view-content"]/section/div[3]/div[21]/button')
        break # once all are visible (i.e page has loaded)
      except:
        continue # if these throw, the page hasn't loaded yet
      
    # (3.1) select 'Tiger Inn' option
    activitySelect.select_by_value('string:TIN') # Tiger Inn select value
    # (3.2) select Year
    yearSelect.select_by_value(f'string:{year}') 
    # (3.3) submit form
    submit.click()

    url = web.current_url

    # (4) wait and get the number of results
    pageNo = 1
    numPages = 2
    while pageNo < int(numPages):
      newUrl = '/'.join(url.split('/')[:-1]) + '/' + str(pageNo) + '#gridStart'
      web.get(newUrl)
      print(f'Page{pageNo} of {numResults}')
      # get the number of results, calculate pages
      while True:
        try:
          numResults = web.find_element(By.XPATH, '/html/body/form/div[3]/main/section/div/div/section/div[3]/div[1]/div/div[2]/div[2]/p/strong').get_attribute('textContent')
          print(f'{numResults} members found in year {year}')
          numPages = int(numResults) // 20 + 1 
          break
        except:
          continue
      
      while True:
        #(5) iterate through results, pulling profile links
        links = []
        while True:
          try:
            # (5.1) get all alums on a page
            alums = web.find_elements(By.CLASS_NAME, 'imod-directory-member-more')
            # (5.2) for each alum on page, get the link to their profile
            for alum in alums:
              profile = alum.find_element(By.TAG_NAME, 'a')
              link = profile.get_attribute('href')
              links.append(link)
            break
          except Exception as e:
            continue


        # (6) Iterate through links for that page
        for link in links:
          # (6.1) visit site
          web.get(link)
          # (6.2) Get categories: personal, contact, education, career
          while True:
            try:
              _ = web.find_element(By.CSS_SELECTOR, '.imod-profile-step.ng-isolate-scope.imod-profile-step-opened')
              break
            except Exception as e:
              continue
          
          # get the 'categories' e.g contact info, career info, academic info
          categories = web.find_elements(By.CSS_SELECTOR, '.imod-profile-step.ng-isolate-scope.imod-profile-step-opened') + web.find_elements(By.CSS_SELECTOR, '.imod-profile-step.ng-isolate-scope.imod-profile-step-closed')
          # (6.3) get content 
          for c in categories:
            # get the fields
            fields = c.find_elements(By.CSS_SELECTOR, '.imod-profile-fields')
            for field in fields:
              # get the name and data 
              fieldNames = field.find_elements(By.CSS_SELECTOR, '.imod-profile-field-label.ng-binding.ng-scope')
              fieldData = field.find_elements(By.CSS_SELECTOR, '.imod-profile-field-data.ng-binding.ng-scope')
              for n, d in zip(fieldNames, fieldData):
                print(f'{n.get_attribute("textContent")} : {d.get_attribute("textContent")}')
          print('*--------------------*')
        break
      # go to next page
      pageNo += 1
    



if __name__ == "__main__":
  main()
