from time import sleep
from log import g_logger
from selenium import webdriver
driver = webdriver.Chrome()
driver.maximize_window()


def read_city_url_csv():
    with open('city_url.csv') as fr:
        city_url_list = []
        lines = fr.readlines()
        for line in lines:
            city_url = line.strip('\n')
            city_url_list.append(city_url)
        return city_url_list


def get_each_city_hotel_url(city_url_list):
    for city_url in city_url_list:
        g_logger.info(city_url)
        driver.get(city_url)
        max_page = get_max_page()
        hotel_url_list = get_each_page_hotel_url(max_page)
        write_hotel_url_csv(hotel_url_list)

        # 只跑一个城市实验
        break


def get_max_page():
    sleep(2)
    close_button_xpath = '//*[@id="site-content"]/div/div/div[6]/div[2]/div/div[1]'
    driver.find_element_by_xpath(close_button_xpath).click()
    max_page_xpath = '//ul[@data-id="SearchResultsPagination"]/li[last()-1]/a/div'
    max_page = driver.find_element_by_xpath(max_page_xpath).text
    return int(max_page)


def get_each_page_hotel_url(max_page):
    hotel_url_list = []
    i = 1
    while i <= max_page:
        if i == 1:
            hotel_id_xpath = '//div[contains(@id, "listing-")]'
            hotel_id_elements = driver.find_elements_by_xpath(hotel_id_xpath)
            hotel_ids = []
            for hotel_id_element in hotel_id_elements:
                hotel_ids.append(hotel_id_element.get_attribute('id').replace('listing-', ''))
            hotel_url_list.extend(hotel_ids)
            i += 1
        else:
            next_page_xpath = '//ul[@data-id="SearchResultsPagination"]/li[last()]/a'
            driver.find_element_by_xpath(next_page_xpath).click()
            sleep(5)
            hotel_id_xpath = '//div[contains(@id, "listing-")]'
            hotel_id_elements = driver.find_elements_by_xpath(hotel_id_xpath)
            hotel_ids = []
            for hotel_id_element in hotel_id_elements:
                hotel_ids.append(hotel_id_element.get_attribute('id').replace('listing-', '').replace('map-', ''))
            hotel_url_list.extend(hotel_ids)
            i += 1
    return hotel_url_list


def write_hotel_url_csv(hotel_url_list):
    hotel_url_list = set(hotel_url_list)
    with open('hotel_url.csv', 'a') as fw:
        for hotel_url in hotel_url_list:
            city_url = 'https://zh.airbnb.com/rooms/' + hotel_url
            fw.write(city_url + '\n')


if __name__ == "__main__":
    city_url_list = read_city_url_csv()
    get_each_city_hotel_url(city_url_list)
    driver.close()