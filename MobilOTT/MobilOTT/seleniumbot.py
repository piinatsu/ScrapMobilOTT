from selenium.webdriver import Chrome, ChromeOptions
from selenium.webdriver.common.by import By
url = []
for x in range(3):

    page_number = x
    page_size = 3
    ott_url = f"https://www.mobil123.com/mobil-dijual/indonesia?" \
              f"type=used&sort=modification_date_search.desc&" \
              f"page_number={page_number}&page_size={page_size}"
    options = ChromeOptions()
    options.headless = True
    driver = Chrome(options=options)
    driver.get(ott_url)
    try:

        el = driver.find_elements(By.CLASS_NAME, 'listing')
        for elem in el:
            url.append(elem.get_attribute('data-url'))
            # listing_id = elem.get_attribute('data-listing-id')
            # title = elem.get_attribute('data-title')
            # url = elem.get_attribute('data-url')
            #
            # price = elem.find_element(By.CLASS_NAME, 'listing__price').text
            # price = price.replace('Rp', '')
            # price = price.replace('.', '')
            # price = int(price)
            #
            # make = elem.get_attribute('data-make')
            # model = elem.get_attribute('data-model')
            # variant = elem.get_attribute('data-variant')
            # year = int(elem.get_attribute('data-year'))
            # mileage = int(elem.get_attribute('data-mileage'))
            # transmission = elem.get_attribute('data-transmission')
            # ad_type = elem.get_attribute('data-ad-type')
            # location = elem.find_element(By.CSS_SELECTOR, 'div.listing__specs :nth-child(3)').text
            #
            # print(listing_id, make, model, variant, year, mileage, transmission, price, ad_type, location)
            # print(title, url)
            # print('-----------------')


    finally:
        driver.quit()

print(url)