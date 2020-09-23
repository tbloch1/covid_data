import requests
import numpy as np
import pandas as pd
import datetime as dt
import xlrd
from xlsx_to_csv import csv_from_excel


def case_data():
  dailycases = requests.get('https://opendata.ecdc.europa.eu/covid19/casedistribution/csv',
                            headers={"User-Agent":"Mozilla/5.0"})

  if dailycases.status_code == 200:
      with open('data/dailycases.csv', 'wb') as f:
          f.write(dailycases.content)
          

def test_data():
  testingdata = requests.get('https://www.ecdc.europa.eu/sites/default/files/documents/weekly_testing_data_EUEEAUK_2020-09-16.xlsx',
                             headers={"User-Agent":"Mozilla/5.0"})

  if testingdata.status_code == 200:
      with open('data/testingdata.xlsx', 'wb') as f:
          f.write(testingdata.content)

  wb = xlrd.open_workbook('data/testingdata.xlsx')
  print(wb.sheet_names())

  csv_from_excel('data/testingdata','Sheet1')


def hospital_data():
  ndays = 0

  while not pd.isna(ndays):
    date = dt.date.today() - ndays*dt.timedelta(days=1)

    hospitaldata = requests.get('https://www.ecdc.europa.eu/sites/default/files/documents/hosp_icu_all_data_'+str(date)+'.xlsx',
                                headers={"User-Agent":"Mozilla/5.0"})

    if hospitaldata.status_code == 200:
        ndays = np.nan
        with open('data/hospitaldata.xlsx', 'wb') as f:
            f.write(hospitaldata.content)
    else:
      ndays = ndays+1

  wb = xlrd.open_workbook('data/hospitaldata.xlsx')
  print(wb.sheet_names())

  csv_from_excel('data/hospitaldata','Sheet1')
  

def death_data():
  year = dt.date.today().isocalendar()[0]
  week = dt.date.today().isocalendar()[1]

  while not np.isnan(week):
    deathdata = requests.get('https://www.ons.gov.uk/file?uri=/peoplepopulationandcommunity/healthandsocialcare/causesofdeath/datasets/deathregistrationsandoccurrencesbylocalauthorityandhealthboard/'+str(year)+'/lahbtablesweek'+str(week)+'.xlsx',
                             headers={"User-Agent":"Mozilla/5.0"})

    if deathdata.status_code == 200:
        week = np.nan
        with open('data/deathdata.xlsx', 'wb') as f:
            f.write(deathdata.content)
    else:
      print(week)
      week = week - 1
  wb = xlrd.open_workbook('data/deathdata.xlsx')
  print(wb.sheet_names())

  csv_from_excel('data/deathdata','Registrations - All data')
  
  
def uk_coord_data():
  coords = requests.get('http://geoportal1-ons.opendata.arcgis.com/datasets/fab4feab211c4899b602ecfbfbc420a3_2.csv?outSR={%22latestWkid%22:4326,%22wkid%22:4326}',
                        headers={"User-Agent":"Mozilla/5.0"})

  if coords.status_code == 200:
      with open('data/coords.csv', 'wb') as f:
          f.write(coords.content)
          
          
def uk_population_data():
  populations = requests.get('https://www.ons.gov.uk/file?uri=%2fpeoplepopulationandcommunity%2fpopulationandmigration%2fpopulationestimates%2fdatasets%2fpopulationestimatesforukenglandandwalesscotlandandnorthernireland%2fmid2019april2020localauthoritydistrictcodes/ukmidyearestimates20192020ladcodes.xls',
                             headers={"User-Agent":"Mozilla/5.0"})

  with open('data/populations.xlsx', 'wb') as f:
    f.write(populations.content)

  wb = xlrd.open_workbook('data/populations.xlsx')
  print(wb.sheet_names())

  csv_from_excel('data/populations','MYE2 - Persons')


def uk_map_data():
  ukmap = requests.get('https://opendata.arcgis.com/datasets/cf8aa4a9e6ee494bbb243462ecb388ee_0.geojson',
                       headers={"User-Agent":"Mozilla/5.0"})

  if ukmap.status_code == 200:
      with open('data/ukmap.geojson', 'wb') as f:
          f.write(ukmap.content)
          
          
def world_pop_data():
  globalpop = requests.get('https://population.un.org/wpp/Download/Files/1_Indicators%20(Standard)/CSV_FILES/WPP2019_TotalPopulationBySex.csv',
                           headers={"User-Agent":"Mozilla/5.0"})

  if globalpop.status_code == 200:
      with open('data/globalpop.csv', 'wb') as f:
          f.write(globalpop.content)


def authority_to_county():
  counties = requests.get('https://opendata.arcgis.com/datasets/0fa948d8a59d4ba6a46dce9aa32f3513_0.csv',
                          headers={"User-Agent":"Mozilla/5.0"})
  
  if counties.status_code == 200:
      with open('data/counties.csv', 'wb') as f:
          f.write(counties.content)
