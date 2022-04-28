from subprocess import PIPE, Popen
import requests
import webbrowser

def execute_return(cmd):
    args = cmd.split(" ")
    proc = Popen(args,stdout=PIPE,stderr=PIPE) #initialise from Popen and create output and error pipe stream
    out ,err = proc.communicate() # fetch output and error code
    return out,err


def make_req(error): # to take the error message and make a request to the stack exchange api 
    resp = requests.get("https://api.stackexchange.com/"+"/2.3/search?order=desc&sort=activity&tagged=python&intitle={}&site=stackoverflow".format(error))
    return resp.json() # return the respective json for that error


def get_urls(json_dict):
    url_list = []
    count = 0
    for i in json_dict["items"]: # the json in stack exchange has a dictionary with key called items. here we iterate through all items in the dict
        if i["is_answered"]: # only add the link to the list if the question is answered on stack exchange
            url_list.append(i["link"])
        count +=1
        if count == 3: # the json list counld be very long so only doing 3 loops here
            break
        for i in url_list: 
            webbrowser.open(i) # will open the links in the browser


op,err = execute_return("python test2.py") # the file whose error is to be checked ----> " python <filename>.py "
error_message = err.decode("utf-8").strip().split("\r\n")[-1] #convert from binary object to utf-8 a string object and split it based on \r\n
print(error_message)
if error_message: # if error message exists
    filter_err = error_message.split(":")
    json1 = make_req(filter_err[0]) # use only the type of the error
    json2 = make_req(filter_err[1]) # to make sure we get better results
    json3 = make_req(error_message) # the entirety of the error message
    get_urls(json1)
    get_urls(json2)
    get_urls(json3)
else:
    print("No error found!")