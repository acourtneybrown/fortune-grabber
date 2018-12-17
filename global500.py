# -*- coding: utf-8 -*-
# Fortune Global 500 grabber. Download and parse companies information

# Import libraries
# Same as the fortune1000.py. However some fields of eps and mktvalue are missing. I skipped it. :)
# last checked : 8th September, 2017

from json import JSONDecodeError
import urllib.request
import json
import csv

class Company:
    ranking = 0
    fullname = ""
    ticker = ""
    industry = ""
    sector = ""
    hqlocation = ""
    hqaddr = ""
    website = ""
    yearsonlist = 0
    ceo = ""
    employees = 0
    fortune500rank = 0
    revenues = 0
    revchange = 0.0
    profits = 0
    prftchange = 0.0
    hqstate = ""
    hqzip = ""
    assets = 0

def grab():
    # Obtaining post id
    companies = []

    # Fetch for pages with data and process JSONs
    for i in range(0, 500, 50):
        page_url = "http://fortune.com/api/v2/list/2082743/expand/item/ranking/asc/{postid}/50/".format(postid=str(i))

        try:
            page_data = json.load(urllib.request.urlopen(page_url), encoding='utf-8')

            for item in page_data["list-items"]:
                company = Company()
                try:
                    company.ranking = item["meta"]["ranking"]
                    company.fullname = item["meta"]["fullname"]
                    company.ticker = item["meta"]["ticker"].upper()
                    company.industry = item["meta"]["industry"]
                    company.sector = item["meta"]["sector"]
                    company.hqlocation = item["meta"]["hqlocation"]
                    company.hqaddr = item["meta"]["hqaddr"]
                    company.yearsonlist = item["meta"]["yearsonlist"]
                    company.ceo = item["meta"]["ceo"]
                    company.employees = item["meta"]["employees"]
                    company.revenues = item["meta"]["revenues"]
                    company.profits = item["meta"]["profits"]
                    company.hqzip = item["meta"]["hqzip"]
                    company.website = item["meta"]["website"]
                    company.fortune500rank = item["meta"]["fortune500-rank"]
                    company.revchange = item["meta"]["revchange"]
                    company.prftchange = item["meta"]["prftchange"]
                    company.hqstate = item["meta"]["hqstate"]
                    company.assets = item["meta"]["assets"]
                except KeyError:
                    print("Keyerror has occurred for " + str(company.fullname))

                print(str(company.ranking) + ". " + str(company.fullname) + " ; " + str(company.ceo))

                companies.append(company)
        except JSONDecodeError:
            print(str(i) + " to " + str(i+100) + " has JSONDecodeError.")

    return companies


# Obtain companies
companies = grab()

# Saving to CSV
f = open("global500.csv", "wt")

try:
    writer = csv.writer(f)
    writer.writerow(["ranking", "full name", "ticker", "industry", "sector", "hq location", "hq address", "years on list", "ceo",
                     "employees", "revenues", "profits", "hq zip", "website", "fortune 500 rank", "revenue change", "profit change", "assets","hq state"])

    for company in companies:
        writer.writerow([company.ranking, company.fullname, company.ticker, company.industry,
                         company.sector, company.hqlocation, company.hqaddr, company.yearsonlist, company.ceo,
                         company.employees, company.revenues, company.profits, company.hqzip, company.website,
                         company.fortune500rank, company.revchange, company.prftchange, company.assets, company.hqstate])

finally:
    f.close()
