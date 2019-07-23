from main import app
from flask import render_template
from flask import abort
from flask import request
from db import database
import utilities as ut
import json
import pandas as pd
from maps import paint_map
from maps import paint_cake
from maps import paint_g


@app.route("/")
def hello():

    return render_template('hello.html')


@app.route("/map/", methods=['POST', 'GET'])
def map_col():
    map_exist = map2_exist = False
    url_root = request.url_root
    ano = ''
    mes = ''
    segmento = ''
    if request.form:
        if (
            'Ano' in request.form and request.form['Ano'],
            'Mes' in request.form and request.form['Mes'],
            'Segmento' in request.form and request.form['Segmento']
        ):
            ano = request.form.get('Ano')
            mes = request.form.get('Mes')
            segmento = request.form.get('Segmento')
            paint_map(ano=ano, mes=mes, segmento=segmento)
            paint_cake()
            map_exist = f'{url_root}iframe_map.html/'
            map2_exist = f'{url_root}iframe_map2.html/'

    return render_template(
        'map.html',
        url_root=url_root,
        map_exist=map_exist,
        map2_exist=map2_exist,
        ano=ano,
        mes=mes,
        segmento=segmento,
    )


@app.route("/map2/", methods=['POST', 'GET'])
def map_col2():
    url_root = request.url_root
    print(request.form)
    image = ' '
    if request.form:
        if (
            'Ano' in request.form and request.form['Ano'],
            'Segmento' in request.form and request.form['Segmento']
        ):
            image = paint_g(
                ano=request.form['Ano'],
                segmento=request.form['Segmento']
            )

    return render_template('map2.html', url_root=url_root, map_exist=image)


@app.route('/iframe_map.html/')
def render_map():
    return render_template('iframe_map.html')


@app.route('/iframe_map2.html/')
def render_map2():
    return render_template('iframe_map2.html')


# @app.route('/cake.png/')
# def cake():
#     return render_template('cake.png')


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
            conect.upsert(request.json['id'], request.json)
            return json.dumps({'Ok': True})
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
