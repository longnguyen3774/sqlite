from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
import re
import sqlite3

###############################################################
# 0. Tạo cơ sở dữ liệu
conn = sqlite3.connect('product.db')
c = conn.cursor()
try:
    c.execute('''
        CREATE TABLE product (
            id integer primary key autoincrement,
            name text,
            price integer,
            image text
        )
    ''')
except Exception as e:
    print(e)
conn.close()

def insert_data(name, price, image):
    conn = sqlite3.connect('product.db')
    c = conn.cursor()
    # Them vao co so du lieu
    c.execute('''
        INSERT INTO product(name, price, image)
        VALUES (:name, :price, :image)
    ''',
      {
          'name': name,
          'price': price,
          'image': image
      })
    conn.commit()
    conn.close()

###############################################################
# 1. Thu thập dữ liệu
# Đường dẫn đến file thực thi geckodriver
gecko_path = 'D:/PyCharm/SQLite/project4/products/geckodriver.exe'

# Khởi tạo đối tượng dịch vụ với đường geckodriver
ser = Service(gecko_path)

# Tạo tùy chọn
options = webdriver.firefox.options.Options()

# Thiết lập firefox chỉ hiện thị giao diện
options.headless = False

# Khởi tạo driver
driver = webdriver.Firefox(options = options, service = ser)

# Tạo url
url = 'https://nhathuoclongchau.com.vn/thuc-pham-chuc-nang/vitamin-khoang-chat'

# Truy cập
driver.get(url)

time.sleep(5)

body = driver.find_element(By.TAG_NAME, 'body')

cont = True
while cont:
    try:
        buttons = driver.find_elements(By.TAG_NAME, 'button')
        is_found = False
        for button in buttons:
            if "Xem thêm" in button.text and "sản phẩm" in button.text:
                is_found = True
                button.click()
                break
        cont = is_found
    except Exception as e:
        print(e)
    time.sleep(2)

for i in range(50):
    body.send_keys(Keys.ARROW_DOWN)
    time.sleep(0.05)

# Tam dung them vai giay
time.sleep(5)

buttons = driver.find_elements(By.XPATH, "//button[text()='Chọn mua']")

for i, bt in enumerate(buttons, 1):
    parent_div = bt
    for _ in range(3):
        parent_div = parent_div.find_element(By.XPATH, './..')

    sp = parent_div

    try:
        tsp = sp.find_element(By.TAG_NAME, 'h3').text
    except Exception as e:
        print(e)
        tsp = ''

    try:
        gsp = sp.find_element(By.CLASS_NAME, 'text-blue-5').text
        gsp = re.sub(r'\D', '', gsp)
    except Exception as e:
        print(e)
        gsp = ''

    try:
        ha = sp.find_element(By.TAG_NAME, 'img').get_attribute('src')
    except Exception as e:
        print(e)
        ha = ''

    if len(tsp) > 0:
        insert_data(tsp, gsp, ha)

driver.quit()
