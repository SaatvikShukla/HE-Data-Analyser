# -*- coding: utf-8 -*-
"""
Saatvik Shukla
31 August 2018

Data filtering script to target cities/country/etc
"""

import pandas as pd
from geopy.geocoders import Nominatim

geolocator = Nominatim(user_agent="HackerearthDataAnalyser", timeout=5)

targetCountries = ["Antigua and Barbuda", "Bahamas", "Barbados", "Belize", "Canada", "Costa Rica", "Cuba", "Dominica", "Dominican Republic", "El Salvador", "Grenada", "Guatemala", "Haiti", "Honduras", "Jamaica", "Mexico", "Nicaragua", "Panama", "Saint Kitts and Nevis", "Saint Lucia", "Saint Vincent and the Grenadines", "Trinidad and Tobago", "USA"]

targetExcel = pd.read_excel("bigdata.xls", header=None, skiprows = 1)
targetExcel.columns = ['Name','Email','Graduation_Year','Contact','Resume','Profile_link','Experience','Colleges','Company','Designation','Location','Gender','Timestamp','Referral Code', 'Are you interested in working for ZS?']
NoneType = type(None)
count = 1
for index, row in targetExcel.iterrows():
    location = geolocator.geocode(row['Location'])
    if (type(location) == NoneType):
        print("========")
        print(count,location," is NoneType")
        print("========")
        targetExcel.drop(index, inplace=True)
        count = count +  1
        pass
    else:
        location = location.address.split(",")
        if(location[-1].strip() in targetCountries):
            print(count, "yes ",location)
            count = count +  1
        else:
            targetExcel.drop(index, inplace=True)
            print(count, "no  ",location)
            count = count +  1
            
targetExcel = (targetExcel)
writer = pd.ExcelWriter('output.xlsx')
targetExcel.to_excel(writer,'Sheet1')
writer.save()