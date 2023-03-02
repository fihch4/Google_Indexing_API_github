import argparse
import datetime
from oauth2client.service_account import ServiceAccountCredentials
import httplib2
import json
import os
from script_mysql import MySQLi

def write_result(work_type, url, date):
    if work_type == 'database':
        db = MySQLi(args.host, args.user, args.password, args.database)
        db.commit("INSERT INTO indexing_api (url, date) VALUES (%s, %s)", url_new, datetime.date.today())
    elif work_type == 'txt_file':
        with open('result.txt', 'a', encoding='utf-8') as result_file:
            string_write = f"{url};{date}\n"
            result_file.write(string_write)

def indexURL2(u, http, action):  
    ENDPOINT = "https://indexing.googleapis.com/v3/urlNotifications:publish"
    content = {'url': u.strip(), 'type': action}
    json_ctn = json.dumps(content)
    response, content = http.request(ENDPOINT, method="POST", body=json_ctn)
    result = json.loads(content.decode())
    # For debug purpose only
    if "error" in result:
        print("Error({} - {}): {}".format(result["error"]["code"], result["error"]["status"],
                                          result["error"]["message"]))
        return "Error({} - {}): {}".format(result["error"]["code"], result["error"]["status"],
                                           result["error"]["message"])
    elif action == "URL_UPDATED":
        print("urlNotificationMetadata.url: {}".format(result["urlNotificationMetadata"]["url"]))
        print("urlNotificationMetadata.latestUpdate.url: {}".format(
            result["urlNotificationMetadata"]["latestUpdate"]["url"]))
        print("urlNotificationMetadata.latestUpdate.type: {}".format(
            result["urlNotificationMetadata"]["latestUpdate"]["type"]))
        print("urlNotificationMetadata.latestUpdate.notifyTime: {}".format(
            result["urlNotificationMetadata"]["latestUpdate"]["notifyTime"]))
        return "OK"
    elif action == "URL_DELETED":
        print("urlNotificationMetadata.url: {}".format(result["urlNotificationMetadata"]["url"]))
        print("urlNotificationMetadata.latestRemove.url: {}".format(
            result["urlNotificationMetadata"]["latestRemove"]["url"]))
        print("urlNotificationMetadata.latestRemove.type: {}".format(
            result["urlNotificationMetadata"]["latestRemove"]["type"]))
        print("urlNotificationMetadata.latestRemove.notifyTime: {}".format(
            result["urlNotificationMetadata"]["latestRemove"]["notifyTime"]))
        return "OK"


SCOPES = ["https://www.googleapis.com/auth/indexing"]
count_urls = 0

args_pr = argparse.ArgumentParser()
args_pr.add_argument("-d", "--delete", action='store_const', const=True, required=False, help="Delete URLs")
args_pr.add_argument("-i", "--input", required=False, type=str, default="urls.csv", help="Path to .csv file with URLs (default ./urls.csv)")
args_pr.add_argument("-t", "--outtype", required=False, type=str, choices=["txt_file", "database"], default="txt_file", help="Type of result output (default txt_file). \
    Output can be written to a file result.txt or to a MySQL database. \
    If 'database' is selected then host, user, password, and database-name must be specified")
args_pr.add_argument("-H", "--host", required=False, type=str, default="127.0.0.1", help="Database's host to connect (default 127.0.0.1)")
args_pr.add_argument("-U", "--user", required=False, type=str, help="Database's user to connect")
args_pr.add_argument("-P", "--password", required=False, type=str, help="Database user's password")
args_pr.add_argument("-D", "--database", required=False, type=str, help="Database to connect")
args = args_pr.parse_args()

action = "URL_UPDATED"
if args.delete: action = "URL_DELETED"

for root, dirs, files in os.walk("json_keys"):
    for json_key_path_name in files:
        json_key = 'json_keys/' + json_key_path_name
        credentials = ServiceAccountCredentials.from_json_keyfile_name(json_key, scopes=SCOPES)
        http = credentials.authorize(httplib2.Http())
        a_file = open(args.input, "r")  # get list of lines
        urls = a_file.readlines()
        a_file.close()
        new_file = open(args.input, "w")
        flag = False
        request_google_api = ''
        for url in urls:
            url_new = url.rstrip("\n")
            if flag:
                new_file.write(url)
            else:
                request_google_api = indexURL2(url_new, http, action)
                
            if 'Error' in request_google_api:
                flag = True
                new_file.write(url)
                request_google_api = ''
            else:
                if not flag:
                    write_result(args.outtype, url_new, datetime.date.today())
                    count_urls += 1
                
        new_file.close()

if action == "URL_UPDATED": print("Отправлено на индексацию: " + str(count_urls) + " шт.")
else: print("Отправлено на деиндексацию: " + str(count_urls) + " шт.")