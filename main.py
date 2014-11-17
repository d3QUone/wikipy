import requests, wikipedia
from bs4 import BeautifulSoup as bs


endLists = []


def getReady():
    global endLists
    #open input file whith links and prepare target file for save

    with open("lists.txt", "r") as f:
        data = f.read()
        endLists = data.split("\n")
        print len(endLists), "links\n"


def parseEndLists(List):
    headers = {"User-agent":"Mozilla/5.0"}

    for link in List:
        if link != "": #for stabilyty
            
            r = requests.get(link, headers=headers)
            soup = bs(r.text)

            hrefs = soup.find_all("a")
            print len(hrefs), "hrefs"

            for hr in hrefs:
                print hr

        


def main():
    # build here
    getReady()
    parseEndLists(endLists)


main()
