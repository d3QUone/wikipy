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


def parse_other_site(page_link):
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


# you can run it manually to get parse_endpoints lists
def find_all_sections(endpoint):
    x = parse_other_site(endpoint)
    return ["http:" + i[0] for i in x if len(i[0]) > 0]


# return link by name
def do_wiki_search(name):
    # search_endpoint = "http://en.wikipedia.org/"
    return ""


def parse_current_person(link):
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


if __name__ == "__main__":
    # parse_endpoints = find_all_sections("http://www.thefamouspeople.com/")
    # but static links are better :)
    parse_endpoints = ['http://www.thefamouspeople.com/activists.php',
                       'http://www.thefamouspeople.com/business-people.php',
                       'http://www.thefamouspeople.com/criminals.php',
                       'http://www.thefamouspeople.com/dancers.php',
                       'http://www.thefamouspeople.com/engineers.php',
                       'http://www.thefamouspeople.com/fashion.php',
                       'http://www.thefamouspeople.com/film-theater-personalities.php',
                       'http://www.thefamouspeople.com/food-experts.php',
                       'http://www.thefamouspeople.com/intellectuals-academics.php',
                       'http://www.thefamouspeople.com/inventors-discoverers.php',
                       'http://www.thefamouspeople.com/lawyers-judges.php',
                       'http://www.thefamouspeople.com/leaders.php',
                       'http://www.thefamouspeople.com/media-personalities.php',
                       'http://www.thefamouspeople.com/musicians.php',
                       'http://www.thefamouspeople.com/painters.php',
                       'http://www.thefamouspeople.com/photographers.php',
                       'http://www.thefamouspeople.com/physicians.php',
                       'http://www.thefamouspeople.com/scientists.php',
                       'http://www.thefamouspeople.com/singers.php',
                       'http://www.thefamouspeople.com/sports-persons.php',
                       'http://www.thefamouspeople.com/writers.php',
                       'http://www.thefamouspeople.com/others.php',
                       'http://www.thefamouspeople.com/famous-people-by-zodiac-sign.php',
                       'http://www.thefamouspeople.com/famous-people-by-country.php',
                       'http://www.thefamouspeople.com/famous-people-by-birthday.php']
    
    already_saved = []
    append = already_saved.append

    '''
    for link in links[file_set]:
        res = parseOtherSite(link)
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
    