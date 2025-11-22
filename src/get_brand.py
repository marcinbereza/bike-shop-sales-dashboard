import csv

all_brands = ['AXA', 'Abus', 'Accent', 'Assos', 'Atran Velo', 'Author', 'BBB Cycling', 'Basil', 'Bell', 'Blackburn', 'Bontrager', 'CN Spoke', 'Cannondale', 'CatEye', 'Crank Brothers', 'Creme', 'Dartmoor', 'Diamant', 'Electra', 'Elite', 'Endura', 'Ergon', 'Extrawheel', 'FOX', 'Factor', 'Finish Line', 'Fizik', 'GT', 'Garmin', 'Giant', 'Giro', 'HJC', 'Herrmans', 'Hiplok', 'Infini', 'K-Edge', 'KASK', 'Knog', 'Komon Bikes', 'Kross', 'Kryptonite', 'Lezyne', 'M-Wave', 'MET', 'MagicShine', 'Magnum', 'Marin', 'Momum', 'Mongoose', 'Morgan Blue', 'Motorex', 'Muc-Off', 'NS Bikes', 'OXC', 'Octane One', 'OnGuard', 'Orbea', 'Orlieb', 'Ortlieb', 'PRO', 'Park Tool', "Peaty's", 'Pinarello', 'Pirelli', 'Polygon', 'ProX', 'Puky', 'RWR', 'Rapha', 'Restrap', 'Rock Shox', 'Rohloff', 'Rondo', 'SKS Germany', 'SRAM', 'Saks', 'Scicon', 'Shimano', 'Sigma', 'Specialized', 'Thule', 'Topeak', 'Trek', 'Trelock', 'Troy Lee Designs (TLD)', 'Unibike', 'Unior', 'Velosock', 'Wahoo', 'Weldtite', 'Woom', 'Zefal']

brand_to_compony = {
    'Bontrager':        'Trek',
    'Diamant':          'Trek',
    'Trek':             'Trek',
    'Electra':          'Trek',
    'NS Bikes':         'NS Bikes',
    'Octane One':       'NS Bikes',
    'Rondo':            'NS Bikes',
    'Rock Shox':        'SRAM',
    'SRAM':             'SRAM',
    'Accent':           'Velo',
    'Author':           'Velo',
    'Dartmoor':         'Velo'}

company_country = {
    'Kryptonite':       'Germany',
    'AXA':              'Netherlands',
    'Abus':             'Germany',
    'Accent':           'Poland',
    'Assos':            'Switzerland',
    'Atran Velo':       'Sweden',
    'Basil':            'Netherlands',
    'BBB Cycling':      'Netherlands',
    'Bell':             'USA',
    'Blackburn':        'USA',
    'CN Spoke':         'Taiwan',
    'Cannondale':       'USA',
    'CatEye':           'Japan',
    'Crank Brothers':   'USA',
    'Creme':            'Poland',
    'Elite':            'Italy',
    'Endura':           'Scotland',
    'Ergon':            'German',
    'Extrawheel':       'Poland',
    'FOX':              'USA',
    'Factor':           'UK',
    'Finish Line':      'USA',
    'Fizik':            'Italy',
    'GT':               'USA',
    'Garmin':           'USA',
    'Giant':            'Taiwan',
    'Giro':             'USA',
    'HJC':              'Korean',
    'Herrmans':         'Finland',
    'Hiplok':           'UK',
    'Infini':           'Taiwan',
    'K-Edge':           'USA',
    'KASK':             'Italy',
    'Knog':             'Austria',
    'Komon Bikes':      'Poland',
    'Kross':            'Poland',
    'Lezyne':           'USA',
    'M-Wave':           'German',
    'MET':              'Italy',
    'MagicShine':       'China',
    'Magnum':           'USA',
    'Marin':            'USA',
    'Momum':            'Spain',
    'Mongoose':         'USA',
    'Morgan Blue':      'Belgium',
    'Motorex':          'France',
    'Muc-Off':          'UK',
    'NS Bikes':         'Poland',
    'OXC':              'UK',
    'OnGuard':          'USA',
    'Orbea':            'Spain',
    'Orlieb':           'Germany',
    'Ortlieb':          'Germany',
    'PRO':              'Italy',
    'Park Tool':        'USA',
    'Peaty\'s':         'UK',
    'Pinarello':        'Italy',
    'Pirelli':          'Italy',
    'Polygon':          'Indonesia',
    'ProX':             'Netherlands',
    'Puky':             'Germany',
    'RWR':              'USA',
    'Rapha':            'UK',
    'Restrap':          'UK',
    'Rohloff':          'Germany',
    'SKS Germany':      'Germany',
    'Saks':             'Germany',
    'Scicon':           'Italy',
    'Shimano':          'Japan',
    'Sigma':            'Germany',
    'SRAM':             'USA',
    'Specialized':      'USA',
    'Thule':            'Sweden',
    'Topeak':           'Taiwan',
    'Trek':             'USA',
    'Trelock':          'Germany',
    'Troy Lee Designs (TLD)': 'USA',
    'Unibike':          'Poland',
    'Unior':            'Slovenia',
    'Velosock':         'Latvia',
    'Wahoo':            'USA',
    'Weldtite':         'UK',
    'Woom':             'Austria',
    'Velo':             'Poland', 
    'Zefal':            'France'}


if __name__=='__main__':
    records = []

    for i, brand in enumerate(all_brands):
        producent_id = f'PROD{1_000+i}'
        company = brand_to_compony.get(brand, brand)
        country = company_country.get(company, 'Unknown')
        email = f'{brand.lower().replace(' ', '')}@example.com'

        records.append([producent_id, company, brand, country, email])

    with open('dim_brand.csv', 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['brand_id', 'brand_name', 'company', 'country', 'website'])
        writer.writerows(records)

    print(f"dim_brand.csv wygenerowany | liczba marek: {len(records)}")