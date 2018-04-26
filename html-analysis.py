import urllib2
from bs4 import BeautifulSoup, Comment
import re, urllib

urllist = []

myurl = 'https://googleprojectzero.blogspot.com.au/2018/04/windows-exploitation-tricks-exploiting.html'
host = 'https://googleprojectzero\.blogspot\.com\.au'
base = 'https://googleprojectzero.blogspot.com.au'

expressions_string = '''href=["']''' + host + '''(.[^"']+)["']'''

for reference in re.findall(expressions_string, urllib.urlopen(myurl).read(), re.I):
        
        if reference not in urllist and '#' not in reference and 'search?' not in reference:
                urllist.append(reference)
                link = base + reference
                print link                

        for layered_reference in re.findall(expressions_string, urllib.urlopen(base + reference).read(), re.I):
                        
                if layered_reference not in urllist and '#' not in layered_reference:
                        urllist.append(layered_reference)
                        layered_link = base + layered_reference
                        print layered_link                                
        
recon_comments = []

for page in urllist:
        link = urllib2.urlopen(base + page)
        html = link.read()

        soup = BeautifulSoup(html,'html.parser')

        for comments in soup.findAll(text=lambda text:isinstance(text, Comment)):
                
                # comment_length = len(comments.extract())
                if comments.extract() not in recon_comments:
                        
                        recon_comments.append(comments.extract())
                        print comments.extract()
                
                # print '-' * comment_length
                # print '\n'
    
