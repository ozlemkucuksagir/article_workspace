import time

from selenium.webdriver.common.keys import Keys
from selenium import webdriver
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import psycopg2

# Chrome WebDriver'ı başlatma
driver = webdriver.Chrome()

# PostgreSQL veritabanına bağlanma
conn = psycopg2.connect(
    dbname="postgres",
    user="postgres",
    password="postgres",
    host="localhost",
    port="5432",
)
cursor = conn.cursor()

# Eski veritabanından otel_ad'ları çekme
cursor.execute('SELECT otel_ad FROM hotels_data')
icotel_ad_list = cursor.fetchall()

# Yeni tabloyu oluşturma (Eğer tablo henüz oluşturulmamışsa)
cursor.execute('''
    CREATE TABLE IF NOT EXISTS otel_comment (
        "id" SERIAL PRIMARY KEY,
        "otel_id" INTEGER REFERENCES hotels_data(id) ON DELETE CASCADE,
        "otel_ad" TEXT,
        "yorum" TEXT
    )
''')

# WebDriver ve sayfa URL'sini ayarlama
search_url = 'https://www.tatilsepeti.com/'

# Her bir otel adı için yorumları çekme
for otel_ad_tuple in icotel_ad_list:
    otel_ad = otel_ad_tuple[0]
    
    # Siteye gitme
    driver.get(search_url)

    try:
        # Otel adını arama kutusuna yazma
        search_input = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, 'bolge'))  # Arama kutusunun doğru CSS seçicisini kullanın
        )
        search_input.clear()
        search_input.send_keys(otel_ad)
        search_input.send_keys(Keys.RETURN) 

        # Yorumları çekme
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, 'score__right'))
        )
        yorumlar_button = driver.find_element(By.CLASS_NAME, 'score__right')
        yorumlar_button.click()

        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, 'review-list'))
        )
        yorum_content = driver.page_source
        yorum_soup = BeautifulSoup(yorum_content, 'html.parser')
        yorum_divler = yorum_soup.select('ul.review-list li.review-item div.content')

        for yorum_div in yorum_divler:
            pozitif_yorumlar = yorum_div.select('p.review-pos')
            for pozitif_yorum in pozitif_yorumlar:
                yorum_text = pozitif_yorum.get_text(strip=True).replace('\n', ' ')
                yorum_text = f"Pozitif yönü, {yorum_text}"
                cursor.execute('INSERT INTO otel_comment (otel_ad, yorum) VALUES (%s, %s)', (otel_ad, yorum_text))

            negatif_yorumlar = yorum_div.select('p.review-neg')
            for negatif_yorum in negatif_yorumlar:
                yorum_text = negatif_yorum.get_text(strip=True).replace('\n', ' ')
                yorum_text = f"Negatif yönü, {yorum_text}"
                cursor.execute('INSERT INTO otel_comment (otel_ad, yorum) VALUES (%s, %s)', (otel_ad, yorum_text))

    except Exception as e:
        print(f"{otel_ad} için yorumları çekerken hata oluştu: {e}")

    # Değişiklikleri kaydetme
    conn.commit()

# Bağlantıyı kapatma
conn.close()
driver.quit()
