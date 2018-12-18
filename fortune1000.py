#!/usr/bin/env python3

from bs4 import BeautifulSoup

import json
import logging
import os
import re
import sys
import urllib.request


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class Company:
    title = ""
    rank = 0
    name = ""
    item = {}


def usage():
    print("Usage: %s <year>" % sys.argv[0])
    sys.exit(1)


def main():
    if len(sys.argv) < 2:
        usage()

    # Obtain companies
    year = sys.argv[1]
    companies = grab(year)
    dirName = f"output/fortune1000/{year}"
    if not os.path.exists(dirName):
        os.makedirs(dirName)

    for company in companies:
        with open(f"{dirName}/{company.rank:04}-{company.name}", "wt") as outfile:
            json.dump(company.item, outfile)


def grab(year):
    # Obtaining post id
    data = urllib.request.urlopen(f"http://fortune.com/fortune500/{year}/")
    soup = BeautifulSoup(data,"html.parser")
    postid = next(attr for attr in soup.body['class'] if attr.startswith('postid'))
    postid = re.match(r'postid-(\d+)', postid).group(1)
    companies = []

    # Fetch for pages with data and process JSONs
    for i in range(0, 1000, 100):
        page_url = "http://fortune.com/api/v2/list/{postid}/expand/item/ranking/asc/{start}/100/".format(postid=postid, start=str(i))
        logger.info(page_url)

        try:
            page_data = json.load(urllib.request.urlopen(page_url), encoding='utf-8')

            for item in page_data["list-items"]:
                company = Company()
                company.title = item["title"]
                company.rank = item["rank"]
                company.name = item["name"]
                company.item = item
                logger.info(str(company.rank) + ". " + str(company.title))

                companies.append(company)
        except json.JSONDecodeError as error:
            logger.error(str(i) + " to " + str(i+100) + " has JSONDecodeError.", exc_info=error)

    return companies


if __name__ == "__main__":
    main()
