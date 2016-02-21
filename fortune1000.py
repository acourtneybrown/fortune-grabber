# -*- coding: utf-8 -*-
# Fortune 1000 grabber. Download and parse companies information

# Import libraries
from bs4 import BeautifulSoup
import urllib2
import json
import re
from urlparse import urljoin
import unicodecsv

# Define class for companies
class Company:
    rank = 0
    title = ""
    ticker = ""
    industry = ""
    sector = ""
    hq_location = ""
    website = ""
    years_on_list = 0
    ceo = ""
    eps = 0
    employees = 0
    revenues = 0
    profits = 0
    img_url = ""
    state_geo_code = ""

# Fortune 1000 graber function
def grab():

    # Obtaining post id
    data = urllib2.urlopen("http://fortune.com/fortune500/")
    soup = BeautifulSoup(data,"html.parser")
    postid = next(attr for attr in soup.body['class'] if attr.startswith('postid'))
    postid = re.match(r'postid-(\d+)', postid).group(1)

    companies = []

    # Fetch for pages with data and process JSONs
    for i in range(1,51):
        page_url = "http://fortune.com/data/franchise-list/{postid}/{index}/".format(postid=postid,index=str(i))
        page_data = json.load(urllib2.urlopen(page_url), encoding='utf-8')

        # Process JSON data
        for item in page_data["articles"]:
            company = Company()
            company.rank = item["rank"]
            company.title = item["title"]
            company.ticker = item["ticker_text"].upper()
            company.industry = item["tables"]["Company Info"]["data"]["Industry"][0]
            company.sector = item["tables"]["Company Info"]["data"]["Sector"][0]
            company.hq_location = item["tables"]["Company Info"]["data"]["HQ Location"][0]
            company.years_on_list = item["tables"]["Company Info"]["data"]["Years on List"][0]
            company.ceo = item["tables"]["Company Info"]["data"]["CEO"][0]
            company.eps = item["tables"]["Earnings Per Share"]["data"]["Earnings Per Share ($)"][0]
            company.employees = item["tables"]["Key Financials (last fiscal year)"]["data"]["Employees"][0]
            company.revenues = item["tables"]["Key Financials (last fiscal year)"]["data"]["Revenues ($M)"][0]
            company.profits = item["tables"]["Key Financials (last fiscal year)"]["data"]["Profits ($M)"][0]

            company.state_geo_code = company.hq_location.split(", ")[1]

            if item["featured_image"] != "":
                company.img_url = item["featured_image"]["src"]

            # Parsing website link
            s = BeautifulSoup(item["tables"]["Company Info"]["data"]["Website"][0],"html.parser")
            company.website = s.a.get('href')

            print company.rank + ". " + company.title

            companies.append(company)

    return companies

# Obtain companies
companies = grab()

# Saving to CSV
f = open("output/fortune1000.csv", "wt")

try:
    writer = unicodecsv.writer(f, encoding='utf-8')
    writer.writerow( ("Rank", "Title", "Ticker", "Industry", "Sector", "HQ Location", "Years on list", "CEO", "EPS",
    "Employees", "Revenues", "Profits", "Image URL", "Website", "geoCode") )

    for company in companies:

        writer.writerow((company.rank, company.title, company.ticker, company.industry,
        company.sector, company.hq_location, company.years_on_list, company.ceo, company.eps, company.employees,
        company.revenues, company.profits, company.img_url, company.website, company.state_geo_code))

finally:
    f.close()
