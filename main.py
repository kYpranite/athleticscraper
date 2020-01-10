from IPython import get_ipython #Remove on release
get_ipython().magic('reset -sf')

# TODO: ADD DEBUG BUTTON

import tkinter as tk
from tkinter import ttk
import bs4 as bs
import requests
import re
import os
import lxml
from tkinter.scrolledtext import ScrolledText



placeCheck = None


def fileTypeCheck():
    global group
    
    fileType = int(fileVar.get())

    if fileType == 1:
        group = 'i'
    elif fileType == 2:
        group = 'g'
    


def varId(sId):
    global schoolId
    
    try:
        schoolId = int(sId)
        printLog("School ID: " + str(schoolId) + " successfully saved!")
    except ValueError:
        tk.messagebox.showerror(title='Error', message= 'Please enter an integer')

def placeId():
    global placeCheck
    print ("PlaceID is working")
    placeInput = str(placeVar.get())
    if placeInput == '0':
        placeCheck = 'f'
    elif placeInput == '1':
        placeCheck = 't'


def fetchGuard():
    try:
        fetchAthlete("https://www.athletic.net/CrossCountry/School.aspx?SchoolID=" + str(schoolId))
    except NameError:
        tk.messagebox.showerror(title='Error', message= 'Please save the School ID before grabbing')
        
def exportGuard():
    try:
        exportData("https://www.athletic.net/CrossCountry/School.aspx?SchoolID="+str(schoolId))       
    except:
        tk.messagebox.showerror(title='Error', message= 'Error: Please save a valid school ID, select individual or group in the configuration settings, and grab athletes before exporting data ')


        

def printLog(text):
    log.configure(state = 'normal')
    log.insert('insert', text+"\n")
    log.configure(state = 'disabled')
    log.see(tk.END)
    
def printInstructions(text):
    instructions.configure(state = 'normal')
    instructions.insert('insert', text+"\n")
    instructions.configure(state = 'disabled')
    instructions.see(tk.END)

def mainUI():
    global root, log, fileVar, placeVar
    HEIGHT = 700
    WIDTH = 950

    root = tk.Tk()
    root.title("Athletic.net Scraper")
    fileVar = tk.IntVar()
    placeVar = tk.IntVar()



    canvas = tk.Canvas (root, height = HEIGHT, width = WIDTH)
    canvas.pack()
    title = tk.Label(root, text = "Athletic Scraper", font = ('Roboto', 20, 'underline'))
    title.place(relx=0.04, rely=-0.05, relwidth = 0.2, relheight=0.2)

    # -- Log Window

    logFrame = tk.Frame(root, bg = 'white', highlightbackground="black", highlightthickness=1)
    logFrame.place(relx=0.05, rely=0.12, relwidth = 0.62, relheight = 0.62)



    log = ScrolledText(logFrame, wrap = 'word', bg = '#cdcdcd', state = 'disabled')
    log.place(relx = 0.03, rely=0.08, relwidth = 0.95, relheight = 0.8)
    logTitle = tk.Label(logFrame, bg = 'white', text = "Log", font = ('roboto', 12, 'bold', 'underline'))
    logTitle.place(relwidth = 0.07, relheight = 0.05, relx = 0.04, rely= 0.01)




     # -- Configuration Settings

    configFrame = tk.Frame(root, bg = 'white', highlightbackground="black", highlightthickness=1)
    configFrame.place(relx=0.7, rely = 0.12, relwidth = 0.28, relheight = 0.6)

    configTitle = tk.Label(configFrame, bg ='white', text = "Configuration", font = ('roboto', 15, 'underline'))
    configTitle.place(relx=0.2, rely = 0.05, relwidth = 0.6, relheight = 0.1 )

    configIdLabel = tk.Label(configFrame, bg ='white', text = "School ID:", font = ('roboto', 12, 'bold'))
    configIdLabel.place(relx=0.07, rely = 0.19)

    configId = tk.Entry(configFrame, bg = 'white')
    configId.place(relx=0.4, rely = 0.2)

    configPlace = tk.Checkbutton(configFrame, variable = placeVar, bg = 'white', text = 'Enable Placing?', font = ('roboto', 12, 'bold'))
    configPlace.place(relx=0.1, rely = 0.8)

    saveId = tk.Button(configFrame ,font = ('roboto', 12, 'bold'), bg = 'white', text = 'Save ID', command = lambda: varId(configId.get()))
    saveId.place(relx=0.3, rely = 0.27, relwidth = 0.3, relheight = 0.08)

    #Individual vs Group Selector
    configSelector = tk.Frame(configFrame, bg = 'white', highlightbackground="black", highlightthickness=1)
    configSelector.place(relx=0.02, rely = 0.4, relwidth = 0.96, relheight = 0.3)

    configIndividual = tk.Radiobutton(configSelector, variable = fileVar, value = 1, bg = 'white', text = 'Individuals', font = ('roboto', 12, 'bold'))
    configIndividual.place(relx=0.1, rely= 0.1)
    configGroup = tk.Radiobutton(configSelector, variable = fileVar, value = 2, bg = 'white', text = 'Group', font = ('roboto', 12, 'bold'))
    configGroup.place(relx=0.1, rely= 0.5)



    #-- Bottom Buttons --
    controlFrame = tk.Frame(root, bg = 'white', highlightbackground="black", highlightthickness=1)
    controlFrame.place(relx = 0.05, rely = 0.77, relwidth = 0.62, relheight = 0.2)
    getAthletes = tk.Button(controlFrame, command = lambda: fetchGuard() , text = "Grab Athletes", bg = '#add8e6', font = ('roboto', 12, 'bold'))
    getAthletes.place(relx = 0.1, rely= 0.2, relwidth = 0.3, relheight= 0.2)

    exportDataButton = tk.Button(controlFrame, command = lambda: [fileTypeCheck(), placeId(), exportGuard()] ,  text = "Export Data", bg = '#add8e6', font = ('roboto', 12, 'bold'))
    exportDataButton.place(relx = 0.6, rely= 0.2, relwidth = 0.3, relheight= 0.2)

    #-- Help Settings --

    helpFrame = tk.Frame(root, bg = 'white', highlightbackground="black", highlightthickness=1)
    helpFrame.place(relx = 0.7, rely=0.77, relwidth = 0.28, relheight = 0.2)

    helpButton = tk.Button(helpFrame, text = "Help", command = lambda: helpWindow(), bg = '#add8e6', font = ('roboto', 12, 'bold'))
    helpButton.place(relx = 0.27, rely=0.2, relwidth = 0.5, relheight = 0.2)
    faqButton = tk.Button(helpFrame, text = "FAQ", bg = '#add8e6', font = ('roboto', 12, 'bold'))
    faqButton.place(relx = 0.27, rely=0.6, relwidth = 0.5, relheight = 0.2)



    root.mainloop()

def helpWindow():
    global instructions
    window = tk.Tk()
    window.geometry('600x700')
    

    
    mainFrame = tk.Frame(window, bg = 'white')
    mainFrame.place(relx = 0, rely= 0, relwidth = 1, relheight = 1)
    
    configSettingTitle = tk.Label(mainFrame, text = 'Configuration Settings', bg = 'white', font = ('roboto', 15))
    configSettingTitle.place(relx = 0.07, rely= 0.07)
    
#    schoolIdHelp = tk.Label(mainFrame, text = "How to find and use a School ID:", bg = 'white', font = ('roboto', 12, 'bold'))
#    schoolIdHelp.place(relx = 0.1, rely = 0.12)
    
    helpTitle = tk.Label(mainFrame, text = 'Help', bg = 'white', font = ('roboto', 18, 'underline', 'bold'))
    helpTitle.pack()
    
    
#    schoolIdInstruction = tk.Message(mainFrame, text = "1. Go a school's athletic.net page (For example: https://www.athletic.net/CrossCountry/School.aspx?SchoolID=1964)\r\n2. Look at the section labeled 'SchoolID=' at the end of the link (In the previous example's case: SchoolID=1964). That number is your school ID\r\n3. Insert that number into the 'School ID' box inside configuration settings and press 'Save ID'. If done right, there will be a 'Success' message inside the log.", width = 500 ,bg = 'white', font = ('roboto', 12))
#    schoolIdInstruction.place(relx = 0.1, rely = 0.17)
#    
#    indVsGroup = tk.Label(mainFrame, text = "Individual vs. Group:", bg = 'white', font = ('roboto', 12, 'bold'))
#    indVsGroup.place(relx=0.1, rely=0.45)
#    
#    indVsGroupInstruction = tk.Message(mainFrame, text = "Individual: Choosing the individual option will export seperate files for each person. For example, let's say John Doe and Jane Doe are running in a team. Choosing the individual option will result in 2 text files, johndoe.txt and janedoe.txt \r\nGroup: Selecting the group option will export all times and information into a single text file. For example, if again, John Doe and Jane Doe were running in a team, choosing the group option would result in a file called anonymoushighschool.txt with both John and Jane's times inside.", width = 500, bg = 'white', font = ('roboto', 12))
#    indVsGroupInstruction.place(relx=0.1, rely=0.5)
    instructions = ScrolledText(mainFrame, wrap = 'word', bg = 'white', state = 'disabled')
    instructions.place(relx=0.01, rely = 0.15)
    printInstructions('How to find and use a School ID:')
    window.mainloop()


#############################################

debug = False


def grabPlace(result, nTitle):
    totalPlace = 1
    runnerPlace = 1
    sauce = requests.get(result).text

    scrapedName = re.findall(r'DivID\":(\d*)', sauce)

    uneditName = re.findall(r'(?<=DivName\"\:\")(.*)(?=\"},\"meet\")', sauce)
    uneditName = uneditName[0]
    filteredName = re.findall(r'\d \w* (.*)(?=\",\"Distance)',uneditName)

    res = []


    meetId = re.findall(r'eetID*\":(\d*)', sauce)
    runnerPlace = re.search(r'Place\":(\d*)', sauce)
    runnerPlace = runnerPlace.group(1)

    for i in range(0,len(meetId)):
        newSauce = requests.get("https://www.athletic.net/CrossCountry/meet/"+meetId[i]+"/results").text
        newSoup = bs.BeautifulSoup(newSauce,'lxml')
        root.update()
        if (newSoup.title.text == nTitle):

            for c in range(0, len(scrapedName)):
                root.update()
                newerSauce = requests.get("https://www.athletic.net/CrossCountry/meet/"+meetId[i]+"/results/"+scrapedName[c]).text
                newerSoup = bs.BeautifulSoup(newerSauce, 'lxml')
                filteredTitle = newerSoup.title.text
                filteredTitle = re.findall(r'(?<=-) (.*) (?=Results)', filteredTitle)
                newFilteredTitle = ''.join(filteredTitle)

                if (newFilteredTitle == filteredName[0]):
                    place = re.findall(r'Place\":(\d*)', newerSauce)
                    try:
                        [res.append(int(x)) for x in place if x not in res]
                        res.sort()
                        totalPlace = res[-1]
                    except:
                        totalPlace = 'No Place'


    try:
        totalPlace = int(totalPlace)
        runnerPlace = int(runnerPlace)
    
        percentile = runnerPlace/totalPlace
        percentile = percentile*100
        percentile = 100-percentile
        percentile = round(percentile, 2)
        return (str(runnerPlace)+"/"+str(totalPlace)+" ("+str(percentile) + "% Percentile)")
    except: 
        return 'No Place'


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
   printLog("Currently processing: " + meetGet[0])

   if (debug == True):
       printLog("Time: " + exactTimeGet)
       printLog("Date: "+ dateGet)
       printLog("Place and Exact Time: " + newMeetGet)

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


def fetchAthlete(schoolId):
   global namelist, idMatch


   namelist = []
   sauce = requests.get(schoolId).text
   soupId = bs.BeautifulSoup(sauce, 'lxml')
   script = str(soupId.find_all('script'))
   idMatch = re.findall(r'\"ID\":(\d\d\d\d\d\d\d\d),', script)
   for i in range(0, int(len(idMatch))-1):
   #for i in range(0, 20):
       root.update()
       athlete = requests.get('https://www.athletic.net/CrossCountry/Athlete.aspx?AID=' + str(idMatch[i])).text
       soupAt = bs.BeautifulSoup(athlete, 'lxml')
       name = soupAt.title.text
       namelist.append(name)
       namelist = [x.replace("\r\n","") for x in namelist]
       namelist = [c.replace("\t","") for c in namelist]
       namelist = [y.replace(" - CA Cross Country Bio","") for y in namelist]
       printLog(str(i+1) + ". Currently grabbing: "+name)
   print(namelist)
   if (namelist):
       printLog('Successfully Grabbed! Try to export data now')
   else:
       tk.messagebox.showerror(title='Error', message= 'Please insert a valid school ID')




def exportData(school):
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

    doc = open(schoolName[0] + ".txt", "w+")
    doc.write("Times | Pace | Date | Meet \r\n " )
    print (idMatch)
    #for i in range (0,3):
    for i in range (0,int(len(idMatch))-1):

      doc.write(namelist[i] + "|" + idMatch[i]+ "\r\n")
      printLog("________________________")
      printLog("Processing: "+ namelist[i])
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
        grabInfo(title)
        varMeetGet = meetGet[0]
        varMeetGet = varMeetGet[1:-1]
        if (placeCheck == 't' ):
            exportPlacement[0] = grabPlace('https://athletic.net' + str(filteredResults[i]), "\r\n\t"+varMeetGet+" - Cross Country Meet\r\n")
        try:
           timeForPace = exactTimeGet[0]
           pace[0] = grabPace(timeForPace)
        except:
            pass

        timeMeet[0] = newMeetGet
        if (placeCheck == 't'):
            doc.write('| '.join(roughTimeGet+pace+dateGet+timeMeet+empty+empty+empty+exportPlacement))
            doc.write("\r\n")
        else:
            doc.write('| '.join(roughTimeGet+pace+dateGet+timeMeet))
            doc.write("\r\n")
        root.update()
    printLog("\r\n")
    printLog("Succesfully exported data! Please check: " + cwd + " for the location of the text files" )
 elif group == 'i':

    try:
       os.mkdir(path)
    except:
       pass

    #for i in range (0,3):
    for i in range (0,int(len(idMatch))-1):
      printLog("________________________")
      printLog("Processing: "+ namelist[i])
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
        
        grabInfo(title)
        varMeetGet = meetGet[0]
        varMeetGet = varMeetGet[1:-1]
        if (placeCheck == "t"):
            exportPlacement[0] = grabPlace('https://athletic.net' + str(filteredResults[i]), "\r\n\t"+varMeetGet+" - Cross Country Meet\r\n")
        try:
           timeForPace = exactTimeGet[0]
           pace[0] = grabPace(timeForPace)
        except:
            pass

        timeMeet[0] = newMeetGet
        if (placeCheck == "t"):
            doc.write('| '.join(roughTimeGet+pace+dateGet+timeMeet+empty+empty+empty+exportPlacement))
            doc.write("\r\n")
        else:
            doc.write('| '.join(roughTimeGet+pace+dateGet+timeMeet))
            doc.write("\r\n")
        root.update()
    printLog("\r\n")
    printLog("Succesfully exported data! Please check: " + path + " for the location of the text files" )


#while True:
# print ("What school would you like to get results from?")
# print ("Insert school ID (athletic.net/CrossCountry/School.aspx?SchoolID=ThisIsTheID)")
# school = input()
# school = "https://www.athletic.net/CrossCountry/School.aspx?SchoolID=" + str(school)
# print ("Type 'g' for group or 'i' for individual")
# print ("Group (All stats in one file) or individual (All athletes get their own .txt file)?")
# group = input()
# print ("Enable placing? Will make process 2 hours longer! Type 't' to enable and 'f' to disable")
# placeCheck = input()
# fetchAthlete()
# exportData()

mainUI()

