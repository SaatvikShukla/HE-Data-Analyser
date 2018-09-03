# -*- coding: utf-8 -*-
"""
Saatvik Shukla
31 August 2018

Data filtering script to target cities/country/etc
"""

import pandas as pd
from geopy.geocoders import Nominatim

geolocator = Nominatim(user_agent="HackerearthDataAnalyser", timeout=5)

# North America
targetCountries = ["Antigua and Barbuda", "Bahamas", "Barbados", "Belize", "Canada", "Costa Rica", "Cuba", "Dominica", "Dominican Republic", "El Salvador", "Grenada", "Guatemala", "Haiti", "Honduras", "Jamaica", "Mexico", "Nicaragua", "Panama", "Saint Kitts and Nevis", "Saint Lucia", "Saint Vincent and the Grenadines", "Trinidad and Tobago", "USA"]
targetFile = "bigdata.xls"

def printIntro():
    print("===============")
    print(" Data Analyser")
    print("===============")
    print("TargetFile: ", targetFile)
    print("Targetting: North America\n\n")

def categorizer(location, index, row, varStatus):
    """ Takes geolocator location object, TargetRow
        Classifies and drop the rows not required based ono targetCountries
    """
    if(varStatus == 0):
        location = location.address.split(",")
        if(location[-1].strip() in targetCountries):
            print(index, "yes ",location)
        else:
            targetExcel.drop(index, inplace=True)
            print(index, "no  ",location)
    else:
        print("Could not deciper location, Brutality Mode Enabled.")
        if(location[-1].strip() in targetCountries):
            print(index, "yes ",location)
        else:
            targetExcel.drop(index, inplace=True)
            print(index, "no  ",location)

printIntro()
targetExcel = pd.read_excel(targetFile, header=None, skiprows = 1)
targetExcel.columns = ['Name','Email','Graduation_Year','Contact','Resume','Profile_link','Experience','Colleges','Company','Designation','Location','Gender','Timestamp','Referral Code', 'Are you interested in working for ZS?']
NoneType = type(None)

for index, row in targetExcel.iterrows():
    location = geolocator.geocode(row['Location'])
    if (type(location) == NoneType):
        location = list(str(row['Location']).split(","))
        categorizer(location, index, row, 1)
        #targetExcel.drop(index, inplace=True)
    else:
        categorizer(location, index, row, 0)
        
            
targetExcel = (targetExcel.reset_index())
writer = pd.ExcelWriter('output.xlsx')
targetExcel.to_excel(writer,'Sheet1')
writer.save()