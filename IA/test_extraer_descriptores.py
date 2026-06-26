# test_extraer_descriptores.py

import cv2
import dlib
import numpy as np

# Asegúrate de que estas rutas sean correctas en tu sistema
predictor_path = "shape_predictor_68_face_landmarks.dat"
face_rec_model_path = "dlib_face_recognition_resnet_model_v1.dat"
ruta_imagen_prueba = "./imagenes/prueba.jpg"

detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor(predictor_path)
face_rec_model = dlib.face_recognition_model_v1(face_rec_model_path)

def extraer_descriptores(imagen):
    rostros_detectados = detector(imagen, 1)
    descriptores = []
    for rostro in rostros_detectados:
        puntos = predictor(imagen, rostro)
        descriptor = np.array(face_rec_model.compute_face_descriptor(imagen, puntos))
        descriptores.append(descriptor)
    return descriptores

# Cargar la imagen y convertirla al formato RGB
imagen = cv2.imread(ruta_imagen_prueba)
imagen_rgb = cv2.cvtColor(imagen, cv2.COLOR_BGR2RGB)

# Extraer los descriptores e imprimirlos
descriptores_imagen_prueba = extraer_descriptores(imagen_rgb)
for descriptor in descriptores_imagen_prueba:
    print(descriptor)
