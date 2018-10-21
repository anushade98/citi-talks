import re
from re import sub
from decimal import Decimal
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
xpaths = ["//SPAN[@class='ILfuVd']", "(//DIV[@class='Crs1tb'])[1]"]
options = webdriver.ChromeOptions()
options.add_argument('headless')
driver = webdriver.Chrome(chrome_options=options)

def try_walmart(item):
    walmart = webdriver.Chrome(chrome_options=options)
    walmart.get("https://www.walmart.com/")
    search = walmart.find_element_by_xpath("//INPUT[@id='global-search-input']")
    search.send_keys(item, Keys.ENTER)
    try:
        WebDriverWait(walmart, 2).until(EC.presence_of_element_located((By.XPATH, "//SELECT[@aria-invalid='false']")))


        sort = Select(walmart.find_element_by_xpath("//SELECT[@aria-invalid='false']"))
        sort.select_by_index(2)
        WebDriverWait(walmart, 5).until(EC.presence_of_element_located((By.XPATH, "//STRONG[text()='Price: low to high']")))

        prices = walmart.find_elements_by_class_name("price-main-block")
        prices = [price.text for price in prices]

    except:
        return ['0', '0', '0']

    return prices


def get_price(item):
    driver.get("https://www.google.com")
    cents = False
    result = None
    prices = None

    # item = raw_input("What would you like to know the price of? ").lower()
    query = "What is the cost of %s" % item

    WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.XPATH, "//INPUT[@class='gLFyf gsfi']")))
    search = driver.find_element_by_xpath("//INPUT[@class='gLFyf gsfi']")
    search.clear()
    search.send_keys(query, Keys.ENTER)

    for xpath in xpaths:
        try:
            result = driver.find_element_by_xpath(xpath).text
            # print result
            break
        except NoSuchElementException:
            continue


    if result != None and len(result) >= 1:
        if 'cents' in result or 'Cents' in result:
            cents = True
        if 'billion' in result or 'Billion' in result:
            billions = True

        prices = re.findall("(?:[\$]{1}[,\d]+.?\d*)", result)

        if len(prices) == 0:
            prices = re.findall("[-+]?\d*\.\d+|\d+", result)
            for year in range(2000, 2030):
                try:
                    prices.remove(str(year))
                except Exception:
                    continue

    else:
        prices = try_walmart(item)

    try:
        price = prices[0]
        price = Decimal(sub(r'[^\d.]', '', price))

    except Exception:
        try:
            price = prices[1]
            price = Decimal(sub(r'[^\d.]', '', price))
        except:
            price = 0

    if cents:
        price /= 100

    result = "$%.2f" % price
    return result
