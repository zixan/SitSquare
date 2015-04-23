from lxml import html as hx
import requests
import time
import random

listing_ids_headers = {'Accept-Encoding': 'gzip, deflate, sdch',
							 'Accept-Language': 'en-US,en;q=0.8,it;q=0.6',
							 'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.90 Safari/537.36',
							 'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
							 'Cache-Control': 'max-age=0', 
							 'Cookie': 'cl_tocmode=sso%3Alist',
							 'Connection': 'keep-alive', 
							 'If-Modified-Since': 'Thu, 23 Apr 2015 01:06:04 GMT'}

listing_headers = {'Accept-Encoding': 'gzip, deflate, sdch', 
						 'Accept-Language': 'en-US,en;q=0.8,it;q=0.6',
						 'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.90 Safari/537.36',
						 'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
						 'Cache-Control': 'max-age=0',
						 'Connection': 'keep-alive',
						 'If-Modified-Since': 'Thu, 23 Apr 2015 01:02:56 GMT'}

for i in range(25): #TODO: get pages count from the first page
	if i == 0:
		listing_ids_url = 'http://losangeles.craigslist.org/search/fuo?postedToday=1&query=furniture&sort=rel'
	else:
		s = str(i * 100)
		listing_ids_url = 'http://losangeles.craigslist.org/search/fuo?postedToday=1&query=furniture&s={}&sort=rel'.format(s)

	listing_ids_obj = requests.get(listing_ids_url, headers=listing_ids_headers)

	if listing_ids_obj.status_code < 400:
		listing_ids_page = listing_ids_obj.text
		listing_ids_hxt = hx.fromstring(listing_ids_page)
		listing_ids = listing_ids_hxt.xpath('//p[@class="row"]/@data-pid')

		for listing_id in listing_ids:
			time.sleep(random.randrange(5,10))
			listing_url = 'http://losangeles.craigslist.org/fb/lax/fuo/{}'.format(listing_id)
			listing_obj = requests.get(listing_url, headers=listing_headers)

			if listing_obj.status_code < 400:
				listing_page = listing_obj.text.encode('utf-8')
				listing_filename = '{}.txt'.format(listing_id)
				open(listing_filename, 'w').write(listing_page)
			else:
				raise Exception('Something went wrong with fetching a listing...')
	else:
		raise Exception('Something went wrong with fetching listing IDs...')