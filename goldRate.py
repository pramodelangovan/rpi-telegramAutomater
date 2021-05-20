import json
import requests
import setup
import time

from datetime import datetime
from datetime import timedelta
from tabulate import tabulate

from utils import alertOwner
from bs4 import BeautifulSoup as bs
from teleModel.models import goldRates



CITIES = ["bangalore", "chennai"]
CARAT = ["22", "24"]
URL = "https://www.goodreturns.in/gold-rates/{}.html"
HEADERS = {
    "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
    "accept-encoding": "gzip, deflate, br",
    "accept-language": "en-US,en;q=0.9",
    "sec-ch-ua": "\" Not A;Brand\";v=\"99\", \"Chromium\";v=\"90\", \"Google Chrome\";v=\"90\"",
    "sec-ch-ua-mobile": "?0",
    "sec-fetch-dest": "document",
    "sec-fetch-mode": "navigate",
    "sec-fetch-site": "same-origin",
    "sec-fetch-user": "?1",
    "upgrade-insecure-requests": "1",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36"
}

def getDataFromWebiste(typ="10"):
    data = {}
    for city in CITIES:
        url = URL.format(city)
        res = requests.get(url, headers=HEADERS)

        if res.status_code == 200:
            if typ == "10":
                data = getLastTenDaysRates(res.text)
            if typ == "1":
                data = getRatesForToday(res.text, city)

            addGoldRatesToDB(data, city)
            time.sleep(30)
        else:
            raise("error in request")

def _cleanText(text):
    return text.replace("\n", "").replace("\t", "").replace("₹", "").replace(",", "").replace("  ", " ").strip()

def _getRatesForTenDays(table):
    lst = []
    for row in table.find_all("tr")[1:]:
        rows = row("td")
        date = _cleanText(rows[0].text)
        lst.extend([_getCategoryUpdate(date, "22", _getClassified(rows[1])), _getCategoryUpdate(date, "24", _getClassified(rows[2]))])
    return lst

def _getCategoryUpdate(date, purity, carat, typ="10"):
    if typ == "10":
        tenGramRate = carat[0]
        oneGramRate = carat[0]/10
        soverignRate = (carat[0]/10)*8
    elif typ == "1":
        tenGramRate = carat[0]*10
        oneGramRate = carat[0]
        soverignRate = carat[0]*8
    return {"date": date,
            "purity": purity,
            "tenGramRate": tenGramRate,
            "oneGramRate": oneGramRate,
            "soverignRate": soverignRate,
            "state": carat[2],
            "differnce": carat[1]}

def _getClassified(row):
    status = None
    cell = str(row)
    text = _cleanText(row.text)
    status = _getStatus(cell)

    data = text.replace(")", "").replace("-","").strip().split("(")
    return int(data[0].strip()), int(data[1].strip())/10, status

def _getStatus(cell):
    status = "noc"
    if "gain" in str(cell):
        status = "inc"
    elif "lose" in str(cell):
        status = "dec"
    elif "nochange" in str(cell):
        status = "noc"
    return status

def getLastTenDaysRates(restext=None):
    soup = bs(restext, 'html5lib')
    tables = soup.find_all("div", {"class": "gold_silver_table_10_days"})
    return _getRatesForTenDays(tables[0])

def getDateInFormat():
    today = datetime.now()
    yday = today - timedelta(days=1)
    dayBefore = today - timedelta(days=2)
    return today.strftime("%b %d %Y"), yday.strftime("%b %d %Y"), dayBefore.strftime("%b %d %Y")

def _getRates(table, purity, city):
    lst = []
    tday, yday, dbday = getDateInFormat()
    row = table.find_all("tr")[1:]
    gramRow = row[0]('td')

    tdayData = getTodayData(gramRow)
    ydayData = getYdayData(gramRow, yday, dbday, purity, city)

    lst.extend([_getCategoryUpdate(tday, purity, tdayData, typ="1"), _getCategoryUpdate(yday, purity, ydayData, typ="1")])
    return lst

def getYdayData(gramRow, yday, dbday, purity, city):
    rate = int(_cleanText(gramRow[2].text))
    if not goldRates.objects.filter(date=dbday, purity=purity, city=city).exists():
        diff = 0; status = "noc"
    else:
        dbRates = goldRates.objects.get(date=dbday, purity=purity, city=city)
        diff = yday - dbRates.oneGramRate
        status = 'dec' if diff < 1 else 'inc' if diff > 1 else 'noc'
    return int(rate), int(diff), status

def getTodayData(gramRow):
    rate = int(_cleanText(gramRow[1].text))
    diff = int(_cleanText(gramRow[3].text))
    status = _cleanText(_getStatus(gramRow[3]))
    return rate, diff, status

def getRatesForToday(restext, city):
    lst = []
    soup = bs(restext, 'html5lib')
    tables = soup.find_all("div", {"class": "gold_silver_table"})
    lst+= _getRates(tables[0], "22", city) + _getRates(tables[1], "24", city)
    return lst

def addGoldRatesToDB(rateList, city):
    for rate in rateList:
        rateObj = goldRates()
        rateObj.date = rate["date"]
        rateObj.oneGramRate = rate["oneGramRate"]
        rateObj.soverignRate = rate["soverignRate"]
        rateObj.tenGramRate = rate["tenGramRate"]
        rateObj.differencePerGram = rate["differnce"]
        rateObj.state = rate["state"]
        rateObj.purity = rate["purity"]
        rateObj.city = city
        if not goldRates.objects.filter(date=rateObj.date,
                                        purity=rateObj.purity,
                                        city=rateObj.city).exists():
            rateObj.save()

def getCurrentGoldRatesByCity():
    data = {}
    ret = ""
    for city in CITIES:
        for purity in CARAT:
            marker = "{}: {} Carat".format(city, purity)
            data[marker] = getCurrentGoldRates(city, purity)

    for key, value in data.items():
        ret += "{}\n{}\n\n".format(key.capitalize(), value)

    return ret

def getCurrentGoldRates(city, purity):
    lst = []
    dates = list(getDateInFormat())
    dates.sort(reverse=True)

    for date in dates:
        lst.append(makeRowItems(date, city, purity))
    return tabulate(lst, headers=["Date", "1 gram", "Change/1gm", "8gram"], tablefmt='plain')

def makeRowItems(date, city, purity):
    rate = goldRates.objects.filter(date=date, city=city, purity=purity).first()
    if rate:
        changeMessage = "{}  ₹{}".format(statusMessage(rate.state), rate.differencePerGram)
        dateStr = datetime.strptime(rate.date, "%b %d %Y").strftime("%d.%m.%y")
        return [dateStr, "₹{}".format(float(rate.oneGramRate)), changeMessage, "₹{}".format(float(rate.soverignRate))]

def statusMessage(status):
    return "⬇️" if status == "dec" else "⬆️" if status == "inc" else "❎"

if __name__ == "__main__":
    try:
        getDataFromWebiste("10")
        alertOwner("Gold details obtained successfully")
    except Exception as e:
        alertOwner("Error occured in fetching results: {}".format(str(e)))