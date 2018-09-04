# -*- coding: utf-8 -*-
"""
Saatvik Shukla
31 August 2018

Data filtering script to target cities/country/etc
"""

# North America
targetCountries = ["Antigua and Barbuda", "Bahamas", "Barbados", "Belize", "Canada", "Costa Rica", "Cuba", "Dominica", "Dominican Republic", "El Salvador", "Grenada", "Guatemala", "Haiti", "Honduras", "Jamaica", "Mexico", "Nicaragua", "Panama", "Saint Kitts and Nevis", "Saint Lucia", "Saint Vincent and the Grenadines", "Trinidad and Tobago", "USA"]

TARGET_FILE = ["ZS-BigData-Challenge-Summer-2018-result.xls", "ZS-BigData-Challenge-Summer-2018-registered-list.xls"]

import pandas as pd
from geopy.geocoders import Nominatim
import datetime
import time
ts = time.time()

geolocator = Nominatim(user_agent="HackerearthDataAnalyser", timeout=5)
loc = 2
NoneType = type(None)
MODE = "A"
def printIntro():
    print("===============")
    print(" Data Analyser")
    print("===============")
    print("TARGET_FILE: ", TARGET_FILE[:])
    print("Targetting: North America\n\n")

def loader():
    """ Loads excel files and handles exec
    """
    for index, i in enumerate(TARGET_FILE):
        if(index == 1):
            MODE = "B"
        else:
            MODE = "A"
        print("running: ",i," with MODE",MODE)
        targetExcel = pd.read_excel(i, header=None)
        header = targetExcel.iloc[0]
        targetExcel = targetExcel[1:]
        targetExcel.rename(columns = header)
        bootstrap(targetExcel, MODE)


def classifier(targetExcel, location, index, row):
    """ takes rows and drop rows from the excel that 
        are not in line with the requirements
    """
    if(location[-1].strip() in targetCountries):
        print(index, "yes ",location)
    else:
        targetExcel.drop(index, inplace=True)
        print(index, "no  ",location)

def categorizer(targetExcel, location, index, row, varStatus):
    """ Takes geolocator location object, TargetRow
        Classifies and drop the rows not required based ono targetCountries
    """
    if(varStatus == 0):
        location = location.address.split(",")
        classifier(targetExcel, location, index, row)
    else:
        print("Could not deciper location automatically.")
        classifier(targetExcel, location, index, row)

def bootstrap(targetExcel, MODE):
    """ Takes the excel file, iterate rows and cals categorizer
    """
    if(MODE == "A"):
        loc = 2
    elif(MODE == "B"):
        loc = 10
    for index, row in targetExcel.iterrows():
        location = geolocator.geocode(row[loc])
        if (type(location) == NoneType):
            location = list(str(row[loc]).split(","))
            categorizer(targetExcel, location, index, row, 1)
        else:
            categorizer(targetExcel, location, index, row, 0)
    save(targetExcel)

def save(targetExcel):
    """ Takes the excel and writes it to the filesystem
    """
    st = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d-%H%M')
    targetExcel = (targetExcel.reset_index())
    print(len(targetExcel.index)," people in total from TARGET LOCATION")
    writer = pd.ExcelWriter('output'+str(st)+'.xlsx')
    targetExcel.to_excel(writer,'Sheet1')
    writer.save()

def init():
    printIntro()
    loader()
    
    
init() 
