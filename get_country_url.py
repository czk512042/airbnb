import requests
from lxml import etree


def get_country_urls():
    url = 'https://zh.airbnb.com/sitemaps'
    res = requests.get(url).content
    res_html = etree.HTML(res)
    href_xpath = '//div[@class="row"]//a/@href'
    href_list = res_html.xpath(href_xpath)
    return href_list


def write_country_url_csv(url_list):
    with open('country_url.csv', 'a') as fw:
        for url in url_list:
            url = 'https://zh.airbnb.com' + url
            fw.write(url + '\n')


if __name__ == "__main__":
    href_list = get_country_urls()
    write_country_url_csv(href_list)
