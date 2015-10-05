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
    data['thisweek_meals'] = thisweek_meals
    data['nextweek_meals'] = nextweek_meals

    return data


def get_meals(soup, id):
    container = soup.find("div", {"id": id})
    tables = container.find_all("table", {'class': 'bill_of_fare'})

    # seperate each row  # attention exclude those elements which only has '\n' in it
    dates = [date.text for date in container.find_all("div", {'class': 'date'})]
    headings = [tr.text for tr in tables[0].find_all('tr')[1] if tr != '\n']
    meals = [tr.text for tr in tables[0].find_all('tr')[2] if tr != '\n']
    # get a list of all alt textes of the image tags inside a row for each entry of the week
    icons = [list(img.get('alt', '') for img in tr.find_all('img')) for tr in
             tables[0].find_all('tr')[3] if tr != '\n']

    meals = [Meal(date=date, heading=heading, meal=meal, icons=icons) for
             date, heading, meal, icons in
             zip(dates, headings, meals, icons)]

    return json.dumps(meals, default=lambda o: o.__dict__,
                      sort_keys=True)


class Meal:
    def __init__(self, date, heading, meal, icons):
        self.date = date
        self.heading = heading
        self.meal = meal
        self.icons = icons

    def to_json(self):
        return json.dumps(self, default=lambda o: o.__dict__,
                          sort_keys=True, indent=4)
