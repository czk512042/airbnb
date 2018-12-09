from lxml import etree
from log import g_logger
import requests


def read_country_url_csv():
    with open('country_url.csv') as fr:
        country_url_list = []
        lines = fr.readlines()
        for line in lines:
            country_url = line.strip('\n')
            country_url_list.append(country_url)
        return country_url_list


def get_each_country_city_url(country_url_list):
    for country_url in country_url_list:
        g_logger.info(country_url)
        res = requests.get(country_url).content
        res_html = etree.HTML(res)
        max_page = get_max_page(res_html)
        city_url_list = get_each_page_city_url(country_url, max_page)
        write_city_url_csv(city_url_list)

        # 只跑一个国家实验
        break


def get_max_page(res_html):
    max_page_xpath = '//div[@class="pagination pagination-responsive"]/ul/li[last()-1]/a/text()'
    max_page = res_html.xpath(max_page_xpath)
    g_logger.info(max_page)
    if max_page:
        return int(max_page[0])
    else:
        return 1


def get_each_page_city_url(country_url, max_page):
    city_url_list = []
    for i in range(max_page):
        g_logger.info('page : %d' % (i+1))
        page_url = country_url + '?page=%d' % (i + 1)
        g_logger.info(page_url)
        res = requests.get(page_url).content
        res_html = etree.HTML(res)
        city_url_path = '//div[@class="row"]/div[@class="col-sm-4"]/ul//li/a/@href'
        url_list = res_html.xpath(city_url_path)
        city_url_list.extend(url_list)
    return city_url_list


def write_city_url_csv(city_url_list):
    city_url_list = set(city_url_list)
    with open('city_url.csv', 'a') as fw:
        for city_url in city_url_list:
            city_url = 'https://zh.airbnb.com' + city_url + '/homes?map_toggle=true'
            fw.write(city_url + '\n')


if __name__ == "__main__":
    country_url_list = read_country_url_csv()
    get_each_country_city_url(country_url_list)
