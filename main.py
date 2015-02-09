# -*- coding: utf-8 -*-
import requests, sys, json, traceback
from bs4 import BeautifulSoup as bs
from datetime import datetime
from saving import do_saving


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


# store processed links
def saveProcessData():
    f = open("indexing.txt", "w")
    f.write(json.dumps(everylink))
    f.close()
        

def main(): # fuck it. not flexible enough 
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
    # want return something ?

    
# find out how to parse 1st paragraph
def parsePeople(link):
    template = {}
    headers = {"User-agent":"Mozilla/5.0"}
    try:
        r = requests.get(link, headers=headers, timeout = 10)
        soup = bs(r.text)
        allclasses = ["fn", "nickname", "bday", "dday deathdate"]
        for aclass in allclasses:                
            group = soup.find_all("span", class_ = aclass)
            if len(group) > 0:
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
        """
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
        """
        if len(template) > 2:
            template["link"] = link
            return template
        else:
            return None
    except Exception as ex:
        print "(parsePeople, r)"#, format_exception(ex)
        return None


def parseTables(page_link):
    template = []
    append = template.append
    headers = {"User-agent":"Mozilla/5.0"}
    try:
        r = requests.get(page_link, headers = headers, timeout = 10)
        soup = bs(r.text)
        all_tables = soup.find_all("table", class_ = "wikitable")
        print "\n---found {0} tables on the page---\n".format(len(all_tables))
        for table in all_tables:
            sub_soup = bs(str(table))
            all_td = sub_soup.find_all("td")

            sub_res = []
            sub_pend = sub_res.append
            for td in all_td:
                buf = str(td).replace("\n", " ").replace("&amp;", "&")
                if "flagicon" in buf:
                    a = buf.find('href="')
                    buf = buf[a+1:]
                    a = buf.find('href="') + len('href="')
                    buf = buf[a+1:]
                    b = buf.find('"')
                    href = buf[:b]
                    sub_pend(href)
                else:
                    while buf.find("<") != -1 and buf.find(">") != -1:
                        a = buf.find("<")
                        b = buf.find(">")
                        buf = buf[:a] + buf[b+1:] 
                    sub_pend(buf)
            append(sub_res) # whole current table
    except Exception as ex:
        print "(parseTables, r)", format_exception(ex)
        print "--"*25
    return template


def parseOtherSite(page_link):
    template = []
    append = template.append
    headers = {"User-agent":"Mozilla/5.0"}
    try:
        r = requests.get(page_link, headers = headers, timeout = 10)
        soup = bs(r.text)
        all_lists = soup.find_all("li", class_="")
        print "\n---found {0} list items on the page---\n".format(len(all_lists))
        for item in all_lists:
            buf = str(item)
            sub_res = []
            sub_pend = sub_res.append
            
            a = buf.find('href="')
            buf = buf[a:]
            a = buf.find('href="') + len('href="')
            buf = buf[a:]
            b = buf.find('"')
            href = buf[:b]
            buf = buf[b+2:]
            sub_pend(href)
            
            while buf.find("<") != -1 and buf.find(">") != -1:
                a = buf.find("<")
                b = buf.find(">")
                buf = buf[:a] + buf[b+1:]
            sub_pend(buf)
            
            append(sub_res) # whole current table
    except Exception as ex:
        print "(parseTables, r)", format_exception(ex)
        print "--"*25
    return template
    

           
if __name__ == "__main__":
    file_set = "9"
    endpoint = "http://en.wikipedia.org/"
    links = {
        "7a": ["http://en.wikipedia.org/wiki/Forbes_Celebrity_100",
               "http://en.wikipedia.org/wiki/Forbes_list_of_The_World's_Most_Powerful_People"],
        "8": ["http://en.wikipedia.org/wiki/Forbes%27_list_of_world%27s_highest-paid_athletes",
              "http://en.wikipedia.org/wiki/40_under_40_(Fortune_magazine)",
              "http://en.wikipedia.org/wiki/Forbes_list_of_The_World%27s_100_Most_Powerful_Women"],
        "9": ["http://www.biographyonline.net/people/famous-100.html"]
              }

    already_saved = []
    append = already_saved.append
    for link in links[file_set]:
        #res = parseTables(link) # set < 9
        res = parseOtherSite(link)
        print res
        '''
        print "--- Got a set of {0} tables".format(len(res))
        for item in res:
            print "- Got a set of {0} rows".format(len(item))
            i = 0
            while i < len(item):
                row = item[i]
                personalData = parsePeople(endpoint + row)
                if personalData:
                    personalData["role"] = item[i + 1]
                    if personalData not in already_saved:
                        append(personalData)
                        do_saving(personalData, file_set)
                    else:
                        print "already saved"
                    i += 1
                i += 1
        '''
    print "\nDone...\n"




    
