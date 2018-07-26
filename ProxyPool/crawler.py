import json
import re
from lxml import etree
from .utils import get_page
from pyquery import PyQuery as pq

class ProxyMetaclass(type):
    def __new__(cls, name, bases, attrs):
        count = 0
        attrs['__CrawlFunc__'] = []
        for k, v in attrs.items():
            if 'crawl_' in k:
                attrs['__CrawlFunc__'].append(k)
                count += 1
        attrs['__CrawlFuncCount__'] = count
        return type.__new__(cls, name, bases, attrs)


class Crawler(object, metaclass=ProxyMetaclass):
    def get_proxies(self, callback):
        proxies = []
        for proxy in eval("self.{}()".format(callback)):
            print('成功获取到代理', proxy)
            proxies.append(proxy)
        return proxies

    def crawl_daili66(self, page_count=4):
        """
        获取代理66
        :param page_count: 页码
        :return: 代理
        """
        start_url = 'http://www.66ip.cn/{}.html'
        urls = [start_url.format(page) for page in range(1, page_count + 1)]
        for url in urls:
            html = get_page(url)
            if html:
                doc = pq(html)
                trs = doc('.containerbox table tr:gt(0)').items()
                for tr in trs:
                    ip = tr.find('td:nth-child(1)').text().strip()
                    port = tr.find('td:nth-child(2)').text().strip()
                    yield ':'.join([ip, port])

    def crawl_ip3366(self):
        for page in range(1, 5):
            start_url = 'http://www.ip3366.net/free/?stype=1&page={}'.format(
                str(page))
            html = get_page(start_url)
            ip_address = re.compile('<tr>\s*<td>(.*?)</td>\s*<td>(.*?)</td>')
            # \s * 匹配空格，起到换行作用
            re_ip_address = ip_address.findall(str(html))
            for address, port in re_ip_address:
                result = address.strip() + ':' + port.strip()
                yield result.replace(' ', '')

    def crawl_kuaidaili(self):
        for i in range(1, 4):
            start_url = 'http://www.kuaidaili.com/free/inha/{}/'.format(i)
            html = get_page(start_url)
            if html:
                ip_address = re.compile('<td data-title="IP">(.*?)</td>')
                re_ip_address = ip_address.findall(html)
                port = re.compile('<td data-title="PORT">(.*?)</td>')
                re_port = port.findall(html)
                for address, port in zip(re_ip_address, re_port):
                    address_port = address + ':' + port
                    yield address_port.replace(' ', '')

    def crawl_xicidaili(self):
        for i in range(1, 6):
            start_url = 'http://www.xicidaili.com/nn/{}'.format(i)
            headers = {
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
                'Host': 'www.xicidaili.com',
                'Referer': 'http://www.xicidaili.com/nn/3',
                'Upgrade-Insecure-Requests': '1',
            }
            html = get_page(start_url, options=headers)
            if html:
                find_trs = re.compile('<tr class.*?>(.*?)</tr>', re.S)
                trs = find_trs.findall(html)
                for tr in trs:
                    find_ip = re.compile('<td>(\d+\.\d+\.\d+\.\d+)</td>')
                    re_ip_address = find_ip.findall(tr)
                    find_port = re.compile('<td>(\d+)</td>')
                    re_port = find_port.findall(tr)
                    for address, port in zip(re_ip_address, re_port):
                        address_port = address + ':' + port
                        yield address_port.replace(' ', '')

    def crawl_ip3366(self):
        for i in range(1, 5):
            start_url = 'http://www.ip3366.net/?stype=1&page={}'.format(i)
            html = get_page(start_url)
            if html:
                find_tr = re.compile('<tr>(.*?)</tr>', re.S)
                trs = find_tr.findall(html)
                for s in range(1, len(trs)):
                    find_ip = re.compile('<td>(\d+\.\d+\.\d+\.\d+)</td>')
                    re_ip_address = find_ip.findall(trs[s])
                    find_port = re.compile('<td>(\d+)</td>')
                    re_port = find_port.findall(trs[s])
                    for address, port in zip(re_ip_address, re_port):
                        address_port = address + ':' + port
                        yield address_port.replace(' ', '')

    def crawl_iphai(self):
        start_url = 'http://www.iphai.com/'
        html = get_page(start_url)
        if html:
            find_tr = re.compile('<tr>(.*?)</tr>', re.S)
            trs = find_tr.findall(html)
            for s in range(1, len(trs)):
                find_ip = re.compile(
                    '<td>\s+(\d+\.\d+\.\d+\.\d+)\s+</td>', re.S)
                re_ip_address = find_ip.findall(trs[s])
                find_port = re.compile('<td>\s+(\d+)\s+</td>', re.S)
                re_port = find_port.findall(trs[s])
                for address, port in zip(re_ip_address, re_port):
                    address_port = address + ':' + port
                    yield address_port.replace(' ', '')

    def crawl_89ip(self):
        start_url = 'http://www.89ip.cn/'
        html = get_page(start_url)
        # print(html)
        if html:
            noods = etree.HTML(html).xpath(
                '//table[@class="layui-table"]/tbody/tr')
            for each in noods:
                ip = each.xpath('./td[1]/text()')[0].strip()
                port = each.xpath('./td[2]/text()')[0].strip()
                ip_port = ip + ':' + port
                yield ip_port.replace(' ', '').replace('\n', '')

    def crawl_data5u(self):
        start_url = 'http://www.data5u.com/free/gngn/index.shtml'
        headers = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7',
            'Cache-Control': 'max-age=0',
            'Connection': 'keep-alive',
            'Host': 'www.data5u.com',
            'Referer': 'http://www.data5u.com/free/index.shtml',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.108 Safari/537.36',
        }
        html = get_page(start_url, options=headers)
        if html:
            ip_address = re.compile(
                '<span><li>(\d+\.\d+\.\d+\.\d+)</li>.*?<li class=\"port.*?>(\d+)</li>', re.S)
            re_ip_address = ip_address.findall(html)
            for address, port in re_ip_address:
                result = address + ':' + port
                yield result.replace(' ', '')

    def proxy_dockers(self):
        url = 'https://www.proxydocker.com/zh/proxylist/search?port=All&type=All&anonymity=ANONYMOUS&country=China&city=All&state=All&need=All'
        html = get_page(url)
        if html:
            noods = etree.HTML(html).xpath(
                '//tr[@id="proxy-table-header"]/following-sibling::*')
            for each in noods:
                if not each.xpath('./td/a[@href]'):
                    continue
                ip = each.xpath(
                    './td/a/text()')[0].strip() if each.xpath('./td/a/text()')[0] else ''
                port = each.xpath(
                    './td/text()')[1].strip() if each.xpath('./td/a/text()')[0] else ''
                ip_port = ip + port
                if ip_port:
                    yield ip_port

    def cross_proxy(self):
        url = 'http://lab.crossincode.com/proxy/'
        html = get_page(url)
        # print(html)
        noods = etree.HTML(html).xpath(
            '//table[@class="table table-bordered proxy-index-table"]/tr')
        for each in noods[1:]:
            ip = each.xpath('./td[1]/text()')[0].strip()
            port = each.xpath('./td[2]/text()')[0].strip()
            ip_port = ip + ':' + port
            yield ip_port

    def kxdaili(self, page_count=5):
        start_url = 'http://ip.kxdaili.com/dailiip/1/{}.html#ip'
        for page in range(1, page_count + 1):
            url = start_url.format(page)
            html = get_page(url)
            noods = etree.HTML(html).xpath(
                '//table[@class="ui table segment"]/tbody/tr')
            for each in noods:
                ip = each.xpath('./td[1]/text()')[0].strip()
                port = each.xpath('./td[2]/text()')[0].strip()
                ip_port = ip + ':' + port
                yield ip_port

    def yqie(self):
        url = 'http://ip.yqie.com/ipproxy.htm'
        html = get_page(url)
        noods = etree.HTML(html).xpath(
            '//div[@class="divcenter"][1]//table/tr')
        for each in noods[1:]:
            ip = each.xpath('./td[1]/text()')[0].strip()
            port = each.xpath('./td[2]/text()')[0].strip()
            ip_port = ip + ':' + port
            yield ip_port

    def ihuan(self):
        start_url = 'https://ip.ihuan.me/address/5Lit5Zu9.html?page=b97827cc'
        base_url = 'https://ip.ihuan.me/'
        data = get_page(start_url)
        nood = etree.HTML(data).xpath('//ul[@class="pagination"]/li')

        page_urls = [base_url + i.xpath('./a/@href')[0] for i in nood[1:7]]
        # print(data)
        print(page_urls)
        for url in page_urls:
            html = get_page(url)
            noods = etree.HTML(html).xpath(
                '//div[@class="table-responsive"]/table/tbody/tr')
            for each in noods:
                ip = each.xpath('./td[1]/a/text()')[0].strip()
                port = each.xpath('./td[2]/text()')[0].strip()
                ip_port = ip + ':' + port
                yield ip_port
