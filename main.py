# -*- coding: utf-8 -*-
"""
Saatvik Shukla
31 August 2018

Data filtering script to target cities/country/etc
"""

# North America
targetCountries = ["Antigua and Barbuda", "Bahamas", "Barbados", "Belize", "Canada", "Costa Rica", "Cuba", "Dominica", "Dominican Republic", "El Salvador", "Grenada", "Guatemala", "Haiti", "Honduras", "Jamaica", "Mexico", "Nicaragua", "Panama", "Saint Kitts and Nevis", "Saint Lucia", "Saint Vincent and the Grenadines", "Trinidad and Tobago", "USA"]

TARGET_FILE = "bigdata.xls"
NoneType = type(None)

import pandas as pd
from geopy.geocoders import Nominatim

geolocator = Nominatim(user_agent="HackerearthDataAnalyser", timeout=5)

def printIntro():
    print("===============")
    print(" Data Analyser")
    print("===============")
    print("TARGET_FILE: ", TARGET_FILE)
    print("Targetting: North America\n\n")

def loader():
    targetExcel = pd.read_excel(TARGET_FILE, header=None, skiprows = 1)
    targetExcel.columns = ['Name','Email','Graduation_Year','Contact','Resume','Profile_link','Experience','Colleges','Company','Designation','Location','Gender','Timestamp','Referral Code', 'Are you interested in working for ZS?']
    return targetExcel


def classifier(targetExcel, location, index, row):
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
        print("Could not deciper location, Brutality Mode Enabled.")
        classifier(targetExcel, location, index, row)

def bootstrap(targetExcel):
    for index, row in targetExcel.iterrows():
        location = geolocator.geocode(row['Location'])
        if (type(location) == NoneType):
            location = list(str(row['Location']).split(","))
            categorizer(targetExcel, location, index, row, 1)
        else:
            categorizer(targetExcel, location, index, row, 0)
    return targetExcel

def save(targetExcel):
    targetExcel = (targetExcel.reset_index())
    writer = pd.ExcelWriter('output.xlsx')
    targetExcel.to_excel(writer,'Sheet1')
    writer.save()

def init():
    printIntro()
    targetExcel = loader()
    targetExcel = bootstrap(targetExcel)
    save(targetExcel)
    
init() 
