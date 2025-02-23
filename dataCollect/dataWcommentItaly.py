import time
from selenium import webdriver
from selenium.common.exceptions import TimeoutException, NoSuchElementException, StaleElementReferenceException

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import psycopg2
import re
# Chrome WebDriver'ı başlatma
driver = webdriver.Chrome()

main_url = 'https://www.tatilsepeti.com/italya-napoli-otelleri?ara=odadetay%3Aoda1%3A1%3Btarih%3A28.07.2025%2C04.08.2025%3Bclick%3Atrue'
# SQLite veritabanına bağlanma
# PostgreSQL veritabanına bağlanma
conn = psycopg2.connect(
    dbname="postgres",
    user="postgres",
    password="postgres",
    host="localhost",
    port="5432",
    
)
cursor = conn.cursor()


# Tablo oluşturma (Eğer tablo henüz oluşturulmamışsa)
cursor.execute('''
    CREATE TABLE IF NOT EXISTS italy_hotels (
        "id" SERIAL PRIMARY KEY,
        "otel_ad" TEXT,       
        "fiyat" TEXT, 
        "imageURL" TEXT,
        "score" TEXT DEFAULT '',
        "Fiyat Aralığı" TEXT DEFAULT '',
        "Bölge" TEXT DEFAULT '',
        "Hava Alanına Uzaklığı" TEXT DEFAULT '',
        "Denize Uzaklığı" TEXT DEFAULT '',
        "Plaj" TEXT DEFAULT '',  
        "İskele" TEXT DEFAULT '',   
        "A la Carte Restoran" TEXT DEFAULT '0',
        "Asansör" TEXT DEFAULT '0',     
        "Açık Restoran" TEXT DEFAULT '0',
        "Kapalı Restoran" TEXT DEFAULT '0',
        "Açık Havuz" TEXT DEFAULT '0',
        "Kapalı Havuz" TEXT DEFAULT '0',
        "Bedensel Engelli Odası" TEXT DEFAULT '0',
        "Bar" TEXT DEFAULT '0',
        "Su Kaydırağı" TEXT DEFAULT '0',   
        "Balo Salonu" TEXT DEFAULT '0',
        "Kuaför" TEXT DEFAULT '0',
        "Otopark" TEXT DEFAULT '0',    
        "Market" TEXT DEFAULT '0',
        "Sauna" TEXT DEFAULT '0',
        "Doktor" TEXT DEFAULT '0',
        "Beach Voley" TEXT DEFAULT '0',
        "Fitness" TEXT DEFAULT '0',
        "Canlı Eğlence" TEXT DEFAULT '0',
        "Wireless Internet" TEXT DEFAULT '0',
        "Animasyon" TEXT DEFAULT '0',
        "Sörf" TEXT DEFAULT '0',
        "Paraşüt" TEXT DEFAULT '0',
        "Araç Kiralama" TEXT DEFAULT '0',
        "Kano" TEXT DEFAULT '0',
        "SPA" TEXT DEFAULT '0',
        "Masaj" TEXT DEFAULT '0',
        "Masa Tenisi" TEXT DEFAULT '0',
        "Çocuk Havuzu" TEXT DEFAULT '0',
        "Çocuk Parkı" TEXT DEFAULT '0'
    )
''')


cursor.execute('''
    CREATE TABLE IF NOT EXISTS otel_yorumlar_italy (
        "id" SERIAL PRIMARY KEY,
        "otel_id" INTEGER REFERENCES italy_hotels(id) ON DELETE CASCADE,
        "otel_ad" TEXT,
        "yorum" TEXT
    )
''')


driver.get(main_url)

time.sleep(7)  # İçeriğin yüklenmesini bekle

for i in range(1,2):  #53
    try:
        # Butonun var olup olmadığını kontrol et
        load_more_button = WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.ID, "btnLoadMore"))
        )

        # Eğer buton görünmezse, aşağı kaydır
        driver.execute_script("arguments[0].scrollIntoView();", load_more_button)
        time.sleep(1)  # Butonun tam yüklenmesini bekle

        # Butona JavaScript ile tıkla (bazı siteler için gerekebilir)
        driver.execute_script("arguments[0].click();", load_more_button)
        print("Butona tıklandı.")
        
        time.sleep(5)  # İçeriğin yüklenmesini bekle
    except Exception as e:
        print("Load More butonu artık yok. İşleme devam ediliyor.")
        break  # Buton yoksa döngüden çık

# Verileri çekme işlemini buraya ekleyebilirsin.
print("Tüm oteller yüklendi, veri çekme işlemine başlanıyor...")

# Sayfanın tamamen yüklendiğinden emin olmak için bir süre bekleyin (Selenium'un bekleme fonksiyonları kullanılır)
WebDriverWait(driver, 2).until(EC.presence_of_element_located((By.CLASS_NAME, 'discount-price')))

# Sayfanın tamamını kaydırmak için Javascript kullanıyoruz.
driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
time.sleep(8)  # Yükleme tamamlanması için biraz bekleyin

# Sayfanın kaynak kodunu al
content = driver.page_source
soup = BeautifulSoup(content, 'html.parser')

# Ana sayfadaki otel1 URL'lerini ve fiyatlarını bulma
otel_infos = []
hotel_list = soup.find('div', id='HotelList')  # id="HotelList" olan div'i bul
otel_names = hotel_list.find_all('div', class_='panel-heading')

otel_butons = soup.find_all('a', class_='btn btn-block btn-primary')
otel_prices = soup.find_all('p', class_='discount-price')

for otel_name, otel_buton, fiyat in zip(otel_names, otel_butons, otel_prices):
    otel_url = 'https://www.tatilsepeti.com' + otel_buton['href']
    otel_ad = otel_name.text.strip().split('\n\n\n')[0]
    fiyat = fiyat.text.strip()
    otel_infos.append((otel_ad, fiyat, otel_url))

# Her bir otel1 detay sayfasından verileri çekme
for otel_info in otel_infos[:2]:
    otel_ad, fiyat, otel_url = otel_info#    #close-button-1454703513200 > span    
    driver.get(otel_url)

    # Reklam penceresini kapatma
    try:
        close_button = WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.CSS_SELECTOR, '#close-button-1454703513200 > span')))
        close_button.click()
    except (TimeoutException, NoSuchElementException):
        print("Reklam penceresi bulunamadı veya kapatılamadı.")
   

    # Sayfanın tamamen yüklendiğinden emin olmak için bir süre bekleyin (Selenium'un bekleme fonksiyonları kullanılır)
    WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.CLASS_NAME, 'row')))

    otel_content = driver.page_source
    otel_soup = BeautifulSoup(otel_content, 'html.parser')

    # Veritabanında aynı otel1 adı var mı kontrol etme
    cursor.execute('SELECT * FROM italy_hotels WHERE otel_ad = %s', (otel_ad,))
    existing_data = cursor.fetchone()

    if existing_data is None:
        # Veritabanına ekleme
        cursor.execute('SELECT COUNT(*) FROM italy_hotels WHERE otel_ad = %s', (otel_ad,))
        if cursor.fetchone()[0] == 0:
            cursor.execute('INSERT INTO italy_hotels (otel_ad, fiyat) VALUES (%s, %s)', (otel_ad, fiyat))
            cursor.execute('SELECT id FROM italy_hotels WHERE otel_ad = %s', (otel_ad,))
            otel_id = cursor.fetchone()[0]


                # Fiyat aralığını kontrol etme ve veritabanına kaydetme
            fiyat = int(fiyat.split(',')[0].replace('.', ''))
            if 5000 < fiyat <= 7000:
                fiyat_araligi = "5000-7000"
            elif 7000 < fiyat <= 9000:
                fiyat_araligi = "7000-9000"
            elif 9000 < fiyat <= 11000:
                fiyat_araligi = "9000-11000"
            elif 11000 < fiyat <= 13000:
                fiyat_araligi = "11000-13000"
            elif 13000 < fiyat <= 15000:
                fiyat_araligi = "13000-15000"
            elif 15000 < fiyat <= 17000:
                fiyat_araligi = "15000-17000"
            elif 17000 < fiyat <= 19000:
                fiyat_araligi = "17000-19000"
            elif 19000 < fiyat <= 21000:
                fiyat_araligi = "19000-21000"
            elif 21000 < fiyat <= 23000:
                fiyat_araligi = "21000-23000"
            elif 23000 < fiyat <= 25000:
                fiyat_araligi = "23000-25000"
            elif 25000 < fiyat <= 27000:
                fiyat_araligi = "25000-27000"
            elif 27000 < fiyat <= 29000:
                fiyat_araligi = "27000-29000"
            elif 29000 < fiyat <= 31000:
                fiyat_araligi = "29000-31000"
            elif 31000 < fiyat <= 33000:
                fiyat_araligi = "29000-33000"
            else:
                fiyat_araligi = "+33000"

            cursor.execute('UPDATE italy_hotels SET "Fiyat Aralığı" = %s WHERE otel_ad = %s', (fiyat_araligi, otel_ad))


            # otel1 adını çekme
            otel_region = otel_soup.find(class_='location')
            otel_ad =otel_soup.find('h1',class_='col-lg-12 col-md-12 col-sm-12 col-xs-12') 
                    
            # otel1 Özellikleri başlığı altındaki verileri çekme
            konum_bilgileri = otel_soup.find('div', class_='row location-info')
            otel_ozellikleri = otel_soup.find('div', class_='row room-spect mt-15') 
            ucretsiz_aktiviteler = otel_soup.find('div', class_='row free-activities')
            ucretli_aktiviteler = otel_soup.find('div', class_='row paid-activities')                
            cocuk_aktiviteleri = otel_soup.find('div', class_='row activities-for-children')
            

            # İlgili CSS selektörü kullanılarak resim öğesine erişim
            resim_etiketi = otel_soup.select_one('body > div.tsmenucontainer.clearfix > main > section > article.col-md-9.col-lg-9.hotel-detail__article > div.hotel-photos > div.photo-gallery.owl-carousel.flatloading.owl-loaded.owl-drag > div.owl-stage-outer > div > div.owl-item.active > div > img')

            # Resim URL'sini al
            if resim_etiketi:
                resim_url = resim_etiketi['src']
            else:
                resim_url = "Resim bulunamadı"

            # Veritabanına resim URL'sini kaydetme
            cursor.execute('UPDATE italy_hotels SET "imageURL" = %s WHERE otel_ad = %s', (resim_url, otel_ad))





            # Bölge bilgisini çekme
            bölge = otel_soup.find('div', class_='hotel__region')
            if bölge:
                bölge_text = bölge.get_text(strip=True).split('Haritada Görüntüle')[0:]
                bölge_metni = ' '.join(bölge_text)
                cursor.execute('UPDATE italy_hotels SET "Bölge" = %s WHERE otel_ad = %s', (bölge_metni, otel_ad))
            # Sayfanın tamamen yüklendiğinden emin olmak için bir süre bekleyin (Selenium'un bekleme fonksiyonları kullanılır)

            try:
                WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.CLASS_NAME, 'score__right')))
                # Score bilgisini çekme
                score = otel_soup.find('div', class_='score__right')
                if score:
                    score_text = score.get_text(strip=True)
                else:
                    score_text = None
            except TimeoutException:
                score_text = None

            # Veritabanına kaydetme
            cursor.execute('UPDATE italy_hotels SET "score" = %s WHERE otel_ad = %s', (score_text, otel_ad))


            if konum_bilgileri:
                cursor.execute("SELECT column_name FROM information_schema.columns WHERE table_name = 'italy_hotels'")
                column_names = [row[0] for row in cursor.fetchall()]
                konum_tablosu = konum_bilgileri.find_next('table')
                if konum_tablosu:
                    konum_bilgileri_listesi = konum_tablosu.find_all('tr')
                    for bilgi in konum_bilgileri_listesi:
                        th_list = bilgi.find_all('th', class_='location-info__title')
                        td_list = bilgi.find_all('td')
                        for i in range(len(th_list)):
                            baslik = th_list[i].text.strip() if i < len(th_list) else ''
                            deger = td_list[i].text.strip() if i < len(td_list) else ''
                            baslik = baslik.split(':')[0]
                            if baslik in column_names:
                                if baslik == "Hava Alanına Uzaklığı":
                                    sayi = re.findall(r'\d+', deger)
                                    uzaklik = sayi[0] if sayi else "No Info"
                                    havaalani_adi_search = re.search(r'([^0-9]+)', deger)
                                    havaalani_adi = havaalani_adi_search.group(0) if havaalani_adi_search else "No Info"
                                    uzaklik_metni = f"{uzaklik} km, {havaalani_adi}"
                                    cursor.execute('UPDATE italy_hotels SET "Hava Alanına Uzaklığı" = %s WHERE otel_ad = %s', (uzaklik_metni, otel_ad))
                                else:
                                    deger = deger if deger.strip() else "No Info"
                                    cursor.execute(f'UPDATE italy_hotels SET "{baslik}" = %s WHERE otel_ad = %s', (deger, otel_ad))

            # otel1 Özellikleri başlığı altındaki verileri çekme
            for ozellik in [otel_ozellikleri, ucretsiz_aktiviteler, ucretli_aktiviteler, cocuk_aktiviteleri]:
                if ozellik:
                    otel_ozellikleri_listesi = ozellik.find('ul')
                    if otel_ozellikleri_listesi:
                        cursor.execute("SELECT column_name FROM information_schema.columns WHERE table_name = 'italy_hotels'")
                        column_names = [row[0] for row in cursor.fetchall()]


                        for li in otel_ozellikleri_listesi.find_all('li'):
                            ozellik = li.text.strip()

                            adet = 1
                            
                            if '(' in ozellik:
                                adet_firstindex = ozellik.find('(')
                                adet_lastindex = ozellik.find(' Adet')
                                if adet_firstindex > 0:
                                    ozellik_adi = ozellik[:adet_firstindex].strip()
                                    if ozellik_adi in column_names:
                                        adet_str = ozellik[adet_firstindex+1:adet_lastindex].strip()
                                        adet = adet_str
                                        cursor.execute(f'UPDATE italy_hotels SET "{ozellik_adi}" = %s WHERE otel_ad = %s', (adet, otel_ad))
                            else: 
                                if ozellik in column_names:                                           
                                    cursor.execute(f'UPDATE italy_hotels SET "{ozellik}" = %s WHERE otel_ad = %s', (adet, otel_ad))

            # Reklam penceresini kapatma
            try:
                close_button = WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.CSS_SELECTOR, '#close-button-1454703513200 > span')))
                close_button.click()
            except (TimeoutException,NoSuchElementException):
                print("Reklam penceresi bulunamadı veya kapatılamadı.")
            

    """"
                # Yorumları çekme
                try:
                    # Yorumlar bölümüne tıklama
                    WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.CLASS_NAME, 'score__right')))
                    yorumlar_button = driver.find_element(By.CLASS_NAME, 'score__right')
                    yorumlar_button.click()

                    # Yorumlar penceresinin tamamen yüklenmesini bekleme
                    WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.CLASS_NAME, 'review-list')))

                    # Yorumları çekme
                    yorum_content = driver.page_source
                    yorum_soup = BeautifulSoup(yorum_content, 'html.parser')
                    yorum_divler = yorum_soup.select('ul.review-list li.review-item div.content')

                    for yorum_div in yorum_divler:
                        # Pozitif yorumları çekme
                        pozitif_yorumlar = yorum_div.select('p.review-pos')
                        for pozitif_yorum in pozitif_yorumlar:
                            yorum_text = pozitif_yorum.get_text(strip=True).replace('\n', ' ')
                            yorum_text = f"Pozitif yönü, {yorum_text}"
                            cursor.execute('INSERT INTO otel_yorumlar (otel_id, otel_ad, yorum) VALUES (%s, %s, %s)', (otel_id, otel_ad, yorum_text))

                        # Negatif yorumları çekme
                        negatif_yorumlar = yorum_div.select('p.review-neg')
                        for negatif_yorum in negatif_yorumlar:
                            yorum_text = negatif_yorum.get_text(strip=True).replace('\n', ' ')
                            yorum_text = f"Negatif yönü, {yorum_text}"
                            cursor.execute('INSERT INTO otel_yorumlar (otel_id, otel_ad, yorum) VALUES (%s, %s, %s)', (otel_id, otel_ad, yorum_text))

                except Exception as e:
                    print(f"Yorumları çekerken hata oluştu: {e}")
        



                # Değişiklikleri kaydetme
                conn.commit()"""
    

# italy_hotels tablosundaki tüm verileri seç
cursor.execute("SELECT * FROM italy_hotels;")
rows = cursor.fetchall()

# Sütun isimlerini al
column_names = [desc[0] for desc in cursor.description]

# Verileri yazdır
print("\t".join(column_names))  # Sütun başlıklarını yazdır
for row in rows:
    print("\t".join(map(str, row)))  # Satırları yazdır

conn.close()

# WebDriver'ı kapatma
driver.quit()