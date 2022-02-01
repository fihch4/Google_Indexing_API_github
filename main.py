import datetime
from oauth2client.service_account import ServiceAccountCredentials
import httplib2
import json
import os
from script_mysql import MySQLi

from config import *
"""
pip install google-api-python-client oauth2client
pip install --upgrade oauth2client
"""

SCOPES = ["https://www.googleapis.com/auth/indexing"]


def indexURL2(u, http):
    ENDPOINT = "https://indexing.googleapis.com/v3/urlNotifications:publish"
    content = {'url': u.strip(), 'type': "URL_UPDATED"}
    json_ctn = json.dumps(content)
    response, content = http.request(ENDPOINT, method="POST", body=json_ctn)
    result = json.loads(content.decode())
    # For debug purpose only
    if "error" in result:
        print("Error({} - {}): {}".format(result["error"]["code"], result["error"]["status"],
                                          result["error"]["message"]))
        return "Error({} - {}): {}".format(result["error"]["code"], result["error"]["status"],
                                           result["error"]["message"])
    else:
        print("urlNotificationMetadata.url: {}".format(result["urlNotificationMetadata"]["url"]))
        print("urlNotificationMetadata.latestUpdate.url: {}".format(
            result["urlNotificationMetadata"]["latestUpdate"]["url"]))
        print("urlNotificationMetadata.latestUpdate.type: {}".format(
            result["urlNotificationMetadata"]["latestUpdate"]["type"]))
        print("urlNotificationMetadata.latestUpdate.notifyTime: {}".format(
            result["urlNotificationMetadata"]["latestUpdate"]["notifyTime"]))
        return "OK"


count_urls = 0
for root, dirs, files in os.walk("json_keys"):
    for json_key_path_name in files:
        json_key = 'json_keys/' + json_key_path_name
        credentials = ServiceAccountCredentials.from_json_keyfile_name(json_key, scopes=SCOPES)
        http = credentials.authorize(httplib2.Http())
        a_file = open("urls.csv", "r")  # get list of lines
        urls = a_file.readlines()
        a_file.close()
        new_file = open("urls.csv", "w")
        flag = False
        request_google_api = ''
        for url in urls:
            url_new = url.rstrip("\n")
            if flag:
                new_file.write(url)
            else:
                request_google_api = indexURL2(url_new, http)
                db = MySQLi(host, user, password, database_home)
                db.commit("INSERT INTO indexing_api (url, seo_id, date) VALUES (%s, %s, %s)", url_new,
                          int('999999'), datetime.date.today())

                count_urls += 1
            if 'Error' in request_google_api:
                flag = True
                new_file.write(url)
                request_google_api = ''
                count_urls -= 1
        new_file.close()

print("Отправлено на индексацию: " + str(count_urls) + " шт.")
