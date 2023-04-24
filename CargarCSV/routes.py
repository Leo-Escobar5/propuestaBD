import matplotlib.pyplot as plt
import numpy as np
#importar os
import os
from werkzeug.utils import secure_filename

#importar UPLOAD_FOLDER
from config import UPLOAD_FOLDER

from flask import current_app


import pandas as pd
from flask import Blueprint, render_template, request, redirect, url_for, flash, session, make_response

cargarCSV = Blueprint('cargarCSV', __name__)


# Función para limpiar los datos
def limpiar_datos(file):
    data = pd.read_csv(file)
    # convertir a mayúsculas todos los datos
    data = data.applymap(lambda x: x.upper() if type(x) is str else x)
    # mover todos los numeros de Nombre a la columna Edad
    
    # Eliminar todas las letras del abecedario de la columna Edad
    data['Edad'] = data['Edad'].apply(lambda x: x.replace('A', '').replace('B', '').replace('C', '').replace('D', '').replace('E', '').replace('F', '').replace('G', '').replace('H', '').replace('I', '').replace('J', '').replace('K', '').replace('L', '').replace('M', '').replace('N', '').replace('O', '').replace('P', '').replace('Q', '').replace('R', '').replace('S', '').replace('T', '').replace('U', '').replace('V', '').replace('W', '').replace('X', '').replace('Y', '').replace('Z', ''))
    # Eliminar todos los numeros de la columa Ciudad
    data['Ciudad'] = data['Ciudad'].apply(lambda x: x.replace('0', '').replace('1', '').replace('2', '').replace('3', '').replace('4', '').replace('5', '').replace('6', '').replace('7', '').replace('8', '').replace('9', ''))
    # quitar nan por espacio en blanco
    data = data.fillna('')
    # quitar acentos a todos los datos
    data = data.applymap(lambda x: x.replace('Á', 'A').replace('É', 'E').replace('Í', 'I').replace('Ó', 'O').replace('Ú', 'U') if type(x) is str else x)
    # remplazar los caracteres raros por letras que se parezcan
    data = data.applymap(lambda x: x.replace('Ñ', 'N').replace('Ü', 'U').replace('¿', 'I').replace('¡', 'I') if type(x) is str else x)
    # quitar los espacios en blanco si antes no hay nada o después no hay nada
    data = data.applymap(lambda x: x.strip() if type(x) is str else x)
    # quitar los caracteres especiales que no se parezcan a letras
    data = data.applymap(lambda x: x.replace('(', '').replace(')', '').replace('-', '').replace('.', '').replace(',', '').replace(';', '').replace(':', '').replace('?', '').replace('!', '').replace('°', '').replace('´', '').replace('`', '').replace('¨', '').replace('"', '').replace("'", '').replace('=', '').replace('+', '').replace('*', '').replace('/', '').replace('¿', '').replace('¡', '').replace('º', '').replace('ª', '').replace('·', '').replace('€', '').replace('¢', '').replace('¬', '').replace('§', '').replace('¶', '').replace('•', '').replace('£', '').replace('•', '').replace('¶', '').replace('§', '').replace('¬', '').replace('¢', '').replace('€', '').replace('·', '').replace('ª', '').replace('º', '').replace('¿', '').replace('¡', '').replace('?', '').replace('!', '').replace('°', '').replace('´', '').replace('`', '').replace('¨', '').replace('"', '').replace("'", '').replace('=', '').replace('+', '').replace('*', '').replace('/', '') if type(x) is str else x)
# reemplazar NaN por una cadena vacía
    # eliminar columnas vacías o con datos en NaN
    data = data.dropna(axis=1, how='all')

# guardar los datos limpios en un archivo csv
    data.to_csv('datos_limpios.csv', index=False)
    return data



# Definir la ruta de la página
@cargarCSV.route('/cargarCSV', methods=['GET', 'POST'])
def csv():
    data = None
    if request.method == 'POST':
        file = request.files['csv_file']
        data = limpiar_datos(file)
        # Eliminar filas con valores faltantes en la columna "Edad"
        data = data[data['Edad'] != '']
        data['Edad'] = data['Edad'].astype(float)
        data['Edad'] = data['Edad'].fillna(data['Edad'].median())

        data = data.dropna(subset=['Edad'])
        print(data['Edad'])
        data['Edad'] = data['Edad'].replace('', np.nan)

        # Crear histograma
        plt.hist(data['Edad'], bins=10)
        plt.xlabel('Edad')
        plt.ylabel('Frecuencia')
        # Guardar imagen del histograma en formato PNG

        # Pasar el número de filas, columnas, edad promedio, edad mediana, edad más común, ciudad más común y un histograma de la edad
        return render_template('cargarCSV.html', data=data, filas=data.shape[0], columnas=data.shape[1], edad_promedio=data['Edad'].mean(), edad_mediana=data['Edad'].median(), edad_mas_comun=data['Edad'].mode()[0], ciudad_mas_comun=data['Ciudad'].mode()[0])
    return render_template('cargarCSV.html', data=data)


# Ruta para descargar archivo limpio
@cargarCSV.route('/descargarCSV', methods=['POST'])
def descargarCSV():
    data = request.form['data']
    response = make_response(data)
    response.headers["Content-Disposition"] = "attachment; filename=datos_limpios.csv"
    response.headers["Content-Type"] = "text/csv"
    return response
