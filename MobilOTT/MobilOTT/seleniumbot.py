from selenium.webdriver import Chrome, ChromeOptions
from selenium.webdriver.common.by import By

page_number = 1
page_size = 2
ott_url = f"https://www.mobil123.com/mobil-dijual/indonesia?" \
          f"type=used&sort=modification_date_search.desc&" \
          f"page_number={page_number}&page_size={page_size}"
options = ChromeOptions()
options.headless = True
driver = Chrome(options=options)
driver.get(ott_url)

el = driver.find_elements(By.CLASS_NAME, 'listing')
for l in el:
    id = l.get_attribute('id')
    title = l.get_attribute('data-title')
    url = l.get_attribute('data-url')
    price = l.get_attribute('data-price')
    make = l.get_attribute('data-make')
    model = l.get_attribute('data-model')
    variant = l.get_attribute('data-variant')
    year = l.get_attribute('data-year')
    mileage = l.get_attribute('data-mileage')
    transmission = l.get_attribute('data-transmission')
    ad_type = l.get_attribute('data-ad-type')

    print(id, make, model, variant, year, mileage, transmission, ad_type)
    print(title, price, url)
print(el)
# id
# data-title
# data-url
# data-price
# data-default-line-text
# data-make
# data-model
# data-year
# data-mileage
# data-transmission
# data-ad-type
# data-variant
#
# div.listing__price

driver.quit()