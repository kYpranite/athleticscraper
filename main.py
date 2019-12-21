import bs4 as bs
import requests
import re
from tkinter import *
import os


#year = input("What year's times are you looking to grab? (2016, 2017, 2018, 2019)")

app = Tk()
app.title('Athletic.net Time Scraper')
app.geometry('700x450')
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
   for i in range(0, int(len(idMatch))-1):
   #for i in range(0, 20):
       athlete = requests.get('https://www.athletic.net/CrossCountry/Athlete.aspx?AID=' + str(idMatch[i])).text
       soupAt = bs.BeautifulSoup(athlete, 'lxml')
       name = soupAt.title.text
       namelist.append(name)
       namelist = [x.replace("\r\n","") for x in namelist]
       namelist = [c.replace("\t","") for c in namelist]
       namelist = [y.replace(" - CA Cross Country Bio","") for y in namelist]
       print (str(i+1) + name)
       print ("---------------")
       print (namelist)
 
def fetchTime():
 global links, meetResult, filturedResults
 directory = "Individuals"
 cwd = os.getcwd()
 path = os.path.join(cwd, directory)

 if (group == 'g'):
    doc = open("info.txt", "w+")
    doc.write("Times | Date | Meet \r\n " )
    #for i in range (0,3):
    for i in range (0,int(len(idMatch))-1):
      doc.write(namelist[i] + "|" + idMatch[i]+ "\r\n")
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
        doc.write('| '.join(timeGet+dateGet+meetGet))
        doc.write("\r\n")
    
 elif (group == 'i'):
    try:
       os.mkdir(path)
    except:
       pass
    #for i in range (0,3):
    for i in range (0,int(len(idMatch))-1):
      doc = open(path + "\\" + namelist[i]+".txt", "w+")
      #date = open(namelist[i]+ "- Dates.txt", "w+")
    
      doc.write(namelist[i] + "|" + idMatch[i]+ "\r\n")
      doc.write("Times | Date | Meet \r\n " )
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
        doc.write('| '.join(timeGet+dateGet+meetGet))
        doc.write("\r\n")
      doc.write("\r\n")

    
      
while True:
 print ("Type 'g' for group or 'i' for individual")
 group = input("Single (All stats in one file) or seperate text documents (All athletes get their own .txt file)?")
 
 fetchAthlete()
 fetchTime()
    
 

