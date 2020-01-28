import requests
import time
import sys
import argparse
import json
from collections import defaultdict
import os
import hashlib

R = '\033[31m'  # red
G = '\033[92m'  # green
C = '\033[36m'  # cyan
W = '\033[0m'  # white

# Prepare command line arguments
desc = "Automatically query the HaveIBeenPwned API with a list of emails to check for associated breaches."

parser = argparse.ArgumentParser(description=desc)
parser.add_argument("--output", "-o", help="File path to output results")
required = parser.add_argument_group('required arguments')
parser.add_argument("--file", "-f", help="File you want to parse emails from", required=True)
parser.add_argument("--key", "-k", help="Your HaveIBeenPwned API key.", required=True)
args = parser.parse_args()

url = "https://haveibeenpwned.com/api/v3/breachedaccount/"
status = ".status"
file_out = args.output
file_in = args.file
doc = defaultdict(int)

hasher = hashlib.md5()
with open(file_in, 'rb') as hashme:
    buf = hashme.read()
    hasher.update(buf)
file_hash = hasher.hexdigest()

with open(file_in, 'r') as f:
    if os.path.exists(status):
        with open(status, "r") as stat:
            stat_data = stat.readline()
            if len(stat_data) > 0:
                stat_hash = stat_data.split(",")[0]
                # Check value in .stats files is a number - not empty value
                if file_hash == stat_hash:
                    stat_val = stat_data.split(",")[1]
                    if stat_val.isnumeric():
                        print(C + "[*] Starting results at previous position: {}".format(stat_val) + W)
                        for lineno, line in enumerate(f):
                            doc[lineno] = line

                        for i in range(int(stat_val)):
                            del doc[i]
                    else:
                        for lineno, line in enumerate(f):
                            doc[lineno] = line
                else:
                    os.remove(status)
            else:
                for lineno, line in enumerate(f):
                    doc[lineno] = line
            stat.close()
    else:
        for lineno, line in enumerate(f):
            doc[lineno] = line

lines = list(doc.keys())[-1]


def check_email(email, counter):

    sys.stdout.write("\r {} of {} emails checked ({}%)\r".format(counter, lines, round(counter * 100 / lines, 1)))

    try:
        response = requests.get(url + email, headers={'hibp-api-key': args.key}, params={'truncateResponse': 'false'}, timeout=10)

        if response.status_code is 200:
            print(G + "[+] Dumps found for {}".format(email) + W)
            json_out = response.content.decode('utf-8', 'ignore')
            simple_out = json.loads(json_out)
            for item in simple_out:
                print(
                        G + '\t-' + C + ' Breach      : ' + W + str(item['Title']) + '\n'
                        + G + '\t-' + C + ' Domain      : ' + W + str(item['Domain']) + '\n'
                        + G + '\t-' + C + ' Date        : ' + W + str(item['BreachDate']) + '\n'
                        + '\t----------------------------\n'
                )
            if file_out is not None:
                store = open(file_name, "a+")
                store.write(email + "\r\n")
                store.close()

        elif response.status_code is 404:
            print(C + "[-] No Dump found for {}".format(email) + W)

        with open(".status", "w") as f:
                f.write("{},{}".format(file_hash, str(counter)))
                f.close()

        time.sleep(1.45) # Required because of API rate limiting to 40 requests per minute.  
    except requests.exceptions.ConnectionError:
        print(R + "[!] Connection refused: status {}".format(response.status_code) + W)

for num, line in doc.items():
    check_email(line.rstrip(), num)
    
os.remove(status)
f.close()


