# -*- coding: utf-8 -*-
import requests, sys, json, traceback
from bs4 import BeautifulSoup as bs
from datetime import datetime

everylink = [] # of loaded
endLists = []  # of new links

# load all datas
def getReady():
    global endLists, everylink
    try: # open input file whith links and prepare target file for save
        f = open("lists.txt", "r")
        data = f.read()
        f.close()
        endLists = data.split("\n")
    except:
        print "File 'lists.txt' not found"
        sys.exit(2)
    try: # open file for indexing system
        f = open("indexing.txt", "r")
        data = f.read()
        f.close()
        everylink = json.loads(data)
    except:
        everylink = {"pages":[], "errors":[], "input":[]}
        f = open("indexing.txt", "w")
        f.write(json.dumps(everylink))
        f.close()
        print "Indexing system was set up, don't delete 'indexing.txt'"
        

def main():
    t = datetime.now()
    getReady()
    print "Started on {0}, have {1} links to parse".format(t, len(endLists))
    parseEndLists(endLists)
    print "\nAll done in {0}; found {1} error links".format(datetime.now() - t, len(everylink["errors"]))

    # an experiment..
    t = datetime.now()
    print "\nre-doing errors... started on {0}\n".format(t)
    en = 0
    for erlink in everylink["errors"]:
        if parsePeople(erlink):
            everylink["pages"].append(erlink)
            en += 1
            print "--", en, "--"
        everylink["errors"].remove(erlink)
        saveProcessData()
    print "\nsession closed:\ncheck", len(everylink["errors"]), "error links"
    print "\nspent {0} time".format(datetime.now() - t)


def parseEndLists(List):
    headers = {"User-agent": "Mozilla/5.0"}
    endpoint = "http://en.wikipedia.org"
    for link in List:
        if len(link) > 0:
            print link
            if link.decode("utf8") not in everylink["input"]: 
                r = requests.get(link, headers = headers)
                soup = bs(r.text)
                hrefs = soup.find_all("a")
                print "\n{0} hrefs on the page\n".format(len(hrefs))
                j = 0
                for hr in hrefs:
                    sthr = str(hr)                    
                    s0 = sthr.find("/wiki/")
                    if s0 != -1:                
                        s1 = 0
                        for i in range(s0, len(sthr)):
                            if sthr[i] == '"':
                                s1 = i
                                break
                        if s1 > s0: # the endpoint to Article page 
                            sthr = endpoint + sthr[s0:s1]
                            if sthr not in everylink["pages"]:
                                if parsePeople(sthr):
                                    everylink["pages"].append(sthr)
                                    if sthr in everylink["errors"]:
                                        everylink["errors"].remove(sthr)
                                    print "-----", j, "-----"
                                    j += 1
                                else: # that pages have no data
                                    everylink["errors"].append(sthr)
                                saveProcessData()
                print "saved data about {0} people total".format(j)
            everylink["input"].append(link)


# store processed links
def saveProcessData():
    f = open("indexing.txt", "w")
    f.write(json.dumps(everylink))
    f.close()
            
    
# find out how to parse 1st paragraph
def parsePeople(link):
    template = {}
    headers = {"User-agent":"Mozilla/5.0"}
    try:
        r = requests.get(link, headers=headers)
        soup = bs(r.text)
        allclasses = ["fn", "nickname", "bday", "dday deathdate"]
        for aclass in allclasses:                
            group = soup.find_all("span", class_ = aclass)
            if len(group) > 0:
                print aclass, group
                f = str(group[0])
                a0 = f.find("<")
                a1 = f.find(">")
                while a0 != -1:
                    a0 = f.find("<")
                    a1 = f.find(">")
                    t = f[a0:a1+1]
                    f = f.replace(t, "")
                forsave = f.replace("\n", " ")                    
                template[aclass] = forsave
        
        # class = role / category , tag = td
        roles = soup.find_all(class_ = "role")
        if len(roles) > 0:
            print "roles:", roles
        else:
            category = soup.find_all(class_ = "category")
            print "category:", category
        '''
        <td class="category" style="vertical-align:middle;line-height:1.3em;">
        <div class="hlist">
        <ul style="line-height:1.25em;">
        <li>Astronomy</li>
        <li><a href="/wiki/Canon_law" title="Canon law">Canon law</a></li>
        <li>Economics</li>
        <li>Mathematics</li>
        <li>Medicine</li>
        <li>Politics</li>
        </ul>
        </div>
        </td>
        '''
        print "link:", link
        if len(template) > 2:
            template["link"] = link
            try: # to save into existing file
                ofile = open("output/output" + str(len(everylink["input"])) + ".csv", "a")
                lis = generateCSVstring(template)
                ofile.write(lis)
                ofile.close()
                return True # 1
            except: # create file and save
                ofile = open("output/output" + str(len(everylink["input"])) + ".csv", "w")
                lis = generateCSVstring(template)
                ofile.write(lis)
                ofile.close()
                return True # 1
    except Exception as ex:
        print "(parsePeople, r)", format_exception(ex)
        print "--"*25
        return False # 3



def parseTables(page_link):
    template = {}
    headers = {"User-agent":"Mozilla/5.0"}
    try:
        r = requests.get(page_link, headers = headers)
        soup = bs(r.text)
        all_tables = soup.find_all("table", class_ = "wikitable")
        print "---found {0} tables on the page---\n".format(len(all_tables))
        for table in all_tables:
            sub_soup = bs(str(table))
            ths = sub_soup.find_all("th")
            step = len(ths)
            print "--current table has {0} columns--".format(step)

            i = 0
            res = ""
            all_td = sub_soup.find_all("td")
            for td in all_td:
                if i % step == 0:
                    print res
                    print "--"*25
                    res = ""
                # returns raw text without html-tags
                buf = str(td).replace("\n", " ").replace("&amp;", "&")
                while buf.find("<") != -1 or buf.find(">") != -1:
                    a = buf.find("<")
                    b = buf.find(">")
                    buf = buf[:a] + buf[b+1:] 
                res += buf + "|"
                i += 1
            print "\n", "**"*30, "\n"
            
    except Exception as ex:
        print "(parseTables, r)", format_exception(ex)
        print "--"*25
        

# prepare a table row for .CSV here
def generateCSVstring(dic):
    st = ""; br = "; "; em = " "
    try:
        st += dic["fn"].encode("utf8") + br
    except:
        st += em + br
    try:
        st += dic["nickname"].encode("utf8") + br
    except:
        st += em + br
    try:
        if isinstance(dic["role"], list):
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


# tracking the error in the caugth exception
def format_exception(e):
    print str(e) + " - given into traceback"
    exception_list = traceback.format_stack()
    exception_list = exception_list[:-2]
    exception_list.extend(traceback.format_tb(sys.exc_info()[2]))
    exception_list.extend(traceback.format_exception_only(sys.exc_info()[0], sys.exc_info()[1]))
    exception_str = "Traceback (most recent call last):\n"
    exception_str += "".join(exception_list)
    exception_str = exception_str[:-1]
    return exception_str

           
if __name__ == "__main__":
    #main()
    #parseTables("http://en.wikipedia.org/wiki/Forbes_Celebrity_100")
    parseTables("http://en.wikipedia.org/wiki/Forbes_list_of_The_World's_Most_Powerful_People")
