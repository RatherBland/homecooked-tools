import requests
import time
import sys
import mmap
import argparse

R = '\033[31m'  # red
G = '\033[32m'  # green
C = '\033[36m'  # cyan
W = '\033[0m'  # white

desc = "Automatically query the HaveIBeenPwned API with a list of emails to check for associated breaches."

parser = argparse.ArgumentParser(description=desc)
parser.add_argument("--output", "-o", help="File path to output results")
required = parser.add_argument_group('required arguments')
parser.add_argument("--file", "-f", help="File you want to parse emails from", required=True)
parser.add_argument("--key", "-k", help="Your HaveIBeenPwned API key.", required=True)
args = parser.parse_args()

url = "https://haveibeenpwned.com/api/v3/breachedaccount/"
yes = []
failed = []


file_name = args.output


def mapcount():
    f = open(args.file, "r+")
    buf = mmap.mmap(f.fileno(), 0)
    lines = 0
    readline = buf.readline
    while readline():
        lines += 1
    return lines


lines = mapcount()

f = open(args.file, "r+")

counter = 0


def check_email(email):
    global counter
    counter += 1
    sys.stdout.write("\r{} of {} emails checked ({}%)\r".format(counter, lines, round(counter * 100 / lines, 1)))
    try:
        response = requests.get(url + email, headers={'hibp-api-key': args.key})

        if response.status_code is 200:
            print(G + "[+] Dumps found for {}".format(email) + W)
            yes.append(email)
            if args.output is not None:
                store = open(file_name, "a+")
                store.write(email + "\r\n")
                store.close()

        elif response.status_code is 404:
            print(C + "[-] No Dump found for {}".format(email) + W)


        time.sleep(1.45) # Required because of API rate limiting to 40 requests per 60 seconds
    except requests.exceptions.ConnectionError:
        failed.append(email)
        print(R + "[!] Connection refused: status {}".format(response.status_code) + W)


for email in f.readlines():
    check_email(email.strip())
if len(failed) > 0:
    for email in failed:
        check_email(email)
print(yes)
print(failed)
f.close()
