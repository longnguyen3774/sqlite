from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import re
import sqlite3

###############################################################
# 0. Tạo cơ sở dữ liệu
conn = sqlite3.connect('painter.db')
c = conn.cursor()
try:
    c.execute('''
        CREATE TABLE painter (
            id integer primary key autoincrement,
            name text,
            birth text,
            death text,
            nationality text
        )
    ''')
except Exception as e:
    print(e)
conn.close()

def insert_data(name, birth, death, nationality):
    conn = sqlite3.connect('painter.db')
    c = conn.cursor()
    # Them vao co so du lieu
    c.execute('''
        INSERT INTO painter(name, birth, death, nationality)
        VALUES (:name, :birth, :death, :nationality)
    ''',
      {
          'name': name,
          'birth': birth,
          'death': death,
          'nationality': nationality
      })
    conn.commit()
    conn.close()

###############################################################
# 1. Thu thập dữ liệu
# Web driver
driver = webdriver.Chrome()

for i in range(65, 91):
    try:
        # Open webpage
        url = 'https://en.wikipedia.org/wiki/List_of_painters_by_name_beginning_with_%22' + chr(i) + '%22'
        driver.get(url)

        # Wait for 1 second
        time.sleep(1)

        # Get all ul tags
        ul_tags = driver.find_elements(By.TAG_NAME, 'ul')

        # Get ul tag at index 20
        ul_painters = ul_tags[20]  # list start with index=0

        # Get all <li> tags in ul_painters
        li_tags = ul_painters.find_elements(By.TAG_NAME, 'li')

        # Create links
        links = []
        for tag in li_tags:
            try:
                link = tag.find_element(By.TAG_NAME, 'a').get_attribute('href')
                links.append(link)
            except Exception as e:
                print(e)
                continue

        for link in links:
            driver.get(link)

            # Wait for 1e-20 seconds
            time.sleep(1e-20)

            # Get name
            try:
                p_name = driver.find_element(By.TAG_NAME, 'h1').text
            except Exception as e:
                print(e)
                p_name = ''

            # Get birthday
            try:
                birth_element = driver.find_element(By.XPATH, "//th[text()='Born']/following-sibling::td")
                p_birth = birth_element.text
                p_birth = re.findall(r'[0-9]{1,2}+\s+[A-Za-z]+\s+[0-9]{4}', p_birth)[0]
            except Exception as e:
                print(e)
                p_birth = ''

            # Get death
            try:
                death_element = driver.find_element(By.XPATH, "//th[text()='Died']/following-sibling::td")
                p_death = death_element.text
                p_death = re.findall(r'[0-9]{1,2}+\s+[A-Za-z]+\s+[0-9]{4}', p_death)[0]
            except Exception as e:
                print(e)
                p_death = ''

            # Get nationality
            try:
                nationality_element = driver.find_element(By.XPATH,
                                                          "//th[text()='Nationality']/following-sibling::td")
                p_nationality = nationality_element.text
            except Exception as e:
                print(e)
                p_nationality = ''

            insert_data(p_name, p_birth, p_death, p_nationality)
    except Exception as e:
        print(e)
        continue

driver.quit()
