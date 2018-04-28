import urllib2, re
from bs4 import BeautifulSoup, Comment
from urlparse import urlparse

'''Get start link to crawl, this will be returned by cmd line arg in the future'''
input_url = 'https://googleprojectzero.blogspot.com.au/2018/04/windows-exploitation-tricks-exploiting.html'

'''Initiate array to store discovered links'''
urllist = []

'''Initate array to store comments'''
recon_comments = []

'''Define get_tld to retrieve the top level domain from inputted URL'''
def get_tld(our_url):
        parsed_uri = urlparse(our_url)
        
        '''Return the TLD (Top Level Domain) from url'''
        base = '{uri.scheme}://{uri.netloc}'.format(uri=parsed_uri)
        
        return base

'''Define escape_host function to handle the regex string compatability of url'''
def escape_host():
        
        '''Escape TLD for use with regex, i.e http://example\.com'''
        host = re.escape(get_tld(input_url))
        
        return host
        
'''Define opener function to handle requests'''
def opener(myurl, cookiestring=False):
        
        opener = urllib2.build_opener()
        
        if cookiestring != False:
                opener.addheaders = [('Cookie', '%d')] %(cookiestring)
                
        response = opener.open(myurl).read()
        return response

'''Define get_comments function to handle the discovery of comments in HTML code'''
def get_comments(link):
        
        html = opener(link)
        soup = BeautifulSoup(html,'html.parser')

        '''Return the HTML for page and determine comments'''
        for comments in soup.findAll(text=lambda text:isinstance(text, Comment)):
                
                print comments.extract()
                
                '''Ensure comments that already exist in the recon_comments array are not added again'''
                if comments.extract() not in recon_comments:
                        
                        recon_comments.append(comments.extract())
                        
'''Generate regex string so to only crawl the desired application'''
expressions_string = '''href=["']''' + escape_host() + '''(.[^"']+)["']'''

'''Begin crawling of application'''
for reference in re.findall(expressions_string, opener(input_url), re.I):
        
        '''Ensure that links that already exist in the urllist array are not added again'''
        if reference not in urllist and '#' not in reference:
                
                urllist.append(reference)
                link = get_tld(input_url) + reference
                print link

                get_comments(link)
                        
        for layered_reference in re.findall(expressions_string, opener(get_tld(input_url) + reference), re.I):
                
                '''Ensure that link does not contain '#', these links direct to local elements of a page'''      
                if layered_reference not in urllist and '#' not in layered_reference:
                        
                        urllist.append(layered_reference)
                        layered_link = get_tld(input_url) + layered_reference
                        print layered_link                                
                        
                        get_comments(layered_link)