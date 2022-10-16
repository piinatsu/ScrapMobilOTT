# response.css('article').attrib['data-default-line-text']
        # 'I am interested in your car on Mobil123.com - 2019 ' \
        # 'Toyota Kijang Innova 2.0 G MPV (Rp 298.000.000). https://www.mobil123.com/dijual
        # / toyota - kijang - innova - g - dki - jakarta - tebet / 10476834.
        # '

str = "https://www.mobil123.com/mobil-dijual/indonesia?type=used&sort=modification_date_search.desc&page_number=2&page_size=5"
str = str.split("&")[2]
print(str)
str = str.split("=")[1]
print(str)
str = int(str)
print(type(str))






