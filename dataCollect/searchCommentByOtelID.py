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
cursor.execute('SELECT otel_ad FROM oteller')
icotel_ad_list = cursor.fetchall()

# Yeni tabloyu oluşturma (Eğer tablo henüz oluşturulmamışsa)
cursor.execute('''
    CREATE TABLE IF NOT EXISTS otel_comment (
        "id" SERIAL PRIMARY KEY,
        "otel_id" INTEGER REFERENCES oteller(id) ON DELETE CASCADE,
        "otel_ad" TEXT,
        "yorum" TEXT
    )
''')

# WebDriver ve sayfa URL'sini ayarlama
search_url = 'https://www.tatilsepeti.com/'

# Her bir otel adı için yorumları çekme
for otel_ad_tuple in icotel_ad_list:
    otel_ad = otel_ad_tuple[0]
    # Otel adından otel_id'yi çekme
    cursor.execute('SELECT id FROM oteller WHERE otel_ad = %s', (otel_ad,))
    otel_id = cursor.fetchone()[0]
    
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
        yorumlar_button.click()        # Tüm sayfa numaralarını toplama

        # Sayfa numarası takibi
        current_page = 1
        while True:
            # Sayfa kaynağını al ve yorumları işle
            yorum_content = driver.page_source
            yorum_soup = BeautifulSoup(yorum_content, 'html.parser')
            yorum_divler = yorum_soup.select('ul.review-list li.review-item div.content')

            # Sayfaya ait yorumları toplama
            page_yorumlar = []

            for yorum_div in yorum_divler:
                yorumlar = yorum_div.select('p.review-pos, p.review-neg')
                for yorum in yorumlar:
                    yorum_text = yorum.get_text(strip=True).replace('\n', ' ')
                    page_yorumlar.append((otel_id, otel_ad, yorum_text))

            # Yorumları veritabanına ekleme
            for otel_id, otel_ad, yorum_text in page_yorumlar:
                cursor.execute('SELECT 1 FROM otel_comment WHERE otel_id = %s AND yorum = %s', (otel_id, yorum_text))
                if not cursor.fetchone():
                    cursor.execute('INSERT INTO otel_comment (otel_id, otel_ad, yorum) VALUES (%s, %s, %s)', (otel_id, otel_ad, yorum_text))
                    print(f"Yorum eklendi: {yorum_text}")

            # Değişiklikleri kaydetme
            conn.commit()

            # Pagination kısmını bulma
            pagination = driver.find_elements(By.CSS_SELECTOR, 'ul.pagination li a')

            if pagination:
                next_page_found = False
                for page in pagination:
                    # Mevcut sayfayı atlayarak bir sonraki sayfaya git
                    if page.text.isdigit() and int(page.text) == current_page + 1:
                        page.click()
                        print("*************YENİ SAYFAYA GEÇİLDİ***********")
                        current_page += 1
                        time.sleep(2)  # Sayfanın yüklenmesi için bekleme süresi
                        next_page_found = True
                        break  # Bir sonraki sayfaya geçtikten sonra çık

                if not next_page_found:
                    break  # Eğer başka sayfa yoksa döngüden çık
            else:
                # Eğer pagination-container yoksa ve review-list mevcutsa yorumları al
                if yorum_soup.select('ul.review-list'):
                    break  # Eğer pagination-container yoksa döngüden çık
                else:
                    break  # Paginasyon kısmı yoksa döngüden çık

    except Exception as e:
        print(f"{otel_ad} için yorumları çekerken hata oluştu: {e}")

# Bağlantıyı kapatma
conn.close()
driver.quit()
