import sys
import traceback


def format_exception(e):
    """Track the error in the caught exception"""
    print "{} - given into traceback".format(e)
    exception_list = traceback.format_stack()
    exception_list = exception_list[:-2]
    exception_list.extend(traceback.format_tb(sys.exc_info()[2]))
    exception_list.extend(traceback.format_exception_only(sys.exc_info()[0], sys.exc_info()[1]))
    exception_str = "Traceback (most recent call last):\n"
    exception_str += "".join(exception_list)
    exception_str = exception_str[:-1]
    return exception_str + "\n" + "-"*15


def generateCSVstring(dic, utf8=False):
    """Prepare a table row for .CSV"""
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
    return st + "\n"


def do_saving(dict_to_save, file_set, log=False):
    lis = generateCSVstring(dict_to_save, utf8 = False)
    with open("output/output{0}.csv".format(file_set), "a") as ofile:
        ofile.write(lis)
    if log:
        print "saved one"
