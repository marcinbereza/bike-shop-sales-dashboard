from datetime import date, timedelta
from pandas import DataFrame
import pandas as pd
import random, os


def growth_factor(current_date:date, start:date, end:date) -> float:
    total_days = (end - start).days
    passed_days = (current_date - start).days
    return passed_days / total_days


def base_orders_trend(date:date, min_sales:int, max_sales:int, start:date, end:date) -> float:
    return min_sales + growth_factor(date, start, end) * (max_sales - min_sales)


def weekday_multiplier(date:date) -> float:
    wd = date.weekday()
    if wd == 5:     return 1.2
    elif wd == 6:   return 0.6
    return 1.0


def orders_per_day(date:date, min_sales:int, max_sales:int, start:date, end:date) -> int:
    SEASON_MULTIPLIER = {
        1: 0.5, 2: 0.6, 3: 0.9,
        4: 1.1, 5: 1.3, 6: 1.5,
        7: 1.6, 8: 1.5, 9: 1.2,
        10: 1.0, 11: 0.8, 12: 0.6}

    base = base_orders_trend(date, min_sales, max_sales, start, end)
    seasonal = SEASON_MULTIPLIER[date.month]
    weekday = weekday_multiplier(date)
    noise = random.uniform(0.85, 1.15)
    orders = base * seasonal * weekday * noise
    return max(1, int(round(orders)))


def get_price(record:DataFrame) -> float:
    normal      = int(record['Regular_Price']*100)
    std_disc    = int(record['Discount_Price']*100) if pd.notna(record['Discount_Price']) else normal
    max_disc    = int(record['30Day_Price']*100) if pd.notna(record['30Day_Price']) else normal

    if random.random()<0.7:   return random.randint(min(normal, std_disc), max(normal, std_disc))/100
    else:                   return random.randint(min(std_disc, max_disc), max(std_disc, max_disc))/100


def gen_order(order_id:str, date_id:int, customers:DataFrame, bikes:DataFrame, accessories:dict[DataFrame]):
    accessory_weights = {
        'category': ['locks', 'lights', 'tools', 'bags', 'helmets', 'gloves'],
        'online':   [0.20, 0.20, .28, .05, .02, 0.15],
        'store':    [0.30, 0.25, .05, .15, .05, 0.10]}
    
    records = []
    basket = {}

    customer = customers.sample(1).iloc[0]
    channel = 'online' if random.random() < 0.65 else 'store'

    # Bike selection
    prob_bike = 0.025 if channel == 'online' else 0.04
    if random.random() < prob_bike:
        bikes_qty = random.choices([1,2,3,4], [0.55, 0.3, 0.13, .02])[0]
        for _ in range(bikes_qty):
            bike_row = bikes.sample(1).iloc[0]
            bike_id = bike_row['product_id']

            if bike_id not in basket: basket[bike_id] = {'row': bike_row, 'qty': 0}
            basket[bike_id]['qty'] += 1

    # Accessories selection
    accessories_qty = random.randint(1,5) if channel == 'online' else random.randint(3,8)
    for _ in range(accessories_qty):
        cat = random.choices(accessory_weights['category'], accessory_weights[channel])[0]
        acc_row = accessories[cat].sample(1).iloc[0]
        acc_id = acc_row['product_id']

        if acc_id not in basket: basket[acc_id] = {'row': acc_row, 'qty': 0}
        basket[acc_id]['qty'] += 1

    # Save list
    for prod_id, info in basket.items():
        row = info['row']
        qty = info['qty']
        final_price = get_price(row)

        records.append([order_id, date_id, customer['customer_id'], customer['delivery_id'], prod_id, qty, final_price, channel])
    return records


def gen_sales(
        start_date:date, end_date:date,
        min_sales:int, max_sales:int,
        bikes:DataFrame, accessories:DataFrame) -> None:
    curr_date = start_date
    sales = []

    output_dir = 'sales_monthly'
    if not os.path.exists(output_dir): os.makedirs(output_dir)

    while curr_date <= end_date:
        date_id = int(curr_date.strftime('%Y%m%d'))
        date_prefix = date_id*10_000

        orders_today = orders_per_day(curr_date, min_sales, max_sales, start_date, end_date)

        for i in range(1, orders_today+1):
            curr_order_id = date_prefix + i
            sales.extend(gen_order(curr_order_id, date_id, customers, bikes, accessories))

        tomorrow = curr_date + timedelta(days=1)
        if tomorrow.day == 1 or curr_date == end_date:
            if sales:
                filename = f'sales_{curr_date.strftime('%Y_%m')}.csv'
                filepath = os.path.join(output_dir, filename)

                df_temp = pd.DataFrame(sales, columns=[
                    'order_id', 'date_id', 'customer_id', 'delivery_id', 
                    'product_id', 'qty', 'unit_price', 'channel'
                ])

                df_temp.to_csv(filepath, index=False, encoding='utf-8')
                print(f'\r📁 Wygenerowano i zapisano plik: {filename} zawierający: {len(sales)} produktów', end='')
                sales = []

        curr_date += timedelta(days=1)

    print(f'\n✅Wszystkie miesiące zostały zapisane w folderze: {output_dir}')


if __name__=='__main__':
    customers   = pd.read_csv('dim_customers.csv')
    bikes       = pd.read_csv('products/bikes.csv')
    accessories = {
        'locks':    pd.read_csv('products/zapięcia.csv'),
        'lights':   pd.read_csv('products/lampki.csv'),
        'tools':    pd.read_csv('products/narzędzia.csv'),
        'bags':     pd.read_csv('products/sakwy.csv'),
        'helmets':  pd.read_csv('products/kaski.csv'),
        'gloves':   pd.read_csv('products/rękawiczki.csv')}

    gen_sales(
        start_date  = date(2023, 1, 1),
        end_date    = date(2025,12,16),
        min_sales   = 5, max_sales = 140,
        bikes=bikes, accessories=accessories
    )