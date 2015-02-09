# prepare a table row for .CSV here
def generateCSVstring(dic, utf8 = False):
    st = ""; br = "; "; em = " "
    if utf8:
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
                #print "encode:", dic["role"].encode("utf8"), "\n"
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
    else:    
        try:
            st += dic["fn"] + br
        except:
            st += em + br
        try:
            st += dic["nickname"] + br
        except:
            st += em + br
        try:
            if isinstance(dic["role"], list):
                for role in dic["role"]:
                    st += role + ", "
                st += br
            else:
                st += dic["role"] + br
        except:
            st += em + br
        try:
            st += dic["bday"] + br
        except:
            st += em + br
        try:
            st += dic["dday deathdate"] + br
        except:
            st += em + br
        try:
            st += dic["link"]
        except:
            st += em
    return st + "\n"


# actually do a save
def do_saving(dict_to_save, file_set, log = False):
    try: 
        ofile = open("output/output{0}.csv".format(file_set), "a")
    except: 
        ofile = open("output/output{0}.csv".format(file_set), "w")
    lis = generateCSVstring(dict_to_save, utf8 = False)
    ofile.write(lis)
    ofile.close()
    if log:
        print "saved one"
