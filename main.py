import requests, sys, json
from bs4 import BeautifulSoup as bs

everylink = [] # of loaded
endLists = []  # of new links 

def main():
    getReady()
    parseEndLists(endLists) # parse from input only, no repeats here 

    print "close session"
    # save the process data
    f = open("indexing.txt", "w")
    f.write(json.dumps(everylink))
    f.close()


# add list2list parse feature 

def parseEndLists(List):
    headers = {"User-agent":"Mozilla/5.0"}
    endpoint = "http://en.wikipedia.org"

    # demo file
    f = open("output/hrefs.txt", "w") 
    f.close()

    j = 0
    for link in List:
        if link != "" and link not in everylink["input"]: 
            r = requests.get(link, headers=headers)
            soup = bs(r.text)
            hrefs = soup.find_all("a")
            print "\n", len(hrefs), "hrefs\n"
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
                        # the endpoint to Article page
                        sthr = endpoint + sthr[s0:s1]

                        if sthr not in everylink["pages"]:
                            # btw may be in 'errors' 

                            # save for debug 
                            f = open("output/hrefs.txt", "a") 
                            f.write(sthr + "\n")
                            f.close()
                            if parsePeople(sthr):
                                # index this 
                                everylink["pages"].append(sthr)
                                print j
                                j += 1
                            else:
                                everylink["errors"].append(sthr)
                                # do "check errors" step
                                # if output isn't the same
                                # (parsed some data/no error, no data) -
                                # - delete from error-list
            # save link to source list 
            everylink["input"].append(link) 

    print "got data about", j, "people total"
    

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
                return True # 1
            except:
                #print "Error in output file"
                return False # 2 
        
    except Exception as ex:
        print "(parse r)", str(ex)
        return False # 3


def getReady():
    global endLists, everylink
    # open input file whith links and prepare target file for save
    try:
        f = open("lists.txt", "r")
        data = f.read()
        f.close()
        endLists = data.split("\n")
        print len(endLists), "links in input"
    except:
        print "File 'lists.txt' not found"
        sys.exit("Create one")
    #out = open("output/output.csv", "w")
    #out.close()
    
    # open file for indexing system
    try:
        f = open("indexing.txt", "r")
        data = f.read()
        f.close()
        everylink = json.loads(data)
    except:
        # create empty file w/template
        f = open("indexing.txt", "w")
        f.write(json.dumps({"pages":[], "errors":[], "input":[]}))
        f.close()
        print "Indexing system was set up, don't delete 'indexing.txt'"
                

def generateCSVstring(dic):
    # prepare CSV row here
    st = ""
    br = "; "
    em = " "
    try:
        st += dic["fn"].encode("utf8") + br
    except:
        st += em + br

    try:
        st += dic["nickname"].encode("utf8") + br
    except:
        st += em + br

    try:
        if type(dic["role"]) == type([]):
            for role in dic["role"]:
                st += role.encode("utf8") + ", "
            st += br
        else:
            st += dic["role"].encode("utf8") + br
    except:
        st += em + br

    try:
        st += dic["bday"].encode("utf8") + br
    except:
        st += em + br
           
    try:
        st += dic["dday deathdate"].encode("utf8") + br
    except:
        st += em + br

    try:
        st += dic["link"].encode("utf8")
    except:
        st += em
        pass

    return st + "\n"
            

main()
