# cargar_datos.py
import csv
from collections import defaultdict

def cargar_datos(ruta_csv):
    imagenes_info = defaultdict(list)
    with open(ruta_csv, 'r', encoding='utf-8') as csvfile:
        csv_reader = csv.reader(csvfile)
        for row in csv_reader:
            ruta, etiquetas, fecha, evento = row
            for etiqueta in etiquetas.split(';'):
                imagenes_info[ruta].append({'etiqueta': etiqueta, 'fecha': fecha, 'evento': evento})
    return imagenes_info
