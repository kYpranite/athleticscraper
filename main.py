import bs4 as bs
import lxml
import requests
import re
import os




debug = True

def grabPlace(result, nTitle):
    totalPlace = 1
    runnerPlace = 1
    sauce = requests.get(result).text
    
    scrapedName = re.findall(r'DivID\":(\d*)', sauce)
    
    uneditName = re.findall(r'(?<=DivName\"\:\")(.*)(?=\"},\"meet\")', sauce)
    uneditName = uneditName[0]
    filteredName = re.findall(r'\d \w* (.*)(?=\",\"Distance)',uneditName)
    
    res = [] 


    meetId = re.findall(r'\"MeetID\":(\d*)', sauce)
    runnerPlace = re.search(r'Place\":(\d*)', sauce)
    runnerPlace = runnerPlace.group(1)
    
    for i in range(0,len(meetId)):
        newSauce = requests.get("https://www.athletic.net/CrossCountry/meet/"+meetId[i]+"/results").text
        newSoup = bs.BeautifulSoup(newSauce,'lxml')
    
        if (newSoup.title.text == nTitle):

            for c in range(0, len(scrapedName)):
                newerSauce = requests.get("https://www.athletic.net/CrossCountry/meet/"+meetId[i]+"/results/"+scrapedName[c]).text
                newerSoup = bs.BeautifulSoup(newerSauce, 'lxml')
                filteredTitle = newerSoup.title.text
                filteredTitle = re.findall(r'(?<=-) (.*) (?=Results)', filteredTitle)
                newFilteredTitle = ''.join(filteredTitle)

                if (newFilteredTitle == filteredName[0]):
                    place = re.findall(r'Place\":(\d*)', newerSauce)
                    [res.append(int(x)) for x in place if x not in res] 
                    res.sort()
                    totalPlace = res[-1]

                    
            
    totalPlace = int(totalPlace)
    runnerPlace = int(runnerPlace)
    
    percentile = runnerPlace/totalPlace
    percentile = percentile*100
    percentile = 100-percentile
    percentile = round(percentile, 2)
    return (str(runnerPlace)+"/"+str(totalPlace)+" ("+str(percentile) + "% Percentile)")


def grabInfo(info):
   global dateGet, yearGet, newMeetGet, schoolGet, roughTimeGet, exactTimeGet, meetGet

   roughTimeGet = re.findall(r'- (..:..)', info)
   exactTimeGet = re.findall(r'- (..:....)', info)
   dateGet = re.findall(r'- (... \d*, \d*)', info)
   yearGet = re.findall(r', (\d*)', info)
   if 'Miles' in info:
      meetGet = re.findall(r'(?<=Miles -)(.*)(?=- ... \d*, \d*)', info)
      try:
         newMeetGet= "(" + exactTimeGet[0] + " @ " + meetGet[0] + ")"
      except:
         newMeetGet = "No time"
      distanceGet = re.findall(r'(\d Miles)', info)
   elif 'Meters' in info:
      meetGet = re.findall(r'(?<=Meters -)(.*)(?=- ... \d*, \d*)', info)
      try:
         newMeetGet= "(" + exactTimeGet[0] + " @ " + meetGet[0] + ")"
      except:
         newMeetGet= "(No Time " + " @ " + meetGet[0] + ")"
      distanceGet = re.findall(r'(\d,\d* Meters)', info)
   if (debug == True):
     print ("----------")
     print (exactTimeGet)
     print ("----------")
     print (dateGet)
     print ("----------")
     print (yearGet)
     print ("----------")
     print (newMeetGet)
     print ("----------")
def grabPace(time):

   grabMinutes = re.findall(r'(\d*):', time)
   grabSeconds = re.findall(r':(\d*)', time)

   minutes = int(grabMinutes[0])
   seconds = int(grabSeconds[0])

   minuteSeconds = minutes*60
   totalSeconds = minuteSeconds+seconds

   paceSeconds = totalSeconds/3
   paceSeconds = round(paceSeconds)
   decimalPace = str(round(paceSeconds/60,2))


   decimalMinutes = re.findall(r'(\d*)\.', decimalPace)
   decimalSeconds = re.findall(r'\.(\d*)', decimalPace)
   decimalMinutes = str(decimalMinutes[0])
   decimalSeconds = int(decimalSeconds[0])



   minuteLength = len(grabMinutes)

   for i in range (0,minuteLength+1):
       decimalSeconds=decimalSeconds/10


   finalSeconds = decimalSeconds*60
   finalSeconds = round(finalSeconds)
   finalSeconds = str(finalSeconds)
   if (len(finalSeconds)==1):
       if (int(finalSeconds) < 6):
           finalSeconds = str(finalSeconds) + "0"
       else:
           finalSeconds = "0" + str(finalSeconds)
            

   pace = str(decimalMinutes) + ":" + str(finalSeconds)
   return (pace)


def fetchAthlete():
   global namelist, idMatch
   namelist = []
   sauce = requests.get(school).text
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
    
def exportData():
 global links, meetResult, filturedResults
 empty = [" "]

 schoolHtml = requests.get(school).text
 soup = bs.BeautifulSoup(schoolHtml, 'lxml')
 title = soup.title.text
 schoolName = re.findall(r'(.*) (?=Cross Country Statistics)', title)
 schoolName[0] = schoolName[0][1:]

 directory = schoolName[0] + " - " + "Individuals"
 cwd = os.getcwd()
 path = os.path.join(cwd, directory)

 if group == 'g':
    pace = ["x"]
    timeMeet = ['x']
    
    doc = open("info.txt", "w+")
    doc.write("Times | Pace | Date | Meet \r\n " )
    #for i in range (0,3):
    for i in range (0,int(len(idMatch))-1):
      
      doc.write(namelist[i] + "|" + idMatch[i]+ "\r\n")
      
      links = []
      meetResult = []

      exportPlacement = ['x']
      person = requests.get('https://www.athletic.net/CrossCountry/Athlete.aspx?AID=' + str(idMatch[i])).text
      yumSoup = bs.BeautifulSoup(person, 'lxml')
      for url in yumSoup.find_all('a'):
        links.append((url.get('href')))
      results = [s for s in links if "/result" in s]
      for s in results:
        if 'meet/' in s:
            meetResult.append(s)
      filteredResults = [x for x in results if x not in meetResult]
      filteredResults = list(set(filteredResults))
      for i in range (0, int(len(filteredResults))):
        pace = ['No Pace']
        meetTime = requests.get('https://athletic.net' + str(filteredResults[i])).text
        soupTime = bs.BeautifulSoup(meetTime, 'lxml')
        title = soupTime.title.text
        print (title)
        grabInfo(title)
        varMeetGet = meetGet[0]
        varMeetGet = varMeetGet[1:-1]
        if (placeCheck == 't' ):
            exportPlacement[0] = grabPlace('https://athletic.net' + str(filteredResults[i]), "\r\n\t"+varMeetGet+" - Cross Country Meet\r\n")
        try:
           timeForPace = exactTimeGet[0]
           pace[0] = grabPace(timeForPace)
        except:
           print (timeForPace)
           print (grabPace(timeForPace))
           print (pace)
           
        timeMeet[0] = newMeetGet
        if (placeCheck == 't'):
            doc.write('| '.join(roughTimeGet+pace+dateGet+timeMeet+empty+empty+empty+exportPlacement))
            doc.write("\r\n")
        else:
            doc.write('| '.join(roughTimeGet+pace+dateGet+timeMeet))
            doc.write("\r\n")

 elif group == 'i':
    
    try:
       os.mkdir(path)
    except:
       pass

    #for i in range (0,3):
    for i in range (0,int(len(idMatch))-1):
      doc = open(path + "\\" + namelist[i]+".txt", "w+")
      doc.write(namelist[i] + "|" + idMatch[i]+ "\r\n")
      doc.write("Times | Pace | Date | Meet and Exact Times | | | |Placing\r\n " )
      links = []
      meetResult = []
      timeMeet = ['x']
      exportPlacement = ['x']
      person = requests.get('https://www.athletic.net/CrossCountry/Athlete.aspx?AID=' + str(idMatch[i])).text
      yumSoup = bs.BeautifulSoup(person, 'lxml')
      for url in yumSoup.find_all('a'):
        links.append((url.get('href')))
      results = [s for s in links if "/result" in s]
      for s in results:
        if 'meet/' in s:
            meetResult.append(s)
      filteredResults = [x for x in results if x not in meetResult]
      filteredResults = list(set(filteredResults))
      for i in range (0, int(len(filteredResults))):
        pace = ['No Pace']
        meetTime = requests.get('https://athletic.net' + str(filteredResults[i])).text
        soupTime = bs.BeautifulSoup(meetTime, 'lxml')
        title = soupTime.title.text
        print (title)
        grabInfo(title)
        varMeetGet = meetGet[0]
        varMeetGet = varMeetGet[1:-1]
        if (placeCheck == "t"):
            exportPlacement[0] = grabPlace('https://athletic.net' + str(filteredResults[i]), "\r\n\t"+varMeetGet+" - Cross Country Meet\r\n")
        try:
           timeForPace = exactTimeGet[0]
           pace[0] = grabPace(timeForPace)
        except:
           print (timeForPace)
           print (grabPace(timeForPace))
           print (pace)
           
        timeMeet[0] = newMeetGet
        if (placeCheck == "t"):
            doc.write('| '.join(roughTimeGet+pace+dateGet+timeMeet+empty+empty+empty+exportPlacement))
            doc.write("\r\n")
        else:
            doc.write('| '.join(roughTimeGet+pace+dateGet+timeMeet))
            doc.write("\r\n")



while True:
 print ("What school would you like to get results from?")
 print ("Insert school ID (athletic.net/CrossCountry/School.aspx?SchoolID=ThisIsTheID)")
 school = input()
 school = "https://www.athletic.net/CrossCountry/School.aspx?SchoolID=" + str(school)
 print ("Type 'g' for group or 'i' for individual")
 print ("Group (All stats in one file) or individual (All athletes get their own .txt file)?")
 group = input()
 print ("Enable placing? Will make process 2 hours longer! Type 't' to enable and 'f' to disable")
 placeCheck = input()
 fetchAthlete()
 exportData()


