__author__ = 'marcman'

import requests, json, datetime
from bs4 import BeautifulSoup


def get_api_as_json():
    URL = 'http://www.studentenwerk-potsdam.de/speiseplan/'

    r = requests.get(URL)
    soup = BeautifulSoup(r.text, "html.parser")

    thisweek_meals = get_meals(soup, 'c16814')
    nextweek_meals = get_meals(soup, 'c16815')

    data = {}
    data['date'] = str(datetime.datetime.now())
    data['meals'] = thisweek_meals + nextweek_meals

    return data


def get_meals(soup, id):
    container = soup.find("div", {"id": id})
    tables = container.find_all("table", {'class': 'bill_of_fare'})

    meals = [get_meal(table) for table in tables]

    return meals


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
