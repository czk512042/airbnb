from time import sleep
from log import g_logger
from selenium import webdriver
driver = webdriver.Chrome()
driver.maximize_window()


def read_hotel_url_csv():
    with open('hotel_url.csv') as fr:
        hotel_url_list = []
        lines = fr.readlines()
        for line in lines:
            hotel_url = line.strip('\n')
            hotel_url_list.append(hotel_url)
        return hotel_url_list


def get_each_hotel_detail(hotel_url_list):
    for hotel_url in hotel_url_list:
        g_logger.info(hotel_url)
        driver.get(hotel_url)
        sleep(5)
        price_xpath = '//*[@id="room"]/div/div[2]/div/div/div[1]/div[2]/div/div/div/div/div[1]/div/div/div[1' \
                      ']/div/div/div[2]/div[1]/span/div/div/div/span[1]/span'
        print(driver.find_element_by_xpath(price_xpath).text)


if __name__ == "__main__":
    hotel_url_list = read_hotel_url_csv()
    get_each_hotel_detail(hotel_url_list)
    driver.close()