# Google API Indexer

This script can automatically update and delete URLs via Google Indexing API. Store your service-accounts's json keys in folder `./json_keys` and run script.

### Requirements

- first you need to install requirements:
`pip install -r requirements.txt`

### Usage

```
python3 main.py --help
usage: main.py [-h] [-d] [-i INPUT] [-t {txt_file,database}] [-H HOST] [-U USER] [-P PASSWORD] [-D DATABASE]

options:
  -h, --help            show this help message and exit
  -d, --delete          Delete URLs
  -i INPUT, --input INPUT
                        Path to .csv file with URLs (default ./urls.csv)
  -t {txt_file,database}, --outtype {txt_file,database}
                        Type of result output (default txt_file). Output can be written to a file result.txt or to a MySQL
                        database. If 'database' is selected then host, user, password, and database-name must be specified
  -H HOST, --host HOST  Database's host to connect (default 127.0.0.1)
  -U USER, --user USER  Database's user to connect
  -P PASSWORD, --password PASSWORD
                        Database user's password
  -D DATABASE, --database DATABASE
                        Database to connect
```