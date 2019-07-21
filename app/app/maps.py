import pandas as pd
import folium
import os
import matplotlib.pyplot as plt
from db import database
import utilities as ut
import math

# Load the shape of the zone (US states)
# Find the original file here: https://github.com/python-visualization/folium/tree/master/examples/data
# You have to download this file and set the directory where you saved it


def paint_map():

    state_unemployment = 'city_files/us_example.csv'
    state_data = pd.read_csv(state_unemployment)

    m = folium.Map(location=[4.6482837, -74.2478938], zoom_start=6)

    # Add the color for the chloropleth:
    m.choropleth(
        geo_data='city_files/co-all.json',
        name='choropleth',
        data=state_data,
        columns=['State', 'Unemployment'],
        key_on='feature.properties.id',
        fill_color='YlGn',
        fill_opacity=0.7,
        line_opacity=0.2,
        legend_name='Unemployment Rate (%)'
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
    conect = database.get_default_bucket()

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
        document = {}
        for position, header in enumerate(headers):

            document.update({header: data[position], 'type': 'product'})

        conect.upsert(ut.generate_id(), document)


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
