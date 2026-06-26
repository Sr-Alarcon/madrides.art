from flask import Flask, request, jsonify, render_template, url_for
import numpy as np
import os
from werkzeug.utils import secure_filename
from tempfile import NamedTemporaryFile
import shutil

# Tus importaciones personalizadas
from procesamiento_facial import extraer_descriptores, reconocer_rostro
from db import inicializar_db, obtener_descriptores_referencia, guardar_descriptores, existe_descriptor
from cargar_datos import cargar_datos

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'temporales'
app.config['MATCHES_FOLDER'] = 'static/matches'
# Asegúrate de que el directorio para las coincidencias existe
os.makedirs(app.config['MATCHES_FOLDER'], exist_ok=True)

# Asumiendo que tienes una función que carga 'personas.csv' y devuelve un diccionario
etiquetas_info = cargar_datos('personas.csv')

@app.route('/')
def index():
    return render_template('IA.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files or 'text' not in request.form:
        return jsonify({'error': 'No se ha enviado archivo o texto'}), 400

    files = request.files.getlist('file')
    text = request.form['text'].lower()
    palabras_clave = text.split()

    etiquetas_relevantes = obtener_etiquetas_relevantes(palabras_clave)

    coincidencias = []
    imagenes_resultantes = []
    for file in files:
        filename = secure_filename(file.filename)
        with NamedTemporaryFile(delete=True, dir=app.config['UPLOAD_FOLDER']) as temp_file:
            file_path = temp_file.name
            file.save(file_path)

            descriptores_imagen = extraer_descriptores(file_path)
            descriptores_referencia = obtener_descriptores_referencia()

            for descriptor in descriptores_imagen:
                for ruta, descriptor_serializado, etiqueta in descriptores_referencia:
                    descriptor_ref = np.frombuffer(descriptor_serializado, dtype=np.float64)
                    if etiqueta in etiquetas_relevantes and reconocer_rostro(descriptor, descriptor_ref):
                        resultado_path = os.path.join(app.config['MATCHES_FOLDER'], filename)
                        shutil.copy(file_path, resultado_path)
                        imagen_url = url_for('static', filename=f'matches/{filename}')
                        imagenes_resultantes.append(imagen_url)
                        coincidencias.append(etiqueta)
                        break

    return jsonify({'coincidencias': coincidencias, 'imagenes_resultantes': imagenes_resultantes})

def obtener_etiquetas_relevantes(palabras_clave):
    etiquetas_info = cargar_datos('personas.csv')
    etiquetas_relevantes = [etiqueta for palabra in palabras_clave for etiqueta, infos in etiquetas_info.items() if palabra in etiqueta.lower()]
    return etiquetas_relevantes

if __name__ == '__main__':
    inicializar_db()  # Asegurarse de que la base de datos está inicializada
    app.run(debug=True)