from selenium.webdriver import Chrome

page_number = 1
page_size = 2

ott_url = f"https://www.mobil123.com/mobil-dijual/indonesia?" \
          f"type=used&sort=modification_date_search.desc&" \
          f"page_number={page_number}&page_size={page_size}"

driver = Chrome()
driver.get(ott_url)

driver.quit()