# test_reconocer_rostro.py

import numpy as np
from procesamiento_facial import reconocer_rostro
from db import obtener_descriptores_referencia

# Asumiendo que 'descriptores_imagen_prueba' es una lista de descriptores extraídos de la imagen de prueba
descriptores_referencia = obtener_descriptores_referencia()  # Esta función debe devolver una lista de descriptores de la base de datos

# Reemplaza esto con el descriptor extraído de la imagen de prueba
descriptor_prueba = np.array([-0.11029682, 0.09323826, 0.05108814, -0.07608712, -0.09404649, 0.01407023, 0.00503913, -0.04262306, 0.17074305, 0.02349016, 0.24696475, -0.02560342, -0.12138445, -0.07009158, -0.07115454, 0.1372827, -0.13307545, -0.13398266, -0.06882317, -0.07858525, 0.02018955, -0.01300417, -0.04804053, 0.06206021, -0.1011734, -0.33090124, -0.08110522, -0.16647087, 0.0613641, -0.17647979, 0.05282943, 0.09648067, -0.17566952, -0.09587918, 0.01185098, 0.0830467, 0.04884602, 0.01328497, 0.12619486, 0.04489668, -0.18141234, 0.0619991, 0.04428837, 0.36047921, 0.11923666, 0.07445461, 0.04359562, 0.03711728, 0.01752489, -0.19389746, 0.09019314, 0.06428412, 0.22008194, -0.03188483, -0.00793086, -0.11280036, -0.02110247, 0.0473851, -0.22414979, 0.09132263, 0.11510612, -0.07907162, -0.05978145, 0.00624245, 0.24811624, 0.13670649, -0.09829154, -0.08677616, 0.14399421, -0.0896688, -0.0144205, 0.02543443, -0.11526867, -0.10227998, -0.2431096, 0.10370774, 0.50275946, 0.06198907, -0.20172958, -0.01298509, -0.1719289, 0.03592003, -0.02584414, -0.00437759, -0.145272, 0.04084603, -0.10660221, 0.04055195, 0.18116318, 0.00298831, -0.03540015, 0.13012719, -0.01342968, -0.04601633, -0.00542236, 0.00199679, -0.05658436, -0.0231428, -0.09597009, -0.08863627, 0.00473468, -0.05262088, -0.00240998, 0.10533164, -0.26098657, 0.12526213, 0.02181187, -0.07220055, -0.01133223, 0.11954214, -0.0816829, -0.07940905, 0.20437109, -0.20174396, 0.13021058, 0.21000692, 0.07055984, 0.11198363, 0.09719554, 0.03013326, 0.01951977, -0.03506364, -0.09942952, -0.05836113, 0.07504155, -0.05394346, 0.07921843, 0.03610256])

coincidencias = []

# Umbral para determinar una coincidencia
umbral = 0.5  # Puede que necesites ajustar esto

# Analizar cada descriptor de referencia
for ruta, descriptor_serializado, etiqueta in descriptores_referencia:
    descriptor_ref = np.frombuffer(descriptor_serializado, dtype=np.float64)
    descriptor_ref = descriptor_ref.reshape(1, -1)  # Asegúrate de que el reshape es correcto

    # Calcular la distancia
    distancia = np.linalg.norm(descriptor_ref - descriptor_prueba)

    # Imprimir la distancia para depuración
    print(f"Comparando con {etiqueta}: Distancia = {distancia}")

    # Si la distancia es menor que el umbral, añadir a coincidencias
    if distancia < umbral:
        print(f"Coincidencia encontrada: {etiqueta}")
        coincidencias.append(etiqueta)

# Eliminar duplicados de coincidencias
coincidencias_unicas = list(set(coincidencias))

# Imprimir las coincidencias encontradas
if coincidencias_unicas:
    print(f"Se encontraron coincidencias únicas: {coincidencias_unicas}")
else:
    print("No se encontraron coincidencias.")