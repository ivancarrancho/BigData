from main import app
from flask import render_template
from flask import abort
from flask import request
from db import database
import utilities as ut
import json
import pandas as pd


@app.route("/")
def hello():
    return render_template('hello.html')


@app.route("/create/", methods=['POST'])
def create():
    if request.json:
        conect = database.get_default_bucket()
        conect.upsert(ut.generate_id(), request.json)

        return json.dumps({'Ok': True})

    abort(400, 'format error')


@app.route("/edit/", methods=['POST'])
def edit():
    if request.json:
        conect = database.get_default_bucket()
        if 'id' in request.json and request.json['id']:
            conect.upsert(request.json['id'],request.json)
            return json.dumps({ 'Ok' : True })
        else:
            abort(400, 'key no defined')

    return print(request.json)
    abort(400, 'format error')


@app.route("/delete/", methods=['POST'])
def delete():

    if request.json:
        conect = database.get_default_bucket()
        if 'id' in request.json and request.json['id']:
            conect.remove(request.json['id'])
            return json.dumps({'Ok': True})
        else:
            abort(400, 'key no defined')

    abort(400, 'format error')


def loadFile():
    conect = database.get_default_bucket()
    # print('hola')
    headers = [
        'V-P',
        'Año',
        'Mes',
        'Numero_mes',
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

    for data in dfs.as_matrix():
        document = {}
        for position, header in enumerate(headers):
            document.update({header: str(data[position]), 'type': 'product'})

        conect.upsert(ut.generate_id(), document)


# Media
def average(data_list):
    return round(float(sum(data_list) / len(data_list)), 2)


# Mediana
def mediana(data_list):
    data_list.sort()

    if len(data_list) % 2 == 0:
        n = len(data_list)
        return (data_list[n / 2 - 1] + data_list[n / 2]) / 2
    else:
        return data_list[len(data_list) / 2]


# DesStd
def DesStd(data_list):
    n = len(data_list)

    promedio = average(data_list)
    cuadrados = []
    for dato in data_list:
        r = (dato - promedio) ** 2
        cuadrados.append(r)

    return (sum(cuadrados) / (n - 1)) ** 0.5


# Varianza
def varianza(data_list):
    suma = 0
    m = average(data_list)
    for elemento in data_list:
        suma += (elemento - m) ** 2

    return suma / float(len(data_list))


# Max
def max_data(data_list):
    return max(data_list)


# Min
def min_data(data_list):
    return min(data_list)
