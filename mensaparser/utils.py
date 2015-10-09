__author__ = 'marcman'

import requests, json, datetime
from bs4 import BeautifulSoup


def get_api_as_json():
    URL = 'http://www.studentenwerk-potsdam.de/speiseplan/'
    r = requests.get(URL)
    soup = BeautifulSoup(r.text, "html.parser")
    thisweek_meals = get_meals(soup, 'c16814')
    nextweek_meals = get_meals(soup, 'c16815')

    URL_today = 'http://www.studentenwerk-potsdam.de/mensa-brandenburg.html'
    r_today = requests.get(URL_today)
    soup_today = BeautifulSoup(r_today.text, "html.parser")
    today_meals = get_todaysmeals(soup_today, 'c10856')

    data = {}
    data['date'] = str(datetime.datetime.now())
    data['meals'] = today_meals + thisweek_meals + nextweek_meals

    return data


'''
    wird verwendet fuer alle tage ab morgen
'''


def get_meals(soup, id):
    container = soup.find("div", {"id": id})
    tables = container.find_all("table", {'class': 'bill_of_fare'})

    meals = [get_meal(table) for table in tables]

    return meals


'''
    wird verwendet fuer alle tage ab morgen
'''


def get_meal(table):
    rows = table.find_all('tr')
    date = rows[0].text
    headings = [col.text for col in rows[1] if col != '\n']
    meals = [col.text for col in rows[2] if col != '\n']
    icons = [list(img.get('alt', '') for img in col.find_all('img')) for col in
             rows[3] if col != '\n']

    meal = {
        'date': date,
        'meals': [{'heading': heading, 'meal': meal, 'icon': icon} for heading, meal, icon in
                  zip(headings, meals, icons)]
    }

    return meal


'''
    wird verwendet fuer heute
'''


def get_todaysmeals(soup, id):
    container = soup.find("div", {"id": id})
    tables = container.find_all("table", {'class': 'bill_of_fare'})

    if not tables:
        date = container.find('h2', {'id': 'ueberschrift_h2'})
        date = str(date.text)
        date = date[date.find('den') + 3:].strip()

        meals = []
        meals.append(
            {'date': date,
             'meals': [{'heading': '',
                        'meal': 'Die Mittagszeit in unseren Mensen ist bereits beendet. Daher steht der heutige Speiseplan nicht mehr zur Verfügung',
                        'icon': ''}
                       ]}
        )


    else:
        meals = [get_todaysmeal(table, container) for table in tables]

    return meals


'''
    wird verwendet fuer heute
'''


def get_todaysmeal(table, container):
    rows = table.find_all('tr')
    date = container.find('h2', {'id': 'ueberschrift_h2'})
    date = str(date.text)
    date = date[date.find('den') + 3:].strip()

    headings = [col.text for col in rows[0] if col != '\n']
    meals = [col.text for col in rows[1] if col != '\n']
    icons = [list(img.get('alt', '') for img in col.find_all('img')) for col in
             rows[2] if col != '\n']

    meal = {
        'date': date,
        'meals': [{'heading': heading, 'meal': meal, 'icon': icon} for heading, meal, icon in
                  zip(headings, meals, icons)]
    }

    return meal
