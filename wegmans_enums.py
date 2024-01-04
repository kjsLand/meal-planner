from enum import Enum

class Paths(Enum):
    department = '//*[@id="react-page"]//a[@class="css-6m6if5"]'
    department_list = '//*[@id="react-page"]/div[1]/div/ul/li[2]/a'
    next_page_button = '//button[@aria-label="Next page"]'
    product = '//div[@class="css-60bqrp"]'