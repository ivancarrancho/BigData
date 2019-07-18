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
