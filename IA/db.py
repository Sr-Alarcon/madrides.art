import sqlite3
import numpy as np

DATABASE = 'descriptores.db'

def inicializar_db():
    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()
    # Crear tabla si no existe
    c.execute('''CREATE TABLE IF NOT EXISTS descriptores
                 (ruta TEXT, descriptor BLOB, etiqueta TEXT)''')
    conn.commit()
    conn.close()

def guardar_descriptores(descriptor, etiqueta):
    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()
    # Convertir el descriptor a formato de almacenamiento (BLOB)
    descriptor_blob = descriptor.tobytes()
    c.execute('''
        INSERT INTO descriptores (descriptor, etiqueta) 
        VALUES (?, ?)
    ''', (descriptor_blob, etiqueta))
    conn.commit()
    conn.close()

def obtener_descriptores_referencia():
    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()
    c.execute('SELECT * FROM descriptores')
    descriptores = [(ruta, np.frombuffer(descriptor, dtype=np.float64), etiqueta)
                    for ruta, descriptor, etiqueta in c.fetchall()]
    conn.close()
    return descriptores

def existe_descriptor(descriptor):
    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()
    descriptor_blob = descriptor.tobytes()
    c.execute('''
        SELECT 1 FROM descriptores WHERE descriptor = ?
    ''', (descriptor_blob,))
    existe = c.fetchone() is not None
    conn.close()
    return existe