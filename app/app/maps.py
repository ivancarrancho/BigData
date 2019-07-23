from db import database
import folium
import pandas as pd
import statistics
import utilities as ut
import math
import numpy as np
from itertools import groupby
from couchbase.n1ql import CONSISTENCY_REQUEST
from couchbase.n1ql import N1QLQuery
import base64
from io import BytesIO
from random import randint
import matplotlib.pyplot as plt


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


def total_products():
    connect = database.get_default_bucket()

    response = connect.query(
        'dev_product',
        'count',
        query='count?stale=false&reduce=true&full_set=true'
    )
    result_list = []

    for r in response:
        result_list.append(r.value)

    return result_list


def total_sold():
    connect = database.get_default_bucket()

    response = connect.query(
        'dev_fix',
        'fix',
        query='count?stale=false&reduce=true&full_set=true'
    )

    result_list = []

    for r in response:
        result_list.append(r.value)

    return result_list


def total_weather():
    connect = database.get_default_bucket()

    response = connect.query(
        'dev_weather',
        'count',
        query='count?stale=false&reduce=true&full_set=true'
    )
    result_list = []

    for r in response:
        result_list.append(r.value)

    return result_list


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

    #  Second map
    connect = database.get_default_bucket()

    start_key = f'{int(ano)}, {int(mes)}'
    end_key = f'{int(ano)}, {int(mes)}'
    # Ivan probar esta vista, del segundo mapa
    response = connect.query(
        'dev_product2',
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
        columns=['State'],
        key_on='feature.properties.id',
        fill_color='YlGn',
        fill_opacity=0.7,
        line_opacity=0.2,
        legend_name='Lluvia'
    )
    folium.LayerControl().add_to(m)

    # Save to html
    m.save('templates/iframe_map2.html')


def average_cake(headers, sizes, ano, segmento):
    fig1, ax1 = plt.subplots()
    ax1.pie(
        sizes,
        labels=headers,
        autopct='%1.1f%%',
        shadow=True,
        startangle=90
    )
    ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.

    plt.title(
        f"Promedio de ventas {ano} - {segmento}",
        bbox={'facecolor':'0.8', 'pad':5}
    )
    plt.savefig('static/average_cake.png')


def quantity_cake(headers, sizes, ano, segmento):
    fig1, ax1 = plt.subplots()
    ax1.pie(
        sizes,
        labels=headers,
        autopct='%1.1f%%',
        shadow=True,
        startangle=90
    )
    ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
    plt.title(
        f"Promedio de lluvia {ano} - {segmento}",
        bbox={'facecolor':'0.8', 'pad':5}
    )
    plt.savefig('static/quantity_cake.png')


def paint_cake():
    headers = ['Fungicidas', 'Insecticidas', 'Herbicidas', 'Coadyuvantes', 'Otros', 'Biosoluciones']

    sizes = [
        randint(1000, 100000),
        randint(1000, 100000),
        randint(1000, 100000),
        randint(1000, 100000),
        randint(1000, 100000),
        randint(1000, 100000)
    ]

    fig1, ax1 = plt.subplots()
    ax1.pie(
        sizes,
        # explode=explode,
        labels=headers,
        autopct='%1.1f%%',
        shadow=True,
        startangle=90
    )
    ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.

    plt.savefig('static/cake.png')


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
    dfs = pd.read_excel('./data2.xlsx')
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


def fixed(new_list):
    a = len(new_list)

    while a < 12:
        a += 1
        new_list.append(randint(100000, 1000000))

    return new_list


def paint_g(ano, segmento):
    connect = database.get_default_bucket()

    #  first query
    start_key = f'{int(ano)}, "{segmento}"'
    end_key = f'{int(ano)}, "{segmento}"'

    response = connect.query(
        'dev_unds',
        'count_unds',
        query='count?stale=false&inclusive_end=true&reduce=false&full_set=true&startkey=[{}]&endkey=[{}]&skip=0&full_set=true'.format(
            start_key,
            end_key
        )
    )
    response_list = []
    for r in response:
        response_list.append(r.value)

    #  Second query
    start_key = f'{int(ano)}'
    end_key = f'{int(ano)}'

    response = connect.query(
        'dev_weather',
        'count',
        query='count?stale=false&inclusive_end=true&reduce=false&full_set=true&startkey=[{}]&endkey=[{}]&skip=0&full_set=true'.format(
            start_key,
            end_key
        )
    )

    response_list_2 = []
    for r in response:
        response_list_2.append(r.value)

    x = ['Ene', 'Feb', 'Mar', 'Abr', 'May', 'Jun', 'Jul', 'Ago', 'Sep', 'Oct', 'Nov', 'Dic']

    print(response_list)

    d2 = []
    for i, g in groupby(sorted(response_list), key=lambda x: x[0]):
        d2.append(sum(v[1] for v in g))

    d3 = []
    for i, g in groupby(sorted(response_list_2), key=lambda x: x[0]):
        d3.append(sum(v[1] for v in g))

    if len(d2) < 12:
        d2 = fixed(d2)

    if len(d3) < 12:
        d3 = fixed(d3)

    y = d2
    z = d3
    average_cake(x, d2, ano, segmento)
    quantity_cake(x, d3, ano, segmento)

    print(y)
    print(z)
    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.plot(x, y, '-', label='Ventas')

    ax2 = ax.twinx()
    ax2.plot(x, z, '-r', label='Porcentaje de lluvia')
    fig.legend(loc=1)

    ax.set_xlabel("x [Meses]")
    ax.set_ylabel(r"Cantidad de venta ")
    ax2.set_ylabel(r"Porcentaje de lluvia")
    buf = BytesIO()
    fig.savefig(buf, format="png")

    return base64.b64encode(buf.getbuffer()).decode("ascii")
    # plt.savefig('static/cake2.png')
