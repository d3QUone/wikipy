import requests, wikipedia, sys
from bs4 import BeautifulSoup as bs

endLists = []

def main():
    getReady()
    parseEndLists(endLists)


def parseEndLists(List):
    headers = {"User-agent":"Mozilla/5.0"}
    endpoint = "http://en.wikipedia.org"

    # recreate file
    f = open("output/hrefs.txt", "w")
    f.close()
    for link in List:
        if link != "": #for stabilyty
            r = requests.get(link, headers=headers)
            soup = bs(r.text)
            hrefs = soup.find_all("a")
            print "\n", len(hrefs), "hrefs"

            f = open("output/hrefs.txt", "a")
            # --
            j = 0
            # --
            for hr in hrefs:
                sthr = str(hr)                    
                s0 = sthr.find("/wiki/")
                if s0 != -1:                
                    s1 = 0
                    for i in range(s0, len(sthr)):
                        if sthr[i] == '"':
                            s1 = i
                            break
                        
                    if s1 > s0:
                        #the endpoint to Article page
                        sthr = endpoint + sthr[s0:s1] 
                        f.write(sthr + "\n")

                        parsePeople(sthr)

                        j += 1
                        
                    # -- testing --
                    if j == 10:
                        break
                    # -- 

            f.close()


def parsePeople(link):
    # load and parse link
    template = {}
    headers = {"User-agent":"Mozilla/5.0"}
    r = requests.get(link, headers=headers)
    soup = bs(r.text)

    allclasses = ["fn", "nickname", "bday", "dday deathdate", "role"]
    for aclass in allclasses:
        fn = soup.find_all("span", class_= aclass)
        if len(fn) > 0:
            item = fn[0]
            f = item.contents
            # check if this has no tags
            if f[0].find("<") == -1 and f[0].find(">") == -1:
                print aclass, str(f[0]) 
                template[aclass] = f[0]

    if len(template) > 0:
        template["link"] = link
        print len(template)-1, "item(s):\n", template, "\n"


    # prepare CSV template, don't save if empty
    #"fullname":"", "nickname":"", "bday":"", "dday":"", "role":""
    #print len(template), "full fields"
    

def getReady():
    global endLists
    #open input file whith links and prepare target file for save
    try:
        f = open("lists.txt", "r")
        data = f.read()
        f.close()
        endLists = data.split("\n")
        print len(endLists), "links"
    except:
        print "File 'lists.txt' not found"
        sys.exit("Create one")


main()
