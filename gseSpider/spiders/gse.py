import scrapy
import csv
import re
from bs4 import BeautifulSoup
from lxml import etree
from gseSpider.items import GsespiderItem


class GseSpider(scrapy.Spider):
    name = 'gse'
    allowed_domains = ['www.ncbi.nlm.nih.gov']
    start_urls = ['https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE107712']
    url_head = 'https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc='

    def start_requests(self):
        GSEs = []
        with open(r'C:\Users\QiTianM425\Desktop\gsm_num.csv', 'r', encoding='UTF-8') as csvfile:
            csv_reader = csv.reader(csvfile)
            for row in csv_reader:
                GSEs.append(row[4])
        for i in GSEs:
            url = self.url_head + str(i)
            item = GsespiderItem()
            item["GSE_num"] = i
            yield scrapy.Request(url=url, meta={'item': item}, callback=self.parse)

    def parse(self, response):
        soup = BeautifulSoup(response.text, "lxml")
        contents = soup.find_all("tr", valign="top")
        bot = len(contents)
        for i in range(1, 3):
            html = etree.HTML(str(contents[i]))
            if i == 1:
                Status = html.xpath('//tr[@valign = "top"]/td[position()>1]/text()')[0]
            else:
                Title = html.xpath('//tr[@valign = "top"]/td[position()>1]/text()')[0]
        Sample = []
        Organisms = []
        for i in range(3, bot):
            P = []
            S = []
            pat1 = 'organism'
            pat2 = 'Experiment type'
            pat3 = 'Summary'
            pat4 = 'Overall design'
            pat5 = 'Platforms'
            pat6 = 'Samples'
            A = re.search(pat1, str(contents[i]))
            B = re.search(pat2, str(contents[i]))
            C = re.search(pat3, str(contents[i]))
            D = re.search(pat4, str(contents[i]))
            E = re.search(pat5, str(contents[i]))
            F = re.search(pat6, str(contents[i]))
            if A:
                html = etree.HTML(str(contents[i]))
                a = html.xpath('//tr[@valign = "top"]/td[position()>1]/a/text()')
                Organisms = ', '.join(a)
            if B:
                html = etree.HTML(str(contents[i]))
                ExpType = html.xpath('//tr[@valign = "top"]/td[position()>1]/text()')[0]
            if C:
                html = etree.HTML(str(contents[i]))
                Summary = html.xpath('//tr[@valign = "top"]/td[position()>1]/text()')
                link = html.xpath('//tr[@valign = "top"]/td[position()>1]/a/text()')
                if link:
                    Summary = Summary + link
                Summary = ', '.join(Summary)
            if D:
                html = etree.HTML(str(contents[i]))
                try:
                    OverallDesign = html.xpath('//tr[@valign = "top"]/td[2]/text()')[0]
                except IndexError:
                    OverallDesign = html.xpath('//tr[@valign = "top"]/td/a/text()')[0]
            if E:
                html = etree.HTML(str(contents[i]))
                a1 = html.xpath('//td[@valign = "top"]/a/text()')
                a2 = html.xpath('//td[@valign = "top"]/text()')
                for x in range(0, len(a1)):
                    E = a1[x] + ' ' + a2[x]
                    P.append(E)
                Platform = ', '.join(P)
            if F:
                html = etree.HTML(str(contents[i]))
                b1 = html.xpath('//td[@valign = "top"]/a/text()')
                b2 = html.xpath('//td[@valign = "top"]/text()')
                for x in range(0, len(b2)):
                    E = b1[x] + ' ' + b2[x]
                    S.append(E)
                Sample = ', '.join(S)

        item = response.meta['item']
        item["Status"] = Status
        item["Title"] = Title
        item["Organism"] = Organisms
        item["ExperimentType"] = ExpType
        item["Summary"] = Summary
        item["OverallDesign"] = OverallDesign
        item["Platform"] = Platform
        item["Samples"] = Sample
        yield item
