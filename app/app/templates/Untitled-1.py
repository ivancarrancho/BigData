function (doc, meta) {
    if(
        doc.type === 'product' &&
        doc.Ano &&
        doc.Mes &&
        doc.Segmento &&
        doc.venta_neta &&
        doc.Zona
    ){
        emit([doc.Ano, doc.Mes, doc.Segmento], [doc.Zona, doc.venta_neta])
    }
}

function (doc, meta) {
    if(
        doc.type === 'product' &&
        doc.Ano &&
        doc.Mes &&
        doc.Segmento &&
        doc.venta_neta &&
        doc.Zona
    ){
        emit([doc.Ano, doc.Mes, doc.Segmento], [doc.Zona, doc.venta_neta])
    }
}

import utilities as ut
from db import database
import random
connect = database.get_default_bucket()


city_list = [
    'AMAZONAS',
    'Antioquia',
    'ARAUCA',
    'ATLANTICO',
    'BOLIVAR',
    'Boyaca',
    'Caldas',
    'CAQUETA',
    'Casanare',
    'Cauca',
    'CESAR',
    'CHOCO',
    'Monteria',
    'Cundinamarca',
    'GUAINIA',
    'GUAVIARE',
    'Huila',
    'LA GUAJIRA',
    'MAGDALENA',
    'Meta',
    'Nariño',
    'Norte De Santander',
    'PUTUMAYO',
    'Quindio',
    'Risaralda',
    'SANTAFE DE BOGOTA D.C',
    'Santander',
    'SUCRE',
    'Tolima',
    'Valle',
    'VAUPES',
    'VICHADA',
]

docs = []
for city in city_list:
    for year in range(2015, 2020):
        for month in range(1, 13):
            for segment in ['Fungicidas', 'Insecticidas', 'Herbicidas', 'Coadyuvantes', 'Otros', 'Biosoluciones']:
                docs.append(
                    {
                        "type": "product",
                        "V-P": "VTAS",
                        "Ano": year,
                        "Mes": month,
                        "Doc": 411675,
                        "Tipo_doc": "Factura",
                        "Zona": city,
                        "Sub-Zona": city,
                        "Nit": "860046341-I",
                        "Cliente": "Federacion Colombiana De Productores De Papa Fedepapa",
                        "Producto-Familia": "Borax Tecnico",
                        "Pres": 20,
                        "Referencia": "300BOTEC020",
                        "Segmento": segment,
                        "Unds": random.randint(1, 100),
                        "kg-ltrs": 600,
                        "venta_neta": random.randint(100000, 10000000)
                    }
                )
                docs.append(
                    {
                        "type": "product",
                        "V-P": "VTAS",
                        "Ano": year,
                        "Mes": month,
                        "Doc": 411675,
                        "Tipo_doc": "Factura",
                        "Zona": city,
                        "Sub-Zona": city,
                        "Nit": "860046341-I",
                        "Cliente": "Federacion Colombiana De Productores De Papa Fedepapa",
                        "Producto-Familia": "Borax Tecnico",
                        "Pres": 20,
                        "Referencia": "300BOTEC020",
                        "Segmento": segment,
                        "Unds": random.randint(1, 100),
                        "kg-ltrs": 600,
                        "venta_neta": random.randint(100000, 10000000)
                    }
                )

for doc in docs:
    connect.upsert(ut.generate_id(), doc)
