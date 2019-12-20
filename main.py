import bs4 as bs
import requests 
import re

#year = input("What year's times are you looking to grab? (2016, 2017, 2018, 2019)")

debug = True
empty = [" "]
  
def grabInfo(info):
    global timeGet, dateGet, yearGet, meetGet
    
    timeGet = re.findall(r'- (..:....)', info)
    dateGet = re.findall(r'- (... \d*, \d*)', info)
    yearGet = re.findall(r', (\d*)', info)
    meetGet = re.findall(r'(?<=Miles -)(.*)(?=- ... \d*, \d*)', info)
    
    if (debug == True):
      print ("----------")
      print (timeGet)
      print ("----------")
      print (dateGet)
      print ("----------")
      print (yearGet)
      print ("----------")
      print (meetGet)
      print ("----------")

      
        
def fetchAthlete():
    global namelist, idMatch
    namelist = []
    sauce = requests.get('https://www.athletic.net/CrossCountry/School.aspx?SchoolID=1964').text #replace this link with whatever school link you want
    soupId = bs.BeautifulSoup(sauce, 'lxml')
    script = str(soupId.find_all('script'))
    idMatch = re.findall(r'\"ID\":(\d\d\d\d\d\d\d\d),', script)
    #for i in range(0, int(len(idMatch))-1):
    for i in range(0, 20):
        athlete = requests.get('https://www.athletic.net/CrossCountry/Athlete.aspx?AID=' + str(idMatch[i])).text
        soupAt = bs.BeautifulSoup(athlete, 'lxml')
        name = soupAt.title.text
        namelist.append(name)
        namelist = [x.replace("\r\n","") for x in namelist]
        namelist = [c.replace("\t","") for c in namelist]
        namelist = [y.replace(" - CA Cross Country Bio","") for y in namelist]
        print (str(i) + name)
        print ("---------------")
        print (namelist)

def fetchTime():
  global links, meetResult, filturedResults
  #f = open("info.txt", "w+")
  for i in range (0,5):
  #for i in range (0,int(len(idMatch))-1):
    number = str(i)
    test = open(namelist[i]+".txt", "w+")
    test.write(namelist[i] + " " + idMatch[i]+ "\r\n")
    #f.write(namelist[i]+"\r\n")
    links = []
    meetResult = []
    person = requests.get('https://www.athletic.net/CrossCountry/Athlete.aspx?AID=' + str(idMatch[i])).text 
    yumSoup = bs.BeautifulSoup(person, 'lxml')
    for url in yumSoup.find_all('a'):
      links.append((url.get('href')))
    results = [s for s in links if "/result" in s]
    for s in results:
      if ('meet/' in s):
          meetResult.append(s)
    filteredResults = [x for x in results if x not in meetResult]
    filteredResults = list(set(filteredResults))
    for i in range (0, int(len(filteredResults))-1):
      meetTime = requests.get('https://athletic.net' + str(filteredResults[i])).text
      soupTime = bs.BeautifulSoup(meetTime, 'lxml')
      title = soupTime.title.text
      print (title)
      grabInfo(title)
   
      test.write('| '.join(meetGet+empty+dateGet+timeGet))
      test.write("\r\n")
      
      #f.write('| '.join(meetGet+dateGet+timeGet))
      #f.write("\r\n")
      
        
while True:
  input("Press enter to start")
  fetchAthlete()
  fetchTime()
              

