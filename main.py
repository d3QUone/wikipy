import requests, wikipedia, sys, csv
from bs4 import BeautifulSoup as bs

endLists = []

def main():
    getReady()
    parseEndLists(endLists)

# add list2list parse feature 

def parseEndLists(List):
    headers = {"User-agent":"Mozilla/5.0"}
    endpoint = "http://en.wikipedia.org"

    f = open("output/hrefs.txt", "w") # demo file
    f.close()

    j = 0
    for link in List:
        if link != "": #for stabilyty
            r = requests.get(link, headers=headers)
            soup = bs(r.text)
            hrefs = soup.find_all("a")
            print "\n", len(hrefs), "hrefs\n"
            # --
            
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
                        f = open("output/hrefs.txt", "a")
                        f.write(sthr + "\n")
                        f.close()
                        if parsePeople(sthr):
                            print j
                            j += 1
                        
                    # -- testing --
                    #if j == 10:
                        #break
                    # -- 
    print "total processed", j
    

def parsePeople(link):
    # load and parse link
    template = {}
    headers = {"User-agent":"Mozilla/5.0"}
    
    try:
        r = requests.get(link, headers=headers)
        soup = bs(r.text)

        allclasses = ["fn", "nickname", "bday", "dday deathdate", "role"]
        for aclass in allclasses:
            if aclass == "role":
                #<td class="role"> -- if role-key
                fn = soup.find_all("td", class_ = aclass)
            else:
                fn = soup.find_all("span", class_= aclass)
                
            if len(fn) > 0:
                for item in fn:
                    f = item.contents
                    if f[0].find("<") == -1 and f[0].find(">") == -1:
                        template[aclass] = f[0]
        # now template is fulled 
        if len(template) > 1:
            template["link"] = link
            try:
                ofile = open("output/output.csv", "a")
                lis = generateCSVstring(template)
                ofile.write(lis)
                ofile.close()
                return True
            except:
                print "Error in output file"
                return False
                #sys.exit(1)
        
    except Exception as ex:
        print "(parse r)", str(ex)
        return False
                

def generateCSVstring(dic):
    # prepare CSV row here
    st = ""
    br = "; "
    try:
        st += dic["fn"].encode("utf8")
        st += br
    except:
        st += br

    try:
        st += dic["nickname"].encode("utf8")
        st += br
    except:
        st += br

    try:
        st += dic["bday"].encode("utf8")
        st += br
    except:
        st += br
           
    try:
        st += dic["dday deathdate"].encode("utf8")
        st += br
    except:
        st += br

    try:
        st += dic["link"].encode("utf8")
    except:
        pass

    return st + "\n"
    

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

    out = open("output/output.csv", "w")
    out.close()


main()
