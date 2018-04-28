import urllib2
import re
from bs4 import BeautifulSoup, Comment
from urlparse import urlparse

'''Initiate array to store discovered links'''
urllist = []

input_url = 'https://googleprojectzero.blogspot.com.au/2018/04/windows-exploitation-tricks-exploiting.html'

def get_tld(our_url):
        parsed_uri = urlparse(our_url)
        
        '''Return the TLD (Top Level Domain) from url'''
        base = '{uri.scheme}://{uri.netloc}'.format(uri=parsed_uri)
        
        return base

def escape_host():
        
        '''Escape TLD for use with regex, i.e http://example\.com'''
        host = re.escape(get_tld(input_url))
        
        return host
        

'''Define opener function to handle requests'''
def opener(myurl, cookiestring=False):
        
        opener = urllib2.build_opener()
        
        if cookiestring != False:
                opener.addheaders = [('Cookie', '%d')] %(cookiestring)
                
                   
        '''Get start link to crawl, this will be returned by cmd line arg in the future'''
        # myurl = 'https://googleprojectzero.blogspot.com.au/2018/04/windows-exploitation-tricks-exploiting.html'
        
        response = opener.open(myurl).read()
        
        return response
        

'''Generate regex string so to only crawl the desired application'''
expressions_string = '''href=["']''' + escape_host() + '''(.[^"']+)["']'''

'''Begin crawling of application'''
for reference in re.findall(expressions_string, opener(input_url), re.I):
        
        '''Ensure that links that already exist in the urllist array are not added again'''
        if reference not in urllist and '#' not in reference:
                urllist.append(reference)
                link = get_tld(input_url) + reference
                print link                

        for layered_reference in re.findall(expressions_string, opener(get_tld(input_url) + reference), re.I):
                
                '''Ensure that link does not contain '#', these links direct to local elements of a page'''      
                if layered_reference not in urllist and '#' not in layered_reference:
                        urllist.append(layered_reference)
                        layered_link = get_tld(input_url) + layered_reference
                        print layered_link                                
        
'''Initate comments array'''
recon_comments = []

'''Begin scraping of comments from crawled links'''
for page in urllist:
        
        '''Generate links to crawl from urllist array'''
        html = opener(get_tld(input_url) + page)

        soup = BeautifulSoup(html,'html.parser')
        
        '''Return the HTML for page and determine comments'''
        for comments in soup.findAll(text=lambda text:isinstance(text, Comment)):
                
                '''Ensure comments that already exist in the recon_comments array are not added again'''
                if comments.extract() not in recon_comments:
                        
                        recon_comments.append(comments.extract())
                        print comments.extract()
