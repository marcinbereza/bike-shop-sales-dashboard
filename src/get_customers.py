import pandas as pd
import random, re, csv


def read_data(filename):
    data = pd.read_csv(filename, encoding='utf-8')
    return data.iloc[:,0].tolist()


def parse_dens(value:str) -> int:
    return int(re.match(r'\d+', value)[0])


def parse_perc(value:str) -> float:
    value = value.replace(',','.')
    number = re.findall(r'\d+\.?\d+', value)
    return float(number[0] if number else 0.0)


def gen_adress(data):
    addresses = []
    address_id = 1

    for i, row in data.iterrows():
        addresses.append([f'DEL_{1_000+i}', 'Polska', row['Województwo'], row['Powiat'], row['weight_norm']])
        address_id += 1
    return addresses


def gen_customer(addresses, name_m, name_w, surname_m, surname_w, num_records:int = 10):
    customers = []
    email_counts = {}

    for i in range(1, num_records+1):
        if random.random() < 0.65:  first, last, gender = random.choice(name_m), random.choice(surname_m), 'M'
        else:                       first, last, gender = random.choice(name_w), random.choice(surname_w), 'F'

        key = f'{first.lower()}.{last.lower()}'
        email_counts[key] = email_counts.get(key, 0) + 1

        if email_counts[key]==1:    email = f'{key}@example.com'
        else:                       email = f'{key}{email_counts[key]}@example.com'

        address = addresses.sample(weights=addresses['weight'], n=1).iloc[0]
        customers.append([f'CUST_{1000+i}', first.capitalize(), last.capitalize(), gender, email, address['delivery_id']])

    return customers


if __name__=='__main__':
    name_m = read_data('data/men_name300.csv')
    name_w = read_data('data/women_name300.csv')
    surname_m = read_data('data/men_surname1000.csv')
    surname_w = read_data('data/women_surname1000.csv')
    regions = pd.read_csv('data/powiaty.csv')

    regions['density'] = regions['Gęstość zaludnienia'].apply(parse_dens)
    regions['urbanization'] = regions['Stopień ubarnizacji'].apply(parse_perc)
    regions['weight'] = (regions['urbanization'] / 100 * regions['density'])
    regions['weight_norm'] = regions['weight'] / regions['weight'].sum()

    addresses = gen_adress(regions)
    with open('dim_address.csv', 'w', newline='', encoding='utf-8-sig') as f:
        writer = csv.writer(f)
        writer.writerow(['delivery_id', 'kraj', 'wojewodztwo', 'powiat'])
        writer.writerows(addresses[:-1])

    print(f"dim_adresses.csv wygenerowany | liczba rekordów: {len(addresses)}")

    address_df = pd.DataFrame(addresses, columns=['delivery_id', 'kraj', 'wojewodztwo', 'powiat', 'weight'])
    customers = gen_customer(address_df, name_m, name_w, surname_m, surname_w, 10_000)
    with open('dim_customers.csv', 'w', newline='', encoding='utf-8-sig') as f:
        writer = csv.writer(f)
        writer.writerow(['customer_id', 'name', 'surname', 'gender', 'email', 'delivery_id'])
        writer.writerows(customers)

    print(f"dim_customers.csv wygenerowany | liczba rekordów: {len(customers)}")