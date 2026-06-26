from flask import Flask, request, jsonify, render_template
import numpy as np
from dotenv import load_dotenv
import os
import openai
from werkzeug.utils import secure_filename
from tempfile import NamedTemporaryFile
import cv2


# Importa las funciones de los nuevos módulos
# from cargar_datos import cargar_datos
# from procesamiento_facial import extraer_descriptores, preparar_descriptores_referencia, reconocer_rostro
# from db import inicializar_db, guardar_descriptores, obtener_descriptores_referencia
# Importa las funciones de los nuevos módulos
from cargar_datos import cargar_datos
from procesamiento_facial import extraer_descriptores, reconocer_rostro
from db import inicializar_db, obtener_descriptores_referencia

# Cargar variables de entorno
load_dotenv()  # Esto carga las variables del archivo .env

app = Flask(__name__)
openai_api_key = os.getenv("OPENAI_API_KEY", "")
# Configurar la carpeta donde se guardarán las imágenes temporalmente
app.config['UPLOAD_FOLDER'] = 'temporales'


# Inicializar la base de datos SQLite y cargar datos de imágenes desde el CSV
inicializar_db()

# Cargar la información de las imágenes desde el CSV
imagenes_info = cargar_datos('personas.csv')


@app.route('/')
def index():
    return render_template('IA.html')


# Prepara y almacena los descriptores de todas tus imágenes de referencia
# Esta función debería ser definida en procesamiento_facial.py para procesar las imágenes indicadas en imagenes_info
# y luego usar guardar_descriptores de db.py para almacenar los resultados en la base de datos SQLite.


@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files or 'text' not in request.form:
        return jsonify({'error': 'Falta archivo o texto'}), 400

    files = request.files.getlist('file')
    text = request.form['text']

    # Procesar el texto con OpenAI
    openai_response = openai.Completion.create(
        engine="davinci",
        prompt=text,
        max_tokens=50  # Ajustar según sea necesario
    )
    # Interpretar la intención del texto
    intent = openai_response.choices[0].text.strip()

    # Procesar las imágenes subidas y buscar coincidencias
    coincidencias = []
    descriptores_referencia = obtener_descriptores_referencia()
    for file in files:
        filename = secure_filename(file.filename)
        # Definir el directorio temporal
        file_path = os.path.join('path_to_temp_folder', filename)
        file.save(file_path)

        # Extraer descriptores de la imagen subida
        descriptores_nueva_imagen = extraer_descriptores(file_path)

        # Comparar con los descriptores de referencia
        for descriptor_nuevo in descriptores_nueva_imagen:
            resultado = reconocer_rostro(
                descriptor_nuevo, descriptores_referencia)
            if resultado is not None:
                coincidencias.append((filename, resultado))

        # Eliminar el archivo temporal después de procesar
        os.remove(file_path)

    # Devolver la respuesta
    return jsonify({
        'status': 'Imagen procesada correctamente',
        'intent': intent,
        'matches': coincidencias
    })


if __name__ == '__main__':
    app.run(debug=True)
