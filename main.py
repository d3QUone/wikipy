import requests, sys, json, traceback
from bs4 import BeautifulSoup as bs

everylink = [] # of loaded
endLists = []  # of new links 

def main():
    getReady()
    # input links
    parseEndLists(endLists) 
    print "close session\ncheck", len(everylink["errors"]), "error links"
    # repeat errors 
    en = 1
    for erlink in everylink["errors"]:
        if parsePeople(erlink):
            everylink["pages"].append(erlink)
            print "--", en, "--"
        en += 1
        everylink["errors"].remove(erlink)
        saveProcessData()


def saveProcessData():
    # save the process data
    f = open("indexing.txt", "w")
    f.write(json.dumps(everylink))
    f.close()


def parseEndLists(List):
    headers = {"User-agent":"Mozilla/5.0"}
    endpoint = "http://en.wikipedia.org"
    j = 0
    for link in List:
        if len(link) > 0 and link not in everylink["input"]: 
            r = requests.get(link, headers=headers)
            soup = bs(r.text)
            hrefs = soup.find_all("a") # any optimisation from here to endpoin? 
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
                            # btw STHR can be in 'errors' 
                            if parsePeople(sthr):
                                everylink["pages"].append(sthr)
                                if sthr in everylink["errors"]:
                                    everylink["errors"].remove(sthr)
                                print "-----", j, "-----"
                                j += 1
                            else:
                                everylink["errors"].append(sthr)
                            saveProcessData()
            # save link to source list 
            everylink["input"].append(link) 
    print "got data about", j, "people total"
    

# 2, find out how to parse 1st paragraph
def parsePeople(link):
    template = {}
    headers = {"User-agent":"Mozilla/5.0"}
    try:
        r = requests.get(link, headers=headers)
        soup = bs(r.text)
        # parse
        allclasses = ["fn", "nickname", "bday", "dday deathdate", "role"]
        for aclass in allclasses:
            if aclass == "role":
                tag = "td"
            else:
                tag = "span"
            group = soup.find_all(tag, class_ = aclass)
            if len(group) > 0:
                #print "----", aclass, "----"
                forsave = ""
                for item in group:
                    f = str(item)
                    a0 = f.find("<")
                    a1 = f.find(">")
                    while a0 != -1:
                        a0 = f.find("<")
                        a1 = f.find(">")
                        t = f[a0:a1+1]
                        f = f.replace(t, "")
                    #print "f2:", f
                    if aclass == "role":
                        forsave += f.replace("\n", " ") + " "
                    else:
                        forsave = f.replace("\n", " ")
                        break
                        # I need only one non-role report
                #print aclass, "|", forsave
                template[aclass] = forsave
        if len(template) > 1:
            # now template is fulled, save to table
            template["link"] = link
            try:
                # save to existing file
                ofile = open("output/output" + str(len(everylink["input"])) + ".csv", "a")
                lis = generateCSVstring(template)
                ofile.write(lis)
                ofile.close()
                return True # 1
            except:
                # create file and save
                ofile = open("output/output" + str(len(everylink["input"])) + ".csv", "w")
                lis = generateCSVstring(template)
                ofile.write(lis)
                ofile.close()
                return True # 1
    except Exception as ex:
        print "(parse r)"
        print format_exception(ex)
        print "--"*25
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
    
    # open file for indexing system
    try:
        f = open("indexing.txt", "r")
        data = f.read()
        f.close()
        everylink = json.loads(data)
    except:
        # create empty file w/template
        everylink = {"pages":[], "errors":[], "input":[]}
        f = open("indexing.txt", "w")
        f.write(json.dumps(everylink))
        f.close()
        print "Indexing system was set up, don't delete 'indexing.txt'"
                

def generateCSVstring(dic):
    # prepare a table row for .CSV here
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


# i like this
def format_exception(e):
    exception_list = traceback.format_stack()
    exception_list = exception_list[:-2]
    exception_list.extend(traceback.format_tb(sys.exc_info()[2]))
    exception_list.extend(traceback.format_exception_only(sys.exc_info()[0], sys.exc_info()[1]))

    exception_str = "Traceback (most recent call last):\n"
    exception_str += "".join(exception_list)
    # Removing the last \n
    exception_str = exception_str[:-1]
    return exception_str
            

main()
