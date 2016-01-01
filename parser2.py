# -*- coding: utf-8 -*-
import sys

import requests
from bs4 import BeautifulSoup as bs

from saving import do_saving, format_exception
from config import links

reload(sys)
sys.setdefaultencoding("utf8")


def parseOtherSite(page_link):
    template = []
    append = template.append
    headers = {"User-agent": "Mozilla/5.0"}
    try:
        # ol -> li
        r = requests.get(page_link, headers=headers, timeout=10)
        soup = bs(r.text)
        find_ol = soup.find_all("ol")
        print "Current page has {0} <ol>-tags".format(len(find_ol))
        for ol_tag in find_ol:
            sub_soup = bs(str(ol_tag))
            find_li = soup.find_all("li", class_="")
            print "Current page has {0} <li>-tags".format(len(find_li))
            for li_tag in find_li:
                buf = str(li_tag)
                sub_res = []
                sub_pend = sub_res.append

                a = buf.find('href="')
                buf = buf[a:]
                a = buf.find('href="') + len('href="')
                buf = buf[a:]
                b = buf.find('"')
                href = buf[:b]
                buf = buf[b + 2:]
                sub_pend(href)

                while buf.find("<") != -1 and buf.find(">") != -1:
                    a = buf.find("<")
                    b = buf.find(">")
                    buf = buf[:a] + buf[b + 1:]
                sub_pend(buf)
                append(sub_res)  # whole current table
    except Exception as ex:
        print "(parseOtherSite, r)", format_exception(ex)
        print "--" * 25
    return template


if __name__ == "__main__":
    file_set = "10"
    main_domain = "http://www.biographyonline.net"
    numerals = "0123456789"
    print "Found {0} links on {1} file-set...".format(len(links[file_set]), file_set)

    already_saved = []
    append = already_saved.append
    for link in links[file_set]:
        j = 0  # stats
        res = parseOtherSite(link)
        print ""
        for item in res:
            # 1 item == 1 man: item[0] - link, item[1] - data....
            link = item[0]
            a = link.find("/")
            link = link[a:]
            if len(link) > 0:
                link = main_domain + link
                data = {}
                data["link"] = link

                p_data = item[1]  # name ... ( b day .... d day ) ... role
                a = p_data.find("(")
                if a != -1:
                    fn = p_data[:a]
                    data["fn"] = fn
                    p_data = p_data[a + 1:]

                    a = p_data.find(")")
                    dates = p_data[:a]
                    data["role"] = p_data[a + 1:]

                    bday = ""
                    dday = ""
                    i = 0
                    f = 0
                    while i < len(dates):
                        char = dates[i]
                        if char in numerals and f == 0:
                            bday += char
                            f = 1
                        elif char in numerals and f == 1:
                            bday += char
                        elif char in numerals and f == 2:
                            dday += char
                        else:
                            f = 2
                        i += 1
                    data["bday"] = bday
                    data["dday deathdate"] = dday

                    # save it :)
                    if data not in already_saved:
                        append(data)
                        do_saving(data, file_set)
                        j += 1
        print "\n\nactually datas: {0}\n".format(j)
    print "\nDone..."
