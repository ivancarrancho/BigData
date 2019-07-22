from db import database
import folium
import pandas as pd
import statistics
import utilities as ut

city_list = {
    'AMAZONAS': 'AMAZONAS',
    'Antioquia': 'ANTIOQUIA',
    'ARAUCA': 'ARAUCA',
    'ARCHIPIELAGO DE SAN ANDRES PROVIDENCIA Y SANTA CATALINA': 'ARCHIPIELAGO DE SAN ANDRES PROVIDENCIA Y SANTA CATALINA',
    'ATLANTICO': 'ATLANTICO',
    'BOLIVAR': 'BOLIVAR',
    'Boyaca': 'BOYACA',
    'Caldas': 'CALDAS',
    'CAQUETA': 'CAQUETA',
    'Casanare': 'CASANARE',
    'Cauca': 'CAUCA',
    'CESAR': 'CESAR',
    'CHOCO': 'CHOCO',
    'Monteria': 'CORDOBA',
    'Cundinamarca': 'CUNDINAMARCA',
    'GUAINIA': 'GUAINIA',
    'GUAVIARE': 'GUAVIARE',
    'Huila': 'HUILA',
    'LA GUAJIRA': 'LA GUAJIRA',
    'MAGDALENA': 'MAGDALENA',
    'Meta': 'META',
    'Nariño': 'NARIÑO',
    'Norte De Santander': 'NORTE DE SANTANDER',
    'PUTUMAYO': 'PUTUMAYO',
    'Quindio': 'QUINDIO',
    'Risaralda': 'RISARALDA',
    'SANTAFE DE BOGOTA D.C': 'SANTAFE DE BOGOTA D.C',
    'Santander': 'SANTANDER',
    'SUCRE': 'SUCRE',
    'Tolima': 'TOLIMA',
    'Valle': 'VALLE DEL CAUCA',
    'VAUPES': 'VAUPES',
    'VICHADA': 'VICHADA',
}


def paint_map(ano, mes, segmento):
    connect = database.get_default_bucket()

    start_key = f'{int(ano)}, {int(mes)}, "{segmento}"'
    end_key = f'{int(ano)}, {int(mes)}, "{segmento}"'

    response = connect.query(
        'dev_product',
        'count',
        query='count?stale=false&connection_timeout=60000&inclusive_end=true&reduce=false&startkey=[{}]&endkey=[{}]&skip=0&full_set=true'.format(
            start_key,
            end_key
        )
    )
    result_list = []
    for r in response:
        result_list.append(r.value)

    result = {}

    for res in result_list:
        city = res[0]
        price = res[1]
        if city in result:
            values = result[city]
            values.append(price)
            result.update({city: values})
        else:
            values = [price]
            result.update({city: values})

    for key, value in result.items():
        result[key] = statistics.mean(value)

    data_map = []
    for key, value in result.items():
        data_map.append([city_list.get(key), value])

    m = folium.Map(location=[4.6482837, -74.2478938], zoom_start=6)

    # Add the color for the chloropleth:
    m.choropleth(
        geo_data='city_files/co-all.json',
        name='choropleth',
        data=data_map,
        columns=['State', 'segmento'],
        key_on='feature.properties.id',
        fill_color='YlGn',
        fill_opacity=0.7,
        line_opacity=0.2,
        legend_name=segmento
    )
    folium.LayerControl().add_to(m)

    # Save to html
    m.save('templates/iframe_map.html')


def paint_cake():
    pass
#     headers = [
#         'V-P',
#         'Año',
#         'Mes',
#         'Numero_mes',
#         'Doc',
#         'Tipo_doc',
#         'Zona',
#         'Sub-Zona',
#         'Nit',
#         'Cliente',
#         'Producto-Familia',
#         'Pres',
#         'Referencia',
#         'Segmento',
#         'Unds',
#         'kg-ltrs',
#         'venta_neta',
#     ]
#     dfs = pd.read_excel('./data2.xlsx')

#     for data in dfs.as_matrix():
#         document = {}
#         for position, header in enumerate(headers):
#             document.update({header: str(data[position]), 'type': 'product'})

#         conect.upsert(ut.generate_id(), document)

#     sizes = [15, 30, 45, 10]

#     fig1, ax1 = plt.subplots()
#     ax1.pie(
#         sizes,
#         # explode=explode,
#         labels=headers,
#         autopct='%1.1f%%',
#         shadow=True,
#         startangle=90
#     )
#     ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.

#     plt.savefig('static/cake.png')


def loadFileProducts():
    print('**********leyendo')
    connect = database.get_default_bucket()

    headers = [
        'V-P',
        'Ano',
        'Mes',
        'Doc',
        'Tipo_doc',
        'Zona',
        'Sub-Zona',
        'Nit',
        'Cliente',
        'Producto-Familia',
        'Pres',
        'Referencia',
        'Segmento',
        'Unds',
        'kg-ltrs',
        'venta_neta',
    ]
    dfs = pd.read_excel('./data.xlsx')
    print('**********termino de leer')

    for data in dfs.as_matrix():
        document = {'type': 'product'}
        for position, header in enumerate(headers):
            document.update({header: data[position]})

        connect.upsert(ut.generate_id(), document)


def loadFileWeather():
    print('**********leyendo')
    connect = database.get_default_bucket()

    # print('hola')
    city_list = [
        'Antioquia',
        'Boyaca',
        'Caldas',
        'Casanare',
        'Cordoba',
        'Cundinamarca',
        'Huila',
        'Meta',
        'Nariño',
        'Norte De Santander',
        'Quindio',
        'Risaralda',
        'Santander',
        'Tolima',
        'Valle',
    ]

    def isNaN(num):
        return num != num

    for cities in city_list:
        headers = [
            'Hora',
            'T',
            'Po',
            'P',
            'Pa',
            'U',
            'DD',
            'Ff',
            'ff10',
            'ff3',
            'N',
            'WW',
            'W1',
            'W2',
            'Tn',
            'Tx',
            'Cl',
            'Nh',
            'H',
            'Cm',
            'Ch',
            'VV',
            'Td',
            'RRR',
            'tR',
            'E',
            'Tg',
            "E'",
            'sss'
        ]
        dfs = pd.read_excel(f'./city_files/{cities}.xls')
        print('**********termino de leer cities ', cities)

        for data in dfs.as_matrix():
            document = {}
            for position, header in enumerate(headers):
                document.update({
                    header: '' if isNaN(data[position]) else data[position],
                    'type': 'weather'
                })

            document.update({'Zona': cities})

            hour = data[0].split('.')
            document.update({
                'Dia': int(hour[0]),
                'Mes': int(hour[1]),
                'Ano': int(hour[2][:4])
            })

            connect.upsert(ut.generate_id(), document)
