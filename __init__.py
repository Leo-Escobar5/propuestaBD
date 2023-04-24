from flask import Flask, render_template
app = Flask(__name__)
from CargarCSV.routes import cargarCSV
import os
from config import UPLOAD_FOLDER





app.config.from_pyfile('config.py')
UPLOAD_FOLDER = app.config.get('UPLOAD_FOLDER')
#Definir la ruta de la página principal
@app.route('/')
def index():
    return render_template('index.html')

app.register_blueprint(cargarCSV)

#Ejecutar la aplicación en el puerto 3000
if __name__ == '__main__':
    app.run(debug=True, port=3000)
