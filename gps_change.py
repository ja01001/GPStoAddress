import requests
import xml.etree.ElementTree as tr
import json

APIKEYID = ""
APIKEY = ""
def getAPIKEY():
    with open("key.json") as api_json:
        json_data = json.load(api_json)
        APIKEYID = json_data["APIKEYID"]
        APIKEY = json_data["APIKEY"]
    api_json.close()
    return APIKEY, APIKEYID
def changeGPStoAddr(data):
    firstUrl = "https://naveropenapi.apigw.ntruss.com/map-reversegeocode/v2/gc?request=coordsToaddr&coords="
    lastUrl = "&output=xml&orders=roadaddr"
    lastUrl2 = "&output=xml&orders=addr"
    headers = {"X-NCP-APIGW-API-KEY-ID": APIKEYID, "X-NCP-APIGW-API-KEY":APIKEY}
    gpsData = str(data[0])+","+str(data[1])
    url = firstUrl+gpsData+lastUrl
    response = requests.get(url, headers=headers)
    root = tr.fromstring(response.text)
    result = ''
    flag = True
    for strs in root.iter('name'):
        if strs.text == "no results":
            flag = False
    if flag :
        for strs in root.iter('results'):
            for name in strs.iter('name'):
                if(name.text != "roadaddr" and name.text != "kr"):
                   result += name.text+" "
            for road in strs.iter('number1'):
                result += road.text
    else:
        response2 = requests.get(firstUrl+gpsData+lastUrl2, headers=headers)
        roots = tr.fromstring(response2.text)

        for strs in roots.iter('name'):

            if (strs.text != "addr" and strs.text != "kr" and strs.text != None and strs.text != 'ok'):
                result += strs.text+" "

        for strs in roots.iter('number1'):
            if(strs.text != None) :
                result += strs.text
        for strs in roots.iter('number2'):
            if (strs.text != None):
                result += "-"+strs.text
    return result

if __name__ == '__main__':
    if(APIKEY == ""):
        keys = getAPIKEY()
        APIKEYID = keys[1]
        APIKEY = keys[0]
    f = open('gps.txt', mode='r', encoding='utf-8')
    q = f.readlines()
    f2 = open('convert.txt', mode='w+', encoding='utf-8')
    cnt = 0
    for item in q:
        item =item.replace("\n", "")
        aa = item.split("\t")
        items = [0, 0]
        items[0] = float(aa[0].replace("[", "").strip())
        items[1] = float(aa[1].replace("]", "").strip())
        a = changeGPStoAddr(items)
        cnt += 1
        print(cnt)
        f2.write(a+"\n")

    f2.close()
    f.close()
