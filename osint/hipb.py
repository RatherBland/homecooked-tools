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

"""Prepare command line arguments"""
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

"""Get the MD5 hash of file being read to compare against progress file"""
hasher = hashlib.md5()
with open(file_in, 'rb') as hashme:
    buf = hashme.read()
    hasher.update(buf)
file_hash = hasher.hexdigest()

with open(file_in, 'r') as f:
    """Check if progress file exists"""
    if os.path.exists(status):
        with open(status, "r") as stat:
            stat_data = stat.readline()
            """Check if there is data in progress file"""
            if len(stat_data) > 0:
                stat_hash = stat_data.split(",")[0]
                """Check value in .stats files is a number - not empty value"""
                if file_hash == stat_hash:
                    stat_val = stat_data.split(",")[1]
                    if stat_val.isnumeric():
                        print(C + "[*] Starting results at previous position: {}".format(stat_val) + W)
                        for lineno, line in enumerate(f):
                            doc[lineno] = line
                        """Remove keys that have been previously checked"""
                        for i in range(int(stat_val)):
                            del doc[i]
                    else:
                        os.remove(status)
                        for lineno, line in enumerate(f):
                            doc[lineno] = line

                    """In the event, the hash for the current input file, and hash in the status file don't match. It would indicate that a different file is being read, or the file hash now changed. Either way, the status file would no longer be valid to use so it is deleted."""
                else:
                    os.remove(status)
                    for lineno, line in enumerate(f):
                        doc[lineno] = line

            else:
                for lineno, line in enumerate(f):
                    doc[lineno] = line
            stat.close()
    else:
        for lineno, line in enumerate(f):
            doc[lineno] = line

"""Get total number of lines in file"""
lines = list(doc.keys())[-1]


def check_email(email, counter):
    """Provide consistent feedback to user in the form of status bar"""
    sys.stdout.write("\r {} of {} emails checked ({}%)\r".format(counter, lines, round(counter * 100 / lines, 1)))

    try:
        """Attempt request to API parsing email as POST data, with API key as header. truncateResponse set to false in headers to return for JSON response, instead of yes/no response."""
        response = requests.get(url + email, headers={'hibp-api-key': args.key}, params={'truncateResponse': 'false'},
                                timeout=10)

        """Status 200 indicates dump for email found. Parse JSON response to output Org breached, and date."""
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
                store = open(file_out, "a+")
                store.write(email + "\r\n")
                store.close()

        elif response.status_code is 404:
            print(C + "[-] No Dump found for {}".format(email) + W)

        """Update status file with progress of file enuemeration so we don't need to start from the beginning in the event execution is cancelled/fails early"""
        with open(".status", "w") as f:
            f.write("{},{}".format(file_hash, str(counter)))
            f.close()

        time.sleep(1.45)
        """Required because of API rate limiting to 40 requests per minute."""
    except requests.exceptions.ConnectionError:
        print(R + "[!] Connection refused: status {}".format(response.status_code) + W)


for num, line in doc.items():
    check_email(line.rstrip(), num)

"""Remove status file at the successful end of execution"""
os.remove(status)
f.close()

