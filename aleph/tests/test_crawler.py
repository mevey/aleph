<<<<<<< HEAD
import requests
from aleph.tests.util import TestCase
from aleph.crawlers import blacklight


=======
from aleph.tests.util import TestCase
from aleph.crawlers.crawler import Crawler
from aleph.crawlers import blacklight

>>>>>>> 4f4f17409bacc3303038390a5857eae8ac2d9d5c
class CrawlersTestCase(TestCase):

    def setUp(self):
        super(CrawlersTestCase, self).setUp()
        self.demo_url = "http://demo.projectblacklight.org/"
<<<<<<< HEAD
        self.bl = blacklight.BlacklightCrawler()
        self.pagecount = self.bl.get_page_count(self.demo_url)
=======
        self.bl = blacklight.BlacklightCrawler(Crawler)
        
>>>>>>> 4f4f17409bacc3303038390a5857eae8ac2d9d5c

    def test_blacklight_crawldocument(self,):
        resp = self.bl.crawl_document(self.demo_url, '1')
        self.assertIsInstance(resp, bool)
        self.assertEqual(resp, True)

    def test_blacklight_get_page_count(self,):
<<<<<<< HEAD
        self.assertTrue(str(self.pagecount).isdigit())

    def test_blacklight_sources(self,):
        for site in blacklight.SITES:
            resp = requests.get(site + 'catalog.json')
            self.assertEqual(resp.status_code, 200)
            data = resp.json()
            try:
                pagecount = data['response']['pages']['total_count']
            except:
                pagecount = 0
            if not self.pagecount == 0:
                self.assertIn('response', data)
                self.assertIn('pages', data['response'])
                self.assertIn('total_count', data['response']['pages'])

    '''
    def test_blacklight_crawlpage(self,):
        for site in blacklight.SITES:
            url = site + 'catalog.json'
            resp = requests.get(url)
            self.assertEqual(resp.status_code, 200)
            data = resp.json()
            try:
                pagecount = data['response']['pages']['total_count']
                page = random.randint(0, pagecount)
                pageresp = requests.get(url + '?page={}'.format(page))
                print page
                pageresp = pageresp.json()
                self.assertIn('response', pageresp)
                self.assertIn('docs', pageresp['response'])
            except KeyError:
                pass
                '''
=======
        resp = self.bl.get_page_count(self.demo_url)
        self.assertTrue(str(resp).isdigit())
>>>>>>> 4f4f17409bacc3303038390a5857eae8ac2d9d5c
