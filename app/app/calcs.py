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
