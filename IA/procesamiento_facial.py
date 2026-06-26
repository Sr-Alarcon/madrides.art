# procesamiento_facial.py
from db import guardar_descriptores
from db import obtener_descriptores_referencia
import dlib
import numpy as np
import cv2

detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor("shape_predictor_68_face_landmarks.dat")
face_rec_model = dlib.face_recognition_model_v1(
    "dlib_face_recognition_resnet_model_v1.dat")


def extraer_descriptores(file_path):
    img = cv2.imread(file_path)  # cv2 ya lee en formato BGR
    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    rostros_detectados = detector(img_rgb, 1)
    descriptores = []
    for rostro in rostros_detectados:
        puntos = predictor(img_rgb, rostro)
        descriptor = face_rec_model.compute_face_descriptor(img_rgb, puntos)
        descriptores.append(np.array(descriptor))
    return descriptores


def reconocer_rostro(descriptor_prueba, descriptores_referencia, umbral=0.6):
    # Asegurarse de que ambos descriptores son bidimensionales
    descriptor_prueba = np.atleast_2d(descriptor_prueba)
    descriptores_referencia = np.atleast_2d(descriptores_referencia)

    # Calcular la distancia euclidiana
    distancias = np.linalg.norm(descriptores_referencia - descriptor_prueba, axis=1)

    # Encontrar la coincidencia más cercana y verificar si está por debajo del umbral
    indice_minimo = np.argmin(distancias)
    if distancias[indice_minimo] < umbral:
        return True
    return False



def preparar_descriptores_referencia(imagenes_info):
    for ruta, infos in imagenes_info.items():
        descriptores = extraer_descriptores(ruta)
        for descriptor in descriptores:
            # Aquí asumimos que infos es una lista de diccionarios, cada uno con las etiquetas y otros metadatos
            for info in infos:
                # Ajusta según tu estructura de datos
                etiqueta = info['etiqueta']
                # Convertir el descriptor a un formato adecuado para almacenamiento, por ejemplo, una lista a un blob
                descriptor_blob = np.array(descriptor).tobytes()
                guardar_descriptores(ruta, descriptor_blob, etiqueta)
