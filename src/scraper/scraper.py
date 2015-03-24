from flavour_parser import FlavourParser

import urllib2
import logging

class Scraper:
  def scrape(self, url):
    try:
      result = urllib2.urlopen(url)
    except:
      logging.error("Could not fetch url")

    html = ''
    for line in result:
      html = html + line
    parser = FlavourParser()
    parser.feed(html)
    self.danver_flavours = parser.danver_flavours
    self.davis_flavours = parser.davis_flavours
    self.delila_flavours = parser.delila_flavours

if __name__ == "__main__":
  url = "http://www.gdcafe.com/website/index.php/Flavours"
  scraper = Scraper()
  scraper.scrape(url)
  print scraper.danver_flavours
  print scraper.davis_flavours
  print scraper.delila_flavours