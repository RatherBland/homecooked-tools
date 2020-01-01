import sys, argparse

desc = "Create permutations of possible emails from first and lastname combinations.\n" \
       "Example: python3 {} --file names.txt --domain example.com --output results.txt".format(sys.argv[0])

parser = argparse.ArgumentParser(description = desc)
parser.add_argument("--output", "-o", help="File path to output results")
required = parser.add_argument_group('required arguments')
parser.add_argument("--file", "-f", help="File you want to parse names from", required=True)
parser.add_argument("--domain", "-d", help="Email domain that should be appended", required=True)
args = parser.parse_args()

f = open(args.file, "r")

results = []


def generate_emails(name, domain):
    if 3 > len(name.split()) > 1:

        fnln = name.split()[0] + name.split()[1] + "@" + domain
        fnpln = name.split()[0] + "." + name.split()[1] + "@" + domain
        fn1c = name.split()[0] + name.split()[1][:1] + "@" + domain
        fnp1c = name.split()[0] + "." + name.split()[1][:1] + "@" + domain
        fn2c = name.split()[0] + name.split()[1][:2] + "@" + domain
        fnp2c = name.split()[0] + "." + name.split()[1][:2] + "@" + domain
        fn3c = name.split()[0] + name.split()[1][:3] + "@" + domain
        fnp3c = name.split()[0] + "." + name.split()[1][:3] + "@" + domain
        fn = name.split()[0] + "@" + domain
        flln = name.split()[0][:1] + name.split()[1] + "@" + domain
        flpln = name.split()[0][:1] + "." + name.split()[1] + "@" + domain

        results.extend([fnln, fnpln, fn1c, fnp1c, fn2c, fnp2c, fn3c, fnp3c, fn, flln, flpln])

        if args.output is not None:
            store = open(args.output, "a+")
            store.write("{}\n{}\n{}\n{}\n{}\n{}\n{}\n{}\n{}\n{}\n{}\n".format(fnln,fnpln,fn1c,fnp1c,fn2c,fnp2c,fn3c,fnp3c,fn,flln,flpln))
            store.close()

        else:

            print(fnln)
            print(fnpln)
            print(fn1c)
            print(fnp1c)
            print(fn2c)
            print(fnp2c)
            print(fn3c)
            print(fnp3c)
            print(fn)
            print(flln)
            print(flpln)


for name in f.readlines():
    generate_emails(name, args.domain)

print("{} lines output to {}".format(len(results), args.output))

f.close()
