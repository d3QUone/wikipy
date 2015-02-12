# -*- coding: utf-8 -*-
import requests, sys
from bs4 import BeautifulSoup as bs
from datetime import datetime
from saving import do_saving, format_exception

headers = {"User-agent": "Mozilla/5.0"}

# get links from lists on any site - OK
def parse_other_site(page_link):
    template = []
    append = template.append
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
        print "(parse_other_site, r)", format_exception(ex)
        print "--"*25
    return template


# you can run it manually to get parse_endpoints lists - OK
def find_all_sections(endpoint):
    x = parse_other_site(endpoint)
    return ["http:" + i[0] for i in x if len(i[0]) > 0]


# get links - OK
def parse_famous_names(endpoint):
    try:
        links = []
        append = links.append
        saved = 0; repeat = 0
        page = 1
        while page < 6: # the hugest category has 5 pages
            r = requests.get(endpoint + "?page={0}".format(page), headers=headers, timeout = 10)
            page += 1
            soup = bs(r.text)
            people = soup.find_all("div", class_="main_cat_profile_box")
            for item in people:
                buf = str(item)
                a = buf.find('href="')
                buf = buf[a+len('href="'):]
                a = buf.find('"')
                link = "http:" + buf[:a]
                if link not in links:
                    append(link)
                    saved += 1
                else:
                    repeat += 1
                if repeat > 0 and repeat > saved:
                    page = 6
                    break
        print "saved {0} links, repeats on {1}+".format(saved, repeat)
        return links
    except Exception as ex:
        print "(parse_famous_names, r)", format_exception(ex)
        return []


# returns clear text
def remove_tags(string):
    buf = str(string)
    while buf.find("<") != -1 and buf.find(">") != -1:
        a = buf.find("<")
        b = buf.find(">")
        buf = buf[:a] + buf[b+1:]
    buf = buf.replace("&amp;", "&").split(" AD") # cause fuck it
    return buf[0]


def get_personal_data(endpoint):
    try:
        r = requests.get(endpoint, headers=headers, timeout = 10)
        soup = bs(r.text)
        # get full name
        name_block = str(soup.find_all("h1")[0])
        a = name_block.find("<h1>")
        b = name_block.find("<span")
        name = name_block[a+len("<h1>"):b-1] # b-1 cause have the trailing space
        data = {}
        data["fn"] = name
        data["link"] = endpoint
        # get all other datas
        quick_right = soup.find_all("div", class_="quick_right")
        quick_left = soup.find_all("div", class_="quick_left")
        len_quick_left = len(quick_left)

        key_words = {"Born on": "bday", "Died": "dday deathdate", "Famous": "role", "Found": "role"}
        keys = key_words.keys()
        data["role"] = ""

        j = 0
        while j < len_quick_left:
            buf = remove_tags(quick_left[j])
            for cat in keys:
                if cat in buf:
                    if key_words[cat] == "role":
                        data["role"] += remove_tags(quick_right[j]) + ", "
                    else:
                        data[key_words[cat]] = remove_tags(quick_right[j])
            j += 1

        if data["role"] == "":
            return None
        else:
            data["role"] = data["role"][:-2] # delete last ', '
            return data
    except Exception as ex:
        print "(get_personal_data, r)", format_exception(ex)
        return None


if __name__ == "__main__":
    # parse_endpoints = find_all_sections("http://www.thefamouspeople.com/") # but static links are better :)
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
    file_set = "12full"
    
    saved = 0; rep = 0
    already_saved = []
    append = already_saved.append
    for endpoint in parse_endpoints:
        set_of_links = parse_famous_names(endpoint)
        for sub_link in set_of_links:
            personal_data = get_personal_data(sub_link)
            if personal_data and personal_data not in already_saved:
                append(personal_data)
                do_saving(personal_data, file_set)
                saved += 1
            else:
                rep += 1
        #break
    print "\nsaved {0} people, {1} canceled".format(saved, rep)
