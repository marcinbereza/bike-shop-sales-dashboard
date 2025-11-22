from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium import webdriver


from bs4 import BeautifulSoup
import csv, time, re


def set_columns_name(header:list = None, csv_filename:str = '../data/bikes.csv'):
    if not header: header = ['product_id', 'SKU', 'Category', 'Subcategory', 'Brand', 'Model', 'Regular_Price', 'Discount_Price', '30Day_Price', 'Image_URL']

    with open(csv_filename, 'w', newline='', encoding='utf-8-sig') as f:
        writer = csv.writer(f)
        writer.writerow(header)


def save_csv(parsed_data, page_counter, csv_filename:str = '../data/bikes.csv'):
    with open(csv_filename, 'a', newline='', encoding='utf-8-sig') as f:
        writer = csv.writer(f)
        writer.writerows(parsed_data)

    print(f'\r✅ Strona {page_counter} sparsowana i zapisana. Znaleziono {len(parsed_data)} produktów.', end='')


def cookie_accept(wait):
    try:
        cookie_btn = wait.until(
            EC.element_to_be_clickable((
                By.CSS_SELECTOR,
                'button#CybotCookiebotDialogBodyLevelButtonLevelOptinAllowallSelection'))
        )
        cookie_btn.click()
        print('Akceptacja cookies powiodła się.')
        time.sleep(1)
    except:
        print('Brak lub problem z przyciskiem cookies, kontynuuję.')
        pass


def product_name(product_string):
    know_brands = ['Giant', 'Kross', 'Orbea', 'Cannondale', 'Unibike', 'Marin', 'Trek', 'Polygon', 'Specialized', 'NS Bikes', 
                   'GT', 'Rondo', 'Dartmoor', 'Woom', 'Electra', 'Diamant', 'Octane One', 'Creme', 'Pinarello', 'Mongoose',
                   'Puky', 'Factor', 'RWR']

    know_brands_sort = sorted(know_brands, key=len, reverse=True)
    brand = 'Unknown'
    model = product_string
    category_string = ''

    for know_brand in know_brands_sort:
        match_brand = re.search(r'\b' + re.escape(know_brand) + r'\b', product_string, re.IGNORECASE)

        if match_brand:
            brand_start = match_brand.start()
            brand_end   = match_brand.end()

            category_string = product_string[:brand_start].strip().split()
            brand = know_brand
            model = product_string[brand_end:].strip()
            break

    category = category_string[0]               if len(category_string) >= 1 else 'Rower'
    subcategory = ' '.join(category_string[:2]) if len(category_string) >= 2 else 'Unknown'
  
    return category, subcategory, brand, model


def parse(html_source, page_counter, product_counter:str):
    soup = BeautifulSoup(html_source, 'lxml')
    rows = soup.find_all(class_='item product product-item')
    parsed_bikes = []
    prod_id = 0

    for row in rows:
        try:# 1. Obraz i SKU
            product_id = f'BIKE{product_counter + prod_id}'
            img = row.select_one('.product-img a img')['src']
            product_sku = row.select_one('.detail-wrap div[data-review-product-id]').get('data-review-product-id')
            if not product_sku: continue

            # 2. Ceny
            prices = [s['data-price-amount'] for s in row.select('.price-box span[data-price-amount]')]
            if not prices: continue
            price_curr     = prices[0] if len(prices)>=1 else ''
            price_discount = prices[1] if len(prices)>=2 else ''
            price_30day    = prices[2] if len(prices)>=3 else ''
            
            # 3. Szczegóły Produktu
            product_details = row.select_one('.product-item-link h3').text.strip()
            category, subcategory, brand, model = product_name(product_details)

            parsed_bikes.append([product_id, product_sku, category, subcategory, brand, model, price_curr, price_discount, price_30day, img])
            prod_id += 1
            
        except Exception as e:
            print(f'Błąd parsowania produktu na stronie {page_counter}: {e}')
            continue
    return parsed_bikes


if __name__=='__main__':
    options = Options()
    options.add_argument('--headless=new') 
    options.add_argument('--disable-gpu')
    driver = webdriver.Chrome(options=options)
    driver.get('https://sprint-rowery.pl/rowery')
    wait = WebDriverWait(driver, 10)
    page_counter = 0

    set_columns_name()
    cookie_accept(wait)
    product_counter = 10_000

    while True:
        page_counter += 1
        
        try:
            wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, '.product-item-details')))
            html_source = driver.page_source

            parsed_data = parse(html_source, page_counter, product_counter)
            product_counter+=len(parsed_data)
            
            save_csv(parsed_data, page_counter)

            next_btn = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'a.action.next')))
            driver.execute_script('arguments[0].click();', next_btn)
            wait.until(EC.staleness_of(next_btn))
            
        except Exception as e:
            print(f'🛑 Brak przycisku "Następny" po stronie {page_counter}')
            break

    driver.quit()
    print(f'Zakończono proces. Całkowita liczba stron przetworzonych: {page_counter}.')