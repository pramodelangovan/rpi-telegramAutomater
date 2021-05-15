import setup
import requests
from bs4 import BeautifulSoup as bs
from teleModel.models import goldRates
import json



CITIES = ["bangalore", "chennai"]
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

def getDataFromWebiste():
    data = {}
    for city in CITIES:
        # url = URL.format(city)
        # res = requests.get(url, headers=HEADERS)
        # ############### Temp Code ##################
        # with open("webpage.html", "w", encoding="utf-8") as resFile:
        #     resFile.write(str(res.text))
        # ############### Temp Code ##################
        data[city] = getRates()
    return data

def _cleanText(text):
    return text.replace("\n", "").replace("\t", "").replace("₹", "").replace(",", "").replace("  ", " ").strip()

def _getRates(table):
    return [[_cleanText(cell.text) for cell in row("td")] for row in table.find_all("tr")]

def _getRates1(table):
    lst = []
    for row in table.find_all("tr")[1:]:
        rows = row("td")
        date = _cleanText(rows[0].text)
        car22 = getClassified(rows[1])
        car24 = getClassified(rows[2])
        ret = {}
        ret[date] = {}
        ret[date].update({"22 Carat": {"tenGramRateYday": car22[0],"status": car22[2], "differnce": car22[1]}})
        ret[date].update({"24 Carat": {"tenGramRateYday": car24[0],"status": car24[2], "differnce": car24[1]}})

        lst.append(ret)
    return lst



def getClassified(row):
    status = None
    cell = str(row)
    text = _cleanText(row.text)
    if "gain" in str(cell):
        status = "inc"
    elif "lose" in str(cell):
        status = "dec"
    elif "nochange" in str(cell):
        status = "noc"

    data = text.replace(")", "").strip().split("(")
    return data[0].strip(), data[1].strip(), status

def _additionalData(data):
    oneGramRateYday = data["yesterday"]
    soverignRateYday = oneGramRateYday * 8
    tenGramRateYday = oneGramRateYday * 10
    oneGramRateTday = data["Today"]
    soverignRateTday = oneGramRateYday * 8
    tenGramRateTday = oneGramRateYday * 10
    data["yesterday"] = {}

def getRates(restext=None):
    ############### Temp Code ##################
    restext = ""
    with open("webpage.html", "r", encoding="utf-8") as resFile:
        restext = resFile.read()
    ############### Temp Code ##################
    soup = bs(restext, 'html5lib')
    tables = soup.find_all("div", {"class": "gold_silver_table"})
    yesterdayRate, TodayRate = _getRates(tables[0])[1][1:-1]
    return {"yesterday": int(yesterdayRate), "Today": int(TodayRate)}

def getLastTenDaysRates(restext=None):
    ############### Temp Code ##################
    restext = ""
    with open("webpage.html", "r", encoding="utf-8") as resFile:
        restext = resFile.read()
    ############### Temp Code ##################
    soup = bs(restext, 'html5lib')
    tables = soup.find_all("div", {"class": "gold_silver_table_10_days"})
    return _getRates1(tables[0])


if __name__ == "__main__":
    print(json.dumps(getLastTenDaysRates(), indent=4))
    # print(getDataFromWebiste())