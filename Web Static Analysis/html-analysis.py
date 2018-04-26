import urllib2
import re
from bs4 import BeautifulSoup, Comment
from urlparse import urlparse

# Initiate array to store discovered links
urllist = []

# Get start link to crawl, this will be returned by cmd arg in the future
myurl = 'https://googleprojectzero.blogspot.com.au/2018/04/windows-exploitation-tricks-exploiting.html'
parsed_uri = urlparse(myurl)
# Return the TLD from url
base = '{uri.scheme}://{uri.netloc}'.format(uri=parsed_uri)
# Escape TLD for use with regex, i.e http://example\.com
host = re.escape(base)

# Generate regex string so to only crawl the desired application
expressions_string = '''href=["']''' + host + '''(.[^"']+)["']'''

# Begin crawling of application
for reference in re.findall(expressions_string, urllib2.urlopen(myurl).read(), re.I):
        
        # Ensure that links that already exist in the urllist array are not added again
        if reference not in urllist and '#' not in reference and 'search?' not in reference:
                urllist.append(reference)
                link = base + reference
                print link                

        for layered_reference in re.findall(expressions_string, urllib2.urlopen(base + reference).read(), re.I):
                
                # Ensure that link does not contain '#', these links direct to local elements of a page        
                if layered_reference not in urllist and '#' not in layered_reference:
                        urllist.append(layered_reference)
                        layered_link = base + layered_reference
                        print layered_link                                
        
# Initate comments array
recon_comments = []

# Begin scraping of comments from crawled links
for page in urllist:
        
        # Generate links to crawl from urllist array
        link = urllib2.urlopen(base + page)
        html = link.read()

        soup = BeautifulSoup(html,'html.parser')
        
        # Return the HTML for page and determine comments
        for comments in soup.findAll(text=lambda text:isinstance(text, Comment)):
                
                # Ensure comments that already exist in the recon_comments array are not added again
                if comments.extract() not in recon_comments:
                        
                        recon_comments.append(comments.extract())
                        print comments.extract()
