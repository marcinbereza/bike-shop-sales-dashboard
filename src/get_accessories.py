from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium import webdriver

from bs4 import BeautifulSoup
import re
from get_bikes import set_columns_name, save_csv, cookie_accept

def accesory_name(
    known_brands:list, 
    product_string:str,
    default_subcategory:str
) -> tuple[str,str,str]:
    
    known_brands = sorted(known_brands, key=len, reverse=True)

    brand = 'Unknown'
    model = product_string
    category_string = ''

    for know_brand in known_brands:
        match_brand = re.search(r'\b' + re.escape(know_brand) + r'\b', product_string, re.IGNORECASE)

        if match_brand:
            brand_start = match_brand.start()
            brand_end   = match_brand.end()

            category_string = product_string[:brand_start].strip()
            brand = know_brand
            model = product_string[brand_end:].strip()
            break

    subcategory = category_string if category_string else default_subcategory
  
    return subcategory, brand, model


def parse(html_source, page_counter:int, brands:list[str], categ:str, subcateg:str, product_counter:int, pref:str):
    soup = BeautifulSoup(html_source, 'lxml')
    rows = soup.find_all(class_='item product product-item')
    parsed_item = []
    prod_id = 0

    for row in rows:
        try:
            product_id = f'{pref}{product_counter + prod_id}'
            img = row.select_one('.product-img a img')
            if img: img = img.get('src')

            product_sku = row.select_one('.detail-wrap div[data-review-product-id]')
            if product_sku: product_sku = product_sku.get('data-review-product-id')
            else: continue
            
            prices = row.select('.price-box span[data-price-amount]')
            if prices: prices = [s['data-price-amount'] for s in prices]
            else: continue
            price_curr     = prices[0] if len(prices)>=1 else ''
            price_discount = prices[1] if len(prices)>=2 else ''
            price_30day    = prices[2] if len(prices)>=3 else ''
            
            product_details = row.select_one('.product-item-link h3').text.strip()
            category = categ
            subcategory, brand, model = accesory_name(brands, product_details, subcateg)

            parsed_item.append([product_id, product_sku, category, subcategory, brand, model, price_curr, price_discount, price_30day, img])
            prod_id += 1
            
        except Exception as e:
            print(f'Błąd parsowania produktu na stronie {page_counter}: {e}')
            continue
    return parsed_item


def download_pipeline(
    *args,
    page_link:str,
    brands:list[str],
    main_category:str,
    main_subcategory:str,
    output_filename:str,
    pref:str,
    timeout:int= 10,
    **kwargs
) -> None:
    
    options = Options()
    options.add_argument('--headless=new') 
    options.add_argument('--disable-gpu')

    driver = webdriver.Chrome(options=options)
    driver.get(page_link)

    wait = WebDriverWait(driver, timeout=timeout)
    page_counter = 1


    set_columns_name(csv_filename=output_filename)
    cookie_accept(wait)
    product_counter = 10_000
    
    
    wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, '.product-item-details')))
    html_source = driver.page_source

    parsed_data = parse(html_source, page_counter, brands, main_category, main_subcategory, product_counter, pref)
    product_counter+=len(parsed_data)

    save_csv(parsed_data, page_counter, output_filename)

    next_btn = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'a.action.next')))
    driver.execute_script('arguments[0].click();', next_btn)
    wait.until(EC.staleness_of(next_btn))

    while next_btn:
        page_counter += 1
        try:
            wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, '.product-item-details')))
            html_source = driver.page_source
            parsed_data = parse(html_source, page_counter, brands, main_category, main_subcategory, product_counter, pref)
            product_counter+=len(parsed_data)

            save_csv(parsed_data, page_counter, output_filename)

            next_btn = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'a.action.next')))
            driver.execute_script('arguments[0].click();', next_btn)
            wait.until(EC.staleness_of(next_btn))

        except Exception as e:
            print(f'Wystąpił nieoczekiwany błąd podczas pracy Selenium: {e}')
            break
        
    driver.quit()
    print(f'Zakończono proces. Całkowita liczba stron przetworzonych: {page_counter}.')


if __name__=='__main__':
    download_pipeline(
        page_link='https://sprint-rowery.pl/zapiecia-do-roweru',
        brands=['Abus', 'OnGuard', 'Kryptonite', 'Magnum', 'Hiplok', 'Zefal', 'Bontrager', 'Giant', 'RWR', 'Trelock', 'AXA', 'Shimano', 'Knog', 'M-Wave', 'OXC', 'Orlieb', 'ProX', 'Scicon'],
        main_category='zapięcia',
        main_subcategory='zapięcia',
        output_filename='../data/zapięcia.csv',
        pref='LOC'
    )

    download_pipeline(
        page_link='https://sprint-rowery.pl/oswietlenie-rowerowe',
        brands=['Lezyne','Knog','CatEye','MagicShine','Blackburn','Bontrager','Infini','Trek','Giant','ProX','Specialized','Garmin','Topeak','AXA','RWR','Zefal','Sigma','Woom','Electra','Herrmans','Author','Cannondale','K-Edge','Kryptonite','Ortlieb','SKS Germany','Saks','Wahoo'],
        main_category='oświetlenie',
        main_subcategory='oświetlenie',
        output_filename='../data/lampki.csv',
        pref='LIG'
    )

    download_pipeline(
        page_link='https://sprint-rowery.pl/narzedzia-rowerowe',
        brands=['Topeak','Park Tool','Lezyne','Weldtite','PRO','Crank Brothers','Bontrager','Finish Line','SKS Germany','Zefal','Rock Shox','Trek','Muc-Off','Accent','Blackburn','RWR','Cannondale','Giant','ProX','Shimano','Unior','Assos','Atran Velo','CN Spoke','Elite','Pirelli','Rohloff','Author','BBB Cycling','Komon Bikes','Kryptonite','Morgan Blue','Motorex','OXC','Peaty\'s','Restrap','SRAM','Scicon'],
        main_category='narzędzia',
        main_subcategory='narzędzia',
        output_filename='../data/narzędzia.csv',
        pref='TOOL'
    )

    download_pipeline(
        page_link='https://sprint-rowery.pl/sakwy-rowerowe',
        brands=['Ortlieb', 'Basil', 'Extrawheel', 'Bontrager', 'Restrap', 'Topeak', 'Shimano', 'Trek', 'Cannondale', 'Diamant', 'Giant', 'ProX', 'SKS Germany', 'Thule', 'Zefal'],
        main_category='sakwa',
        main_subcategory='sakwa',
        output_filename='../data/sakwy.csv',
        pref='SAK'
    )

    download_pipeline(
        page_link='https://sprint-rowery.pl/kaski-rowerowe',
        brands=['Abus', 'Giro', 'FOX', 'MET', 'Bontrager', 'Troy Lee Designs (TLD)', 'HJC', 'Specialized', 'Endura', 'Trek', 'Electra', 'KASK', 'Giant', 'Bell', 'Fizik', 'ProX', 'Woom', 'Assos', 'Shimano', 'Velosock'],
        main_category='kaski',
        main_subcategory='kaski',
        output_filename='../data/kaski.csv',
        pref='HEL'
    )

    download_pipeline(
        page_link='https://sprint-rowery.pl/rekawiczki-rowerowe',
        brands=['FOX', 'Troy Lee Designs (TLD)', 'Giro', 'Specialized', 'Endura', 'Assos', 'Bontrager', 'Trek', 'Giant', 'Rapha', 'Momum', 'Woom', 'Ergon'],
        main_category='rękawiczki',
        main_subcategory='rękawiczki',
        output_filename='../data/rękawiczki.csv',
        pref='GLOV'
    )