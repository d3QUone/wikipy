# -*- coding: utf-8 -*-
import requests, sys, json, traceback
from bs4 import BeautifulSoup as bs
from datetime import datetime

from saving import do_saving
from config import links

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
        print "(parseOtherSite, r)", format_exception(ex)
        print "--"*25
    return template
    

           
if __name__ == "__main__":
    file_set = "9" 

    already_saved = []
    append = already_saved.append
    for link in links[file_set]:
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




    
